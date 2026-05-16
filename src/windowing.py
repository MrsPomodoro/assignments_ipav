# windowing.py
# author: Barbara Klimek
# This class handles:
# - map original image intensities into visible grayscale range
# - windowing intensity transfer function (ITF)
# - center slider
# - width slider
# - updating image after changing windowing parameters
# - RectangleSelector ROI selection
# - ROI based ITF update

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RectangleSelector
from visualisation import show_slice_slider


# TODO: after the slider for selecting the active image slice is working,
# try to implement a windowing ITF specified by the windowing parameters center and width:
#
# - implement 2 additional sliders for specifying the windowing ITF
#   (parameters: center, width)
#
# - apply the windowing ITF on the current slice before visualizing
#
# - make sure the width is limited to the range from 10 to 85
#
# - make sure the visualization updates correctly
#   when changing a windowing ITF parameter


## 1. Prepare function for applying windowing ITF
# Goal:
# - calculate lower and upper intensity range
# - clip intensity values outside the range

# based on exercise06 from the lecture:
# def windowing_itf(inputValueRange, center, width):
#     numValues = len(inputValueRange)
#     maxValue = numValues - 1
#     itf = np.zeros(numValues)
#     left = center - width // 2
#     right = center + (width - width // 2)

def windowing_itf(inputValueRange, center, width):

    numValues = len(inputValueRange)                  # get number of intensity values
    maxValue = numValues - 1                          # determine maximum intensity value

    itf = np.zeros(numValues)                         # create empty ITF array

    left = center - width // 2                        # calculate left window boundary
    right = center + (width - width // 2)             # calculate right window boundary

    leftClamped = max(0, left)                        # clamp left boundary
    rightClamped = min(maxValue, right)               # clamp right boundary

    itf[0:left] = 0                                   # values below window become black
    itf[right:] = maxValue                            # values above window become white

    wholeWidth = right - left + 1                     # calculate visible width interval

    intensityValueLeft = (
        leftClamped - left
    ) / wholeWidth

    intensityValueRight = (
        1 - ((right - rightClamped) / wholeWidth)
    )

    values = np.linspace(
        intensityValueLeft,
        intensityValueRight,
        rightClamped - leftClamped + 1
    ) * maxValue

    itf[leftClamped:rightClamped + 1] = np.round(values)

    return itf


# TODO:
# implement sliders for center and width
#
# Goal:
# - visualize selected slice
# - update image after slider changes
# - apply windowing ITF before visualization

def show_windowing(volume3D):

    slice_index = 53    # start visualization with the 54th slice

    # check min and max intensity values

    print(volume3D.min())
    print(volume3D.max())

    current_slice = volume3D[:, :, slice_index]

    max_intensity = int(np.max(volume3D))             # get maximum intensity value
    min_intensity = int(np.min(volume3D))             # get minimum intensity value

    center = (min_intensity + max_intensity) // 2
    width = max_intensity - min_intensity

    # create ITF

    itf = windowing_itf(
        range(0, max_intensity + 1),
        center,
        width
    )

    current_slice = np.clip(
        current_slice,
        0,
        max_intensity
    )

    mapped_image = itf[current_slice]                 # map original slice with ITF

    # create matplotlib figure

    figure, ax_image = plt.subplots()

    image_plot, slice_slider = show_slice_slider(
        volume3D,
        slice_index,
        figure,
        ax_image
    )

    image_plot.set_data(
        mapped_image.astype(np.uint8)
    )

    # create free space for sliders

    plt.subplots_adjust(bottom=0.3)

    # create slider axes

    ax_center_slider = plt.axes((0.2, 0.20, 0.6, 0.03))
    ax_width_slider = plt.axes((0.2, 0.12, 0.6, 0.03))

    # create center slider

    center_slider = Slider(
        ax=ax_center_slider,
        label="Center",
        valmin=0,
        valmax=max_intensity,
        valinit=center,
        valstep=1
    )

    # create width slider
    # assignment says width must be between 10 and 85

    width_slider = Slider(
        ax=ax_width_slider,
        label="Width",
        valmin=10,
        valmax=85,
        valinit=width,
        valstep=1
    )

    ax_image.set_title("Windowing ITF visualization")


# TODO:
# update image after slider changes
#
# Goal:
# - get actual slider values
# - create updated ITF
# - map image again
# - update visualization and title

    changed_slider = ["Slice"]   #variable for the slider to know, which was changed and show it in the title

    def update_windowing(selected_value):

        current_center = int(center_slider.val)
        current_width = int(width_slider.val)
        current_slice_index = int(slice_slider.val)

        current_slice = volume3D[:, :, current_slice_index]

        updated_itf = windowing_itf(
            range(0, max_intensity + 1),
            current_center,
            current_width
        )

        updated_image = updated_itf[current_slice]

        image_plot.set_data(
            updated_image.astype(np.uint8)
        )

        # TODO:
        # ensure that whenever a slider is changed
        # the figure title is updated with information
        # which slider caused the update

        ax_image.set_title(
            f"{changed_slider[0]} slider updated | "
            f"Slice: {current_slice_index} | "
            f"Center: {current_center} | "
            f"Width: {current_width}"
        )

        figure.canvas.draw_idle()

    # connect sliders with callback function

    def on_center(val):
        changed_slider[0] = "Center"
        update_windowing(val)

    def on_width(val):
        changed_slider[0] = "Width"
        update_windowing(val)

    def on_slice(val):
        changed_slider[0] = "Slice"
        update_windowing(val)

    center_slider.on_changed(on_center)
    width_slider.on_changed(on_width)
    slice_slider.on_changed(on_slice)


    #### roi_selection #####

    # TODO:
    # implement interactive rectangular ROI selection
    #
    # determine:
    # - min ROI intensity
    # - max ROI intensity
    #
    # derive:
    # - center
    # - width
    #
    # update sliders and visualization

    # based on older matplotlib RectangleSelector example documentation:
    # https://matplotlib.org/3.1.3/gallery/widgets/rectangle_selector.html

    def select_roi(eclick, erelease):

        # get mouse click coordinates

        x1 = int(eclick.xdata)
        y1 = int(eclick.ydata)

        x2 = int(erelease.xdata)
        y2 = int(erelease.ydata)

        # get current slice

        current_slice = volume3D[:, :, int(slice_slider.val)]

        # extract ROI

        roi = current_slice[y1:y2, x1:x2]

        # calculate ROI intensity range

        roi_min = roi.min()
        roi_max = roi.max()

        print("ROI min intensity:", roi_min)
        print("ROI max intensity:", roi_max)

        # derive ITF parameters

        roi_center = (roi_min + roi_max) // 2
        roi_width = roi_max - roi_min

        # TODO:
        # changing slider values automatically
        # triggers update_windowing()

        center_slider.set_val(roi_center)
        width_slider.set_val(roi_width)

    # activate RectangleSelector

    rectangle_selector = RectangleSelector(
        ax_image,
        select_roi,
        useblit=True,
        interactive=True
    )

    plt.show()