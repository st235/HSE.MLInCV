"""Helper functions for trained models loading."""

import os

__CURRENT_FOLDER = os.path.dirname(os.path.realpath(__file__))


def get_tensorflow_model_file() -> str:
    """Returns path to the default Tensorflow segmentation model."""

    return os.path.join(
        __CURRENT_FOLDER, "tensorflow_model_float16_quant.tflite"
    )
