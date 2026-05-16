## visualisation.py
# author: Barbara Klimek
# This class handles:
# - show 54th sorted slice
# - create matplotlib figure
# -  show slice slider
## - update image when slider changes

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


#TODO 1: visualize the 54th slice image after sorting from the volume numpy array
# in a figure with matplotlib

def visualize_54th_slice(volume3D, slice_index, ax):
    image_plot = ax.imshow(
        volume3D[:, :, slice_index],
        cmap="gray"
    )
    ax.set_title("54th sorted slice")
    return image_plot


#TODO 2: implement a slider to select the image slice of interest to be visualized in a separate figure
# take a look at matplotlib’s documentation and slider examples in the documentation

# TODO detailed:
#  use separate axes inside the figure:
#  - one axis for image visualization
#  - one axis for the slider

def show_slice_slider(volume3D, slice_index, figure, ax_image):

    number_of_slices = volume3D.shape[2]     # get number of slices from z-direction

    # based on the matplotlib slider documentation example:
    # - create image visualization
    # - create additional space for slider
    # - create slider axis
    # - create slider widget

    image_plot = visualize_54th_slice(
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


# TODO detailed:
#  make the slider update the visualized slice image
#  when slider value changes using on_changed()

    def update_slice(selected_value):

        slice_index = int(selected_value)

        image_plot.set_data(
            volume3D[:, :, slice_index]
        )

        figure.canvas.draw_idle()            # redraw figure after image update

    slice_slider.on_changed(update_slice)

    return image_plot, slice_slider