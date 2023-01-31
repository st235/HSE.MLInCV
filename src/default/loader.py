"""Helpers for samples loading for demo app."""

import os

__CURRENT_FOLDER = os.path.dirname(os.path.realpath(__file__))


def get_sample_image() -> str:
    """Returns default image sample path for human segmentation."""
    return os.path.join(__CURRENT_FOLDER, "sample.jpeg")
