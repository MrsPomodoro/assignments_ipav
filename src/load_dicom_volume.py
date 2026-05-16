# load_dicom_volume.py
#author: Barbara Klimek
# This class handles:
# - loading DICOM files - already done by professor
# - creating 3D numpy volume
# - sorting slices
# - filling the 3D volume

import numpy as np
import pydicom
import glob


# load the DICOM files into list datasets - refactor into helper function
def load_dicom_files(filepath):
    filenames = glob.glob(filepath, recursive=False)
    datasets = []
    for fname in filenames:
        print("loading: {}".format(fname))
        datasets.append(pydicom.dcmread(fname))
    print(len(datasets), ' slices loaded...')
    return datasets



#  I prepared the  function that creates an empty 3D numpy array for the DICOM volume.
#    Goal:
#    -  set up volume dimensions: slice shape in x-,y- direction and number of slices in z-direction

def prepare_empty_volume(rows, columns, number_of_slices, datatype):
    volume = np.zeros((rows, columns, number_of_slices), dtype=datatype)
    return volume


#TODO 2: the list of individual slice images is mixed-up, therefore loop over all datasets:
# determine the correct slice index from dicom metadata
# the class pydicom.dataset.FileDataset is the same class we already encountered in the pydicom-example from the lecture,
# so you should know how to access the pixel data and DICOM attributes (you learned how to obtain DICOM attributes as type
# pydicom.dataelem.DataElement, use the ‘.value’ attribute to get just the value)
# store the individual slice in the correct position in the volume

## Fill the 3D volume with sorted DICOM slices
# Goal:
# - get correct slice index from DICOM metadata
# - copy every slice into correct z-position in the 3D volume

def sort_and_fill_volume(datasets, volume3D):

    for dataset in datasets:
        slice_index = int(dataset[0x0020, 0x0013].value)          # get slice index from DICOM metadata
        volume3D[:, :, slice_index] = dataset.pixel_array         # copy pixel data into correct position in 3D volume

    return volume3D

