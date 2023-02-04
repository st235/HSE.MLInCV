import cv2
import pytest
import os

__OPTION_OVERWRITE_REGRESSION_RESULTS = "--overwrite-regression-result"


def pytest_addoption(parser):
    parser.addoption(
        __OPTION_OVERWRITE_REGRESSION_RESULTS,
        action="store_true",
        default=False,
        help="overwrites regression results and disables assertions.",
    )


class ImageRegressionAssertions:
    def __init__(
        self,
        test_name: str,
        test_file_path: str,
        states_folder_path: str,
        overwrite_regression_mode=False,
    ):
        self.__test_name = test_name
        self.__test_file_path = test_file_path
        self.__states_folder_path = states_folder_path
        self.__overwrite_regression_mode = overwrite_regression_mode

    def assert_no_regression(self, new_state):
        if self.__overwrite_regression_mode:
            self.__state = new_state

        diff = cv2.compare(self.__state, new_state, cv2.CMP_NE)
        diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        assert cv2.countNonZero(diff) == 0

    def __get_state_image_path(self):
        test_file_name = os.path.basename(self.__test_file_path)
        test_file_name = os.path.splitext(test_file_name)[0]

        state_image_name = f"{test_file_name}_{self.__test_name}.png"
        states_directory_path = os.path.dirname(self.__test_file_path)

        if (
            self.__states_folder_path is not None
            and len(self.__states_folder_path) > 0
        ):
            states_directory_path = os.path.join(
                states_directory_path, self.__states_folder_path
            )
            os.makedirs(states_directory_path, exist_ok=True)

        return os.path.join(states_directory_path, state_image_name)

    @property
    def __state(self):
        image = cv2.imread(self.__get_state_image_path())
        if image is None:
            raise FileNotFoundError(
                f"Cannot find file with name {self.__get_state_image_path()}"
            )
        return image

    @__state.setter
    def __state(self, value):
        cv2.imwrite(self.__get_state_image_path(), value)


@pytest.fixture(name="image")
def image(request):
    test_path = request.node.path
    test_dir_path = os.path.dirname(test_path)

    marker = request.node.get_closest_marker("load_image")
    relative_image_path = marker.args[0]

    image_path = os.path.join(test_dir_path, relative_image_path)

    yield cv2.imread(image_path)


@pytest.fixture(name="image_regression_assertions")
def image_regression_assertions(request):
    test_path = request.node.path

    marker = request.node.get_closest_marker("image_regression")
    states_folder_path = marker.args[0]

    overwrite_regression_results = request.config.getoption(
        __OPTION_OVERWRITE_REGRESSION_RESULTS
    )

    yield ImageRegressionAssertions(
        request.node.name,
        test_path,
        states_folder_path,
        overwrite_regression_results,
    )


def pytest_runtest_setup(item):
    overwrite_regression_results = item.config.getoption(
        __OPTION_OVERWRITE_REGRESSION_RESULTS
    )
    marker = item.get_closest_marker("image_regression")

    if overwrite_regression_results and marker is None:
        pytest.skip(f"Skipping {item.name} as not image regression test")
