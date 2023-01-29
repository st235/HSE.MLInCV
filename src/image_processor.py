import cv2
import numpy as np
from tensorflow.lite.python.interpreter import Interpreter


class ImageProcessor:
    def __init__(self, model: str):
        self.__interpreter = Interpreter(model_path=model, num_threads=4)
        self.__interpreter.allocate_tensors()

        self.__input_details = self.__interpreter.get_input_details()[0][
            "index"
        ]
        self.__output_details = self.__interpreter.get_output_details()[0][
            "index"
        ]

    def process_image(self, image_file: str):
        original_image = cv2.imread(image_file)
        height = original_image.shape[0]
        width = original_image.shape[1]

        image = cv2.resize(original_image, (256, 144))
        image = np.asarray(image)
        image = image / 255.0
        image = image.astype(np.float32)
        image = image[np.newaxis, :, :, :]

        self.__interpreter.set_tensor(self.__input_details, image)
        self.__interpreter.invoke()
        output = self.__interpreter.get_tensor(self.__output_details)

        foreground = output[0][:, :, 0]
        background = output[0][:, :, 1]

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

        masked_foreground = cv2.addWeighted(
            original_image, 0.9, final_mask, 0.4, 0
        )

        cv2.imshow(image_file, masked_foreground)
        cv2.waitKey(0)

        cv2.destroyAllWindows()
