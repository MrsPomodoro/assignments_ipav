#################################
# TODO ASSIGNMENT PART 3:
# - after the slider for selecting the active image slice is working, try to implement a windowing ITF specified by the windowing parameters center and width:
#       - implement 2 additional sliders for specifying the windowing ITF (parameters: center, width), apply the windowing ITF on the current slice before 
#         visualizing (really create a new image with the mapped intensities in this step) make sure the width is limited to the range from 10 to 85
#       - make sure the visualization updates correctly when changing a windowing ITF parameter
# - also implement an interactive rectangular region of interest (ROI) selection (search docs for RectangleSelector) to allow the user to select a ROI, 
#   determine the min and max intensity value inside the ROI for the currently selected slice and derive the ITF parameters (center and width) from it.
# - If you strive for full assignment points make sure the slice order in the volume is correct and changing the ROI or a slider behaves correctly 
#   and updates the visualization correctly: ensure that whenever a slider is changed the title of the figure is updated with information which 
#   slider was updated – it is important that it is stated which slider caused the update
#       - changing the slider for the selected slice should update the visualized slice taking into account the currently selected windowing ITF
#       - changing one of the sliders for the windowing ITF parameters should update the visualization (by mapping the original slice with the current specified ITF)
#       - selecting a ROI should update the slider values and also update the visualization accordingly
#################################

# windowing.py
# author: Barbara Klimek
# This class handles:
# - windowing intensity transfer function (ITF)
# - center and width sliders
# - updating image after changing windowing parameters
# - RectangleSelector ROI selection
# - ROI based ITF parameter update

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RectangleSelector
from visualisation import show_slice_slider

#  windowing ITF function - implementation based on exercise06 from the lecture
#  Goal:
#   - calculate lower and upper intensity range
#   - clip intensity values outside the range
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

    intensityValueLeft = (                            # calculate start intensity value within window
        leftClamped - left
    ) / wholeWidth

    intensityValueRight = (
        1 - ((right - rightClamped) / wholeWidth)     # calculate end intensity value within window
    )

    values = np.linspace(                             # fill window range with values going from dark to bright
        intensityValueLeft,
        intensityValueRight,
        rightClamped - leftClamped + 1
    ) * maxValue

    itf[leftClamped:rightClamped + 1] = np.round(values) # fill ITF with rounded intensity values

    return itf


#  visualization function for windowing ITF
#  Goal:
#   - visualize selected slice with windowing ITF applied
#   - center and width sliders allow to adjust the ITF parameters
#   - ROI selection derives ITF parameters from selected region
def show_windowing(volume3D):

    slice_index = 53                                 # start visualization with the 54th slice

    print(volume3D.min())                            # check min and max intensity values
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

    current_slice = np.clip(                         # make sure all values stay between 0 and max_intensity
        current_slice,
        0,
        max_intensity
    )

    mapped_image = itf[current_slice]                 # map original slice with ITF

    # create matplotlib figure
    figure, ax_image = plt.subplots()

    image_plot, slice_slider = show_slice_slider(
        volume3D,
        slice_index + 1,                             # +1 because Python indexing starts at 0, so slice 53 = 54th slice
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

    ax_image.set_title("Windowing ITF visualization | default slice: 54")

#  callback function - called when any slider is changed
#  Goal:
#    - get current slider values
#    - create updated ITF based on new values
#    - apply ITF on current slice and update visualization
#    - update figure title with which slider was changed

    changed_slider = ["Slice"]   #variable for the slider to know, which was changed and show it in the title

    def update_windowing(selected_value):
        current_center = int(center_slider.val)          # get current center slider value
        current_width = int(width_slider.val)            # get current width slider value
        current_slice_index = int(slice_slider.val)      # get current slice slider value

        current_slice = volume3D[:, :, current_slice_index]   # get current slice from volume

        updated_itf = windowing_itf(                     # create updated ITF with current slider values
            range(0, max_intensity + 1),
            current_center,
            current_width
        )                                               

        updated_image = updated_itf[current_slice]       # apply ITF on current slice

        image_plot.set_data(                             # update image with mapped intensities
            updated_image.astype(np.uint8)
        )                                                

        # ensure that whenever a slider is changed the figure title is updated with information which slider caused the update
        ax_image.set_title(
            f"{changed_slider[0]} slider updated | "
            f"Slice: {current_slice_index} | "
            f"Center: {current_center} | "
            f"Width: {current_width}"
        )

        figure.canvas.draw_idle()


    # helper callbacks to track which slider was changed before calling update_windowing
    def on_center(val):
        changed_slider[0] = "Center"
        update_windowing(val)

    def on_width(val):
        changed_slider[0] = "Width"
        update_windowing(val)

    def on_slice(val):
        changed_slider[0] = "Slice"
        update_windowing(val)

    # connect sliders with callback function
    center_slider.on_changed(on_center)
    width_slider.on_changed(on_width)
    slice_slider.on_changed(on_slice)


    # ROI selection - user draws a rectangle on the image
    #  Goal:
    #  - determine min and max intensity inside selected ROI
    #  - derive center and width ITF parameters from ROI
    #  - update sliders and visualization accordingly
    #    based on matplotlib RectangleSelector documentation: https://matplotlib.org/3.1.3/gallery/widgets/rectangle_selector.html 
    def select_roi(eclick, erelease):

        # get mouse click coordinates
        x1 = int(eclick.xdata)
        y1 = int(eclick.ydata)
        x2 = int(erelease.xdata)
        y2 = int(erelease.ydata)
    
        current_slice = volume3D[:, :, int(slice_slider.val)]     # get current slice
        roi = current_slice[y1:y2, x1:x2]                         # extract ROI

        # calculate ROI intensity range
        roi_min = roi.min()
        roi_max = roi.max()

        #check log
        print("ROI min intensity:", roi_min)
        print("ROI max intensity:", roi_max)

        roi_center = (int(roi_min) + int(roi_max)) // 2         # calculate center from ROI intensity range
        roi_width = int(roi_max) - int(roi_min)                 # calculate width from ROI intensity range

        # setting slider values automatically triggers update_windowing()
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