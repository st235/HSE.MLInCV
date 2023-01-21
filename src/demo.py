import cv2
import numpy as np
from tensorflow.lite.python.interpreter import Interpreter

from src.models.loaders import get_tensorflow_model_file
from src.utils.args_parser import create_parser_for_cli, FLAG_NO_FLAG


def process_image(image_file: str):
    original_image = cv2.imread(image_file)
    height = original_image.shape[0]
    width = original_image.shape[1]

    image = cv2.resize(original_image, (256, 144))
    image = np.asarray(image)
    image = image / 255.
    image = image.astype(np.float32)
    image = image[np.newaxis, :, :, :]

    interpreter = Interpreter(model_path=get_tensorflow_model_file(), num_threads=4)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()[0]['index']
    output_details = interpreter.get_output_details()[0]['index']

    interpreter.set_tensor(input_details, image)
    interpreter.invoke()
    output = interpreter.get_tensor(output_details)

    foreground = output[0][:, :, 0]
    background = output[0][:, :, 1]

    foreground_inverted = np.invert((foreground > 0.5) * 255)
    background_inverted = np.invert((background > 0.5) * 255)

    foreground_resized = cv2.resize(np.uint8(foreground_inverted), (width, height))
    background_resized = cv2.resize(np.uint8(background_inverted), (width, height))

    final_mask = cv2.ximgproc.jointBilateralFilter(background_resized, foreground_resized, 8, 75, 75)
    final_mask = cv2.cvtColor(final_mask, cv2.COLOR_GRAY2RGB)

    masked_foreground = cv2.addWeighted(original_image, 0.9, final_mask, 0.4, 0)

    cv2.imshow(image_file, masked_foreground)
    cv2.waitKey(0)

    cv2.destroyAllWindows()


def main():
    args_parser = create_parser_for_cli()
    image_file = args_parser.get_string(FLAG_NO_FLAG)
    process_image(image_file)


if __name__ == "__main__":
    main()
