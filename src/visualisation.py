#################################
# TODO ASSIGNMENT PART 2:
#  - visualize the 54th slice image after sorting from the volume numpy array in a figure with matplotlib
#  - implement a slider to select the image slice of interest to be visualized in a separate figure
#  - take a look at matplotlib’s documentation and slider examples in the documentation
#  - use separate axes inside the figure: use one axis for the slider, and one axis for plotting the image
#    (read about axes in the documentation if you are unfamiliar with this concept)
#  - make the slider update the visualized slice image in the figure on a slider value change: use the on_changed()
#    callback function mechanism by registering an own callback function to it (with the slice number being the only 
#    parameter) and use it to update the visualized image. Update the image either by redrawing it to the correct axis,
#    or better, by drawing the default slice image initially with the imshow() function,
# -  and updating the image data of the matplotlib.image.AxesImage object (the return value of the imshow() function) 
#    with the set_data() function providing the selected slice image from the volume
#################################

## visualisation.py
# author: Barbara Klimek
# This class handles:
# - visualize a selected slice from the 3D volume
# - create matplotlib figure
# - show slice slider
# - update image when slider changes

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


# function to visualize any selected slice from the 3D volume
# (formerly visualize_54th_slice - refactored, 54th slice index is defined in windowing.py)
def visualize_selected_slice(volume3D, slice_index, ax):   
    image_plot = ax.imshow(
        volume3D[:, :, slice_index],
        cmap="gray"
    )
    return image_plot


#implementation of a slider to select the image slice of interest to be visualized in a separate figure
def show_slice_slider(volume3D, slice_index, figure, ax_image):

    number_of_slices = volume3D.shape[2]     # get number of slices from z-direction

    # based on the matplotlib slider documentation example:
    # - create image visualization
    # - create additional space for slider
    # - create slider axis
    # - create slider widget

    image_plot = visualize_selected_slice(
        volume3D,
        slice_index,
        ax_image
    )

    plt.subplots_adjust(bottom=0.25)

    ax_slider = plt.axes((0.2, 0.04, 0.6, 0.03))

    slice_slider = Slider(
        ax=ax_slider,
        label="Slice",
        valmin=0,                            # first possible slice index
        valmax=number_of_slices - 1,         # last possible slice index
        valinit=slice_index,
        valstep=1
    )


#  update the visualized slice image when slider value changes using on_changed()
    def update_slice(selected_value):

        slice_index = int(selected_value)

        image_plot.set_data(
            volume3D[:, :, slice_index]
        )

        figure.canvas.draw_idle()            # redraw figure after image update

    slice_slider.on_changed(update_slice)

    return image_plot, slice_slider