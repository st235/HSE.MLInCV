import pytest

from src.human_segmentation_engine import HumanSegmentationEngine


@pytest.mark.load_image("images/sample_regression.jpeg")
@pytest.mark.image_regression("regression")
def test_no_regression_on_regular_image(image_regression_assertions, image):
    human_segmentation_engine = HumanSegmentationEngine.create()
    segmentation_result = human_segmentation_engine.perform_segmentation(image)
    image_regression_assertions.assert_no_regression(segmentation_result)
