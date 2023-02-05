"""Web demo: shows usage examples of the library. Using streamlit."""

import cv2
import numpy as np
import streamlit as st

from src.human_segmentation_engine import HumanSegmentationEngine


def read_bytestream_as_image(streamlit_file):
    """Reads image from bytestream.

    Converts streamlit bytestream from a file uploader to
    numpy array. Uses opencv to perform the conversion.
    Returns an RGB image as a numpy array.
    """
    bytes_data = streamlit_file.getvalue()
    cv2_image = cv2.imdecode(
        np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR
    )
    return cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)


def replace_background(foreground_image, background_image, mask):
    """ "Replaces image's background with another image.

    Extracts foreground from foreground_image using the given mask
    then puts it on the background_image.
    Returns a tuple of cropped background and a merged image.
    """
    _, bitmask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
    bitmask = cv2.cvtColor(bitmask, cv2.COLOR_RGB2GRAY)

    foreground = cv2.bitwise_and(
        foreground_image, foreground_image, mask=bitmask
    )

    desired_width = int(foreground_image.shape[1])
    desired_height = int(
        background_image.shape[0]
        * (foreground_image.shape[1] / background_image.shape[1])
    )

    # If width scaling resulted in a smaller image
    # Let's additionally scale it to make height equal
    # to the original image's height
    if desired_height < foreground_image.shape[0]:
        desired_width = int(
            desired_width * (foreground_image.shape[0] / desired_height)
        )
        desired_height = int(foreground_image.shape[0])

    desired_dimensions = (desired_width, desired_height)

    resized_background = cv2.resize(
        background_image, desired_dimensions, interpolation=cv2.INTER_AREA
    )

    leftover_width = resized_background.shape[1] - foreground_image.shape[1]
    leftover_height = resized_background.shape[0] - foreground_image.shape[0]

    cropped_background = resized_background[
        leftover_height : leftover_height + foreground_image.shape[0],
        leftover_width : leftover_width + foreground_image.shape[1],
    ]

    inverted_mask = cv2.bitwise_not(bitmask)

    background = cv2.bitwise_and(
        cropped_background, cropped_background, mask=inverted_mask
    )

    return cropped_background, cv2.bitwise_or(foreground, background)


segmentation_engine = HumanSegmentationEngine.create()

st.title("Human segmentation")
st.caption(
    "A lightweight model to segment the prominent "
    "humans in the scene in videos captured by a smartphone or "
    "web camera. Runs in real-time (~120 FPS) on a laptop CPU via XNNPack TFLite backend."
)

# Pylint 'invalid-name' check has been disabled as the name
# is just right. Pylint thinks that these fields are constants,
# therefore wants to rename them.

# Original image to process.
# Can be any image with a human on it.
# pylint: disable=invalid-name
original_image = None

# Optional background overlay.
# Can be used to provide custom background, like in zoom calls.
# pylint: disable=invalid-name
background_overlay = None

# Final background image: cropped and resized.
# pylint: disable=invalid-name
processed_background = None

local_image_tab, camera_tab = st.tabs(["Local image", "Camera"])

with local_image_tab:
    locally_provided_file = st.file_uploader(
        "Choose an image",
        help="This image will be used for further processing and segmentation.",
        type=["png", "jpg", "jpeg"],
    )
    if locally_provided_file is not None:
        original_image = read_bytestream_as_image(locally_provided_file)

with camera_tab:
    camera_provided_file = st.camera_input("Take a picture")
    if camera_provided_file is not None:
        original_image = read_bytestream_as_image(camera_provided_file)

if original_image is not None:
    background_overlay_file = st.file_uploader(
        "Background overlay",
        help="This image will be used to replace background on "
        "the provided photo, just like Google Meet or Zoom do.",
        type=["png", "jpg", "jpeg"],
    )
    if background_overlay_file is not None:
        background_overlay = read_bytestream_as_image(background_overlay_file)

    foreground_mask = segmentation_engine.perform_segmentation(original_image)

    if background_overlay is not None:
        processed_background, final_image = replace_background(
            original_image, background_overlay, foreground_mask
        )
    else:
        # No background, let's highlight the area then
        final_image = cv2.addWeighted(
            original_image, 0.9, foreground_mask, 0.5, 0
        )

    st.subheader("Result image")
    st.image(final_image)

    _, download_image = cv2.imencode(
        ".png", cv2.cvtColor(final_image, cv2.COLOR_RGB2BGR)
    )
    st.download_button(
        "Download",
        download_image.tobytes(),
        file_name="result.png",
        mime="image/png",
    )

    background_column, original_image_column, mask_column = st.columns(3)

    with background_column:
        st.subheader("Background")
        if processed_background is not None:
            st.image(processed_background)
        else:
            st.image(np.zeros(original_image.shape))

    with original_image_column:
        st.subheader("Original")
        st.image(original_image)

    with mask_column:
        st.subheader("Mask")
        st.image(foreground_mask)
