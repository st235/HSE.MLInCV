"""Module for different tensorflow interpreters."""

try:
    from tensorflow.lite.python.interpreter import Interpreter
except ImportError:
    from tflite_runtime.interpreter import Interpreter


# pylint: disable=R0903
# Class has enough public methods.
class ImageInterpreter:
    """Abstracts different tensorflow interpreters.

    Use interpreter from tensorflow if found, otherwise
    falls back to tensorflow runtime.
    """

    def __init__(self, model_path: str):
        self.__interpreter = Interpreter(model_path=model_path, num_threads=4)
        self.__interpreter.allocate_tensors()

        self.__input_details = self.__interpreter.get_input_details()[0][
            "index"
        ]
        self.__output_details = self.__interpreter.get_output_details()[0][
            "index"
        ]

    def segment_layers(self, image):
        """Segments background from foreground of the given image.

        Returns a tuple of 2 weighted masks:
        one for foreground and another for background.
        """
        self.__interpreter.set_tensor(self.__input_details, image)
        self.__interpreter.invoke()
        output = self.__interpreter.get_tensor(self.__output_details)

        foreground = output[0][:, :, 0]
        background = output[0][:, :, 1]

        return foreground, background
