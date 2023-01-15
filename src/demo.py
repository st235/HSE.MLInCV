import cv2
import numpy as np
from tensorflow.lite.python.interpreter import Interpreter

from models.loaders import get_tensorflow_model_file
from utils.args_parser import create_parser_for_cli, FLAG_NO_FLAG


def process_image(image_file: str):
    img = cv2.imread(image_file)
    h = img.shape[0]
    w = img.shape[1]

    img = cv2.resize(img, (256, 144))
    img = np.asarray(img)
    img = img / 255.
    img = img.astype(np.float32)
    img = img[np.newaxis, :, :, :]

    # Tensorflow Lite

    interpreter = Interpreter(model_path=get_tensorflow_model_file(), num_threads=4)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()[0]['index']
    output_details = interpreter.get_output_details()[0]['index']

    interpreter.set_tensor(input_details, img)
    interpreter.invoke()
    output = interpreter.get_tensor(output_details)

    print(output.shape)
    out1 = output[0][:, :, 0]
    out2 = output[0][:, :, 1]

    out1 = np.invert((out1 > 0.5) * 255)
    out2 = np.invert((out2 > 0.5) * 255)

    print('out1:', out1.shape)
    print('out2:', out2.shape)

    out1 = cv2.resize(np.uint8(out1), (w, h))
    out2 = cv2.resize(np.uint8(out2), (w, h))

    cv2.imwrite('out1.jpg', out1)
    cv2.imwrite('out2.jpg', out2)

    out3 = cv2.ximgproc.jointBilateralFilter(out2, out1, 8, 75, 75)

    cv2.imwrite('out3.jpg', out3)


def main():
    args_parser = create_parser_for_cli()
    image_file = args_parser.get_string(FLAG_NO_FLAG)
    process_image(image_file)


if __name__ == "__main__":
    main()
