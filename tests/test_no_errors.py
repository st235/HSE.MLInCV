import pytest

from src.human_segmentation_engine import HumanSegmentationEngine


@pytest.mark.load_image("images/sample_small.jpg")
def test_no_errors_while_processing_small_image(image):
    human_segmentation_engine = HumanSegmentationEngine.create()
    human_segmentation_engine.perform_segmentation(image)


@pytest.mark.load_image("images/sample_medium.jpg")
def test_no_errors_while_processing_medium_image(image):
    human_segmentation_engine = HumanSegmentationEngine.create()
    human_segmentation_engine.perform_segmentation(image)


@pytest.mark.load_image("images/sample_large.jpg")
def test_no_errors_while_processing_large_image(image):
    human_segmentation_engine = HumanSegmentationEngine.create()
    human_segmentation_engine.perform_segmentation(image)
