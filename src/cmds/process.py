from src.default.loader import get_sample_image
from src.models.loaders import get_tensorflow_model_file
from src.utils.args_parser import create_parser_for_cli, FLAG_NO_FLAG

from src.image_processor import ImageProcessor


def main():
    args_parser = create_parser_for_cli()
    image_file = get_sample_image()

    if not args_parser.is_empty():
        image_file = args_parser.get_string(FLAG_NO_FLAG)

    processor = ImageProcessor(get_tensorflow_model_file())
    processor.process_image(image_file)


if __name__ == "__main__":
    main()
