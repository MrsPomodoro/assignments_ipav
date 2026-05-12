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

def Visualize_54th_slice(volume3D, slice_index, ax):
    ax.imshow(volume3D[:, :, slice_index], cmap="gray")
    ax.set_title("54th sorted slice")

#TODO 2: implement a slider to select the image slice of interest to be visualized in a separate figure
# take a look at matplotlib’s documentation and slider examples in the documentation

# TODO detailed:
#  use separate axes inside the figure: use one axis for the slider, and one axis for plotting the image
#  (read about axes in the documentation if you are unfamiliar with this concept)

def show_slice_slider(volume3D, slice_index):

    number_of_slices = volume3D.shape[2]     # get the number of slices from the 3D volume - the third dimension represents the z-direction / slice direction

    # based on the matplotlib slider documentation example I created :
    #  - a figure and separate axis for the image visualization
    #  - additional free space at the bottom of the figure for the slider widget
    #  - a separate axis object for the slider [left, bottom, width, height]
    #  - the slider widget

    figure, ax_image = plt.subplots()
    Visualize_54th_slice(volume3D, slice_index, ax_image)

    plt.subplots_adjust(bottom=0.25)
    ax_slider = plt.axes((0.2, 0.1, 0.6, 0.03))
    slice_slider = Slider(
        ax=ax_slider,
        label="Slice",
        valmin=0,                            # first possible slice index in the volume
        valmax=number_of_slices - 1,         # last possible slice index in the volume
        valinit=slice_index,
        valstep=1
    )


# TODO detailed:
#  make the slider update the visualized slice image in the figure on a slider value change: use the on_changed() callback function mechanism by registering an own callback function to it (with the slice number being the only parameter)
#  and use it to update the visualized image. Update the image either by redrawing it to the correct axis, or better,
#  by drawing the default slice image initially with the imshow() function, and updating the image data of the matplotlib.image.
#  AxesImage object (the return value of the imshow() function) with the set_data() function providing the selected slice image from the volume

    image_plot = ax_image.images[0]

    def update_slice(selected_value):
        slice_index = int(selected_value)                 # slider returns float values -> convert to integer slice index
        image_plot.set_data(volume3D[:, :, slice_index])  # update image data with set_data()
        figure.canvas.draw_idle()                         # based on the documentation example -> redraw the figure after updating the image

    slice_slider.on_changed(update_slice)                 # connect the slider with the callback function and on_changed()

    plt.show()  # show the interactive figure