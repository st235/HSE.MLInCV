"""Module for image processing commands, like, segmentation."""

import cv2

from src.default.loader import get_sample_image
from src.models.loaders import get_tensorflow_model_file
from src.utils.args_parser import create_parser_for_cli, FLAG_NO_FLAG

from src.human_segmentation_engine import HumanSegmentationEngine


def main():
    """Entry point to the process command."""
    args_parser = create_parser_for_cli()
    image_file = get_sample_image()

    if not args_parser.is_empty():
        image_file = args_parser.get_string(FLAG_NO_FLAG)

    segmentation_engine = HumanSegmentationEngine.create(get_tensorflow_model_file())

    original_image = cv2.imread(image_file)
    masked_foreground = segmentation_engine.perform_segmentation(original_image)

    masked_foreground = cv2.addWeighted(
        original_image, 0.9, masked_foreground, 0.4, 0
    )

    cv2.imshow(image_file, masked_foreground)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
