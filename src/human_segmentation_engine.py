"""High level interface to segmentate images with prominent humans on them."""

import cv2
import numpy as np

from src.models.loaders import get_tensorflow_model_file
from src.utils.image_interpreter import ImageInterpreter


# pylint: disable=R0903
# Class has enough public methods.
class HumanSegmentationEngine:
    """Class representing an engine extracting prominent humans from backgrounds."""

    @classmethod
    def create(cls, tensorflow_model_path=get_tensorflow_model_file()):
        """Creates HumanSegmentationEngine instance.

        Uses default tensorflow model if not specified.
        """

        interpreter = ImageInterpreter(tensorflow_model_path)
        return HumanSegmentationEngine(interpreter)

    def __init__(self, interpreter: ImageInterpreter):
        self.__interpreter = interpreter

    def perform_segmentation(self, original_image):
        """Performs humans segmentation for the given image.

        Returns a bit mask the same size as the original image,
        where the mask specifies people locations.
        """

        height = original_image.shape[0]
        width = original_image.shape[1]

        image = cv2.resize(original_image, (256, 144))
        image = np.asarray(image)
        image = image / 255.0
        image = image.astype(np.float32)
        image = image[np.newaxis, :, :, :]

        foreground, background = self.__interpreter.segment_layers(image)

        foreground_inverted = np.invert((foreground > 0.5) * 255)
        background_inverted = np.invert((background > 0.5) * 255)

        foreground_resized = cv2.resize(
            np.uint8(foreground_inverted), (width, height)
        )
        background_resized = cv2.resize(
            np.uint8(background_inverted), (width, height)
        )

        final_mask = cv2.ximgproc.jointBilateralFilter(
            background_resized, foreground_resized, 8, 75, 75
        )
        final_mask = cv2.cvtColor(final_mask, cv2.COLOR_GRAY2RGB)

        return final_mask
