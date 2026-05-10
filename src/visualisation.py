# visualisation.py
# author: Barbara Klimek
# This class handles:
# - show 54th sorted slice
# - create matplotlib figure
# -  show slice slider
# - update image when slider changes

import numpy as np
import pydicom
import matplotlib.pyplot as plt
import glob

#TODO: visualize the 54th slice image after sorting from the volume numpy array
# in a figure with matplotlib

def show_54th_slice(volume3D):   # I used the function as we did in excersice04
    plt.figure()
    plt.imshow(volume3D[:, :, 53], cmap="gray")
    plt.title("54th sorted slice")
    plt.show()

#TODO: implement a slider to select the image slice of interest to be visualized in a separate figure
# take a look at matplotlib’s documentation and slider examples in the documentation
# use separate axes inside the figure: use one axis for the slider, and one axis for plotting the image (read about axes in the documentation if you are unfamiliar with this concept)
# make the slider update the visualized slice image in the figure on a slider value change: use the on_changed() callback function mechanism by registering an own callback function to it (with the slice number being the only parameter) and use it to update the visualized image. Update the image either by redrawing it to the correct axis, or better, by drawing the default slice image initially with the imshow() function, and updating the image data of the matplotlib.image.AxesImage object (the return value of the imshow() function) with the set_data() function providing the selected slice image from the volume


