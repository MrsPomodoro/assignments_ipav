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


# TODO: after the slider for selecting the active image slice is working, try to implement a windowing ITF specified by the windowing parameters center and width:
#  - implement 2 additional sliders for specifying the windowing ITF (parameters: center, width), apply the windowing ITF on the current slice before visualizing
#  (really create a new image with the mapped intensities in this step) make sure the width is limited to the range from 10 to 85
#  - make sure the visualization updates correctly when changing a windowing ITF parameter



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

    left = center - width // 2                        # calculate left and right window boundary
    right = center + (width - width // 2)

    leftClamped = max(0, left)                        # clamp boundaries into valid range
    rightClamped = min(maxValue, right)

    itf[0:left] = 0                                   # values smaller than left boundary become black
    itf[right:] = maxValue                            # values larger than right boundary become white

    wholeWidth = right - left + 1                     # calculate width of visible interval
    intensityValueLeft = (leftClamped - left) / wholeWidth               # normalize left boundary
    intensityValueRight = 1 - ((right - rightClamped) / wholeWidth)      # normalize right boundary

    values = np.linspace(                             #  linear mapping values
        intensityValueLeft,
        intensityValueRight,
        rightClamped - leftClamped + 1
    ) * maxValue

    itf[leftClamped:rightClamped + 1] = np.round(values)   # store mapped values into ITF

    return itf


# TODO:
# implement sliders for center and width
#
# Goal:
# - visualize selected slice
# - update image after slider changes
# - apply windowing ITF before visualization

def show_windowing(volume3D):

    slice_index = 53    #  start visualization with the 54th slice

# check mn, max to be able to setup windowing parameters
    print(volume3D.min())
    print(volume3D.max())

    current_slice = volume3D[:, :, slice_index]

    max_intensity = int(np.max(volume3D))         # get maximum intensity from DICOM volume
    min_intensity = int(np.min(volume3D))         # get min intensity from DICOM volume


    center = (min_intensity + max_intensity) // 2
    width = max_intensity - min_intensity

    itf = windowing_itf(                          # create ITF based exersice06
        range(0, max_intensity + 1),
        center,
        width
    )
    current_slice = np.clip(current_slice, 0, max_intensity)
    mapped_image = itf[current_slice]              # map original slice intensities with ITF
    figure, ax_image = plt.subplots()              # create matplotlib figure

    plt.subplots_adjust(bottom=0.35)                          # create free space for sliders
    ax_center_slider = plt.axes((0.2, 0.15, 0.6, 0.03))       # create axes for sliders
    ax_width_slider = plt.axes((0.2, 0.08, 0.6, 0.03))
    ax_slice_slider = plt.axes((0.2, 0.01, 0.6, 0.03))

    center_slider = Slider(                                  # create center slider
        ax=ax_center_slider,
        label="Center",
        valmin=0,
        valmax=max_intensity,
        valinit=center,
        valstep=1
    )

    # create width slider - assignment says width must be between 10 and 85

    width_slider = Slider(
        ax=ax_width_slider,
        label="Width",
        valmin=10,
        valmax=85,
        valinit=width,
        valstep=1
    )

    slice_slider = Slider(
        ax=ax_slice_slider,
        label="Slice",
        valmin=0,
        valmax=volume3D.shape[2] - 1,
        valinit=0,
        valstep=1
    )
    # display mapped image
    image_plot = ax_image.imshow( mapped_image.astype(np.uint8),  cmap="gray" )

    ax_image.set_title("Windowing ITF visualization")


# TODO:
# update image after slider changes
#
# Goal:
# - get actual slider values
# - create updated ITF
# - map image again
# - update visualization

    def update_windowing(selected_value):
        current_center = int(center_slider.val)                     # get actual slider values
        current_width = int(width_slider.val)
        current_slice_index = int(slice_slider.val)
        current_slice = volume3D[:, :, current_slice_index]               # get current slice
        updated_itf = windowing_itf(                                # create updated ITF
            range(0, max_intensity + 1),
            current_center,
            current_width
        )

        updated_image = updated_itf[current_slice]                  # map slice intensities with updated ITF
        image_plot.set_data(updated_image.astype(np.uint8))         # update image visualization


        # TODO:
        # - If you strive for full assignment points make sure the slice order in the volume is correct
        # and changing the ROI or a slider behaves correctly and updates the visualization correctly:
        # ensure that whenever a slider is changed the title of the figure is updated with information
        # which slider was updated – it is important that it is stated which slider caused the update

        ax_image.set_title(                                         # update figure title
            f"Center slider updated | Center: "
            f"{current_center} Width: {current_width}"
        )

        figure.canvas.draw_idle()                                   # redraw figure

    center_slider.on_changed(update_windowing)                     # connect sliders with callback function
    width_slider.on_changed(update_windowing)
    slice_slider.on_changed(update_windowing)


    #### roi_selection #####

    # TODO: also implement an interactive rectangular region of interest (ROI) selection
    # (search docs for RectangleSelector)
    # to allow the user to select a ROI, determine the min and max intensity value
    # inside the ROI for the currently selected slice and derive the ITF parameters
    # (center and width) from it.


    # based on older matplotlib RectangleSelector example documentation:
    # https://matplotlib.org/3.1.3/gallery/widgets/rectangle_selector.html
    #
    # based on the example:
    # - use RectangleSelector callback function
    # - use mouse click start and end coordinates
    # - use RectangleSelector on image axis

    def select_roi(eclick, erelease):

        # based on older matplotlib RectangleSelector example documentation:
        # use mouse click start and end coordinates

        x1 = int(eclick.xdata)
        y1 = int(eclick.ydata)

        x2 = int(erelease.xdata)
        y2 = int(erelease.ydata)


        # get current slice from 3D volume
        current_slice = volume3D[:, :, slice_index]


        # based on exercise02 linear indexing:
        # use numpy image indexing to extract ROI from current slice

        roi = current_slice[y1:y2, x1:x2]


        # based on exercise07 histogram equalization:
        # use min() and max() intensity calculation on image region

        roi_min = roi.min()
        roi_max = roi.max()

        print("ROI min intensity:", roi_min)
        print("ROI max intensity:", roi_max)


        # derive ITF parameters from ROI
        roi_center = (roi_min + roi_max) // 2
        roi_width = roi_max - roi_min


        # TODO 2 detailed:
        # changing the slider for the selected slice should update the visualized slice
        # taking into account the currently selected windowing ITF
        #
        # - changing one of the sliders for the windowing ITF parameters
        # should update the visualization
        # (by mapping the original slice with the current specified ITF)
        #
        # - selecting a ROI should update the slider values
        # and also update the visualization accordingly
        #
        # based on matplotlib Slider.set_val():
        # changing slider values automatically triggers update_windowing()

        center_slider.set_val(roi_center)
        width_slider.set_val(roi_width)


    # based on older matplotlib RectangleSelector example documentation:
    # https://matplotlib.org/3.1.3/gallery/widgets/rectangle_selector.html
    #
    # activate interactive ROI selection on image axis

    rectangle_selector = RectangleSelector(
        ax_image,
        select_roi,
        useblit=True,
        interactive=True
    )

    plt.show()