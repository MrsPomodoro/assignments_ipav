#################################
# TODO ASSIGNMENT PART 1:
# - prepare a 3D numpy array as array of zeros to store the volume intensities, use the same datatype as it is used in the input dicom files, 
#   volume dimensions should be the slice shape in x-,y- direction and number of slices in z-direction so that every input slice can 
#   go into its correct position
# - the list of individual slice images is mixed-up, therefore loop over all datasets:
#      - determine the correct slice index from dicom metadata
#      - the class pydicom.dataset.FileDataset is the same class we already encountered in the pydicom-example from the lecture,
#        so you should know how to access the pixel data and DICOM attributes (you learned how to obtain DICOM attributes as type
#        pydicom.dataelem.DataElement, use the ‘.value’ attribute to get just the value)
#      - store the individual slice in the correct position in the volume
#################################

# load_dicom_volume.py
# author: Barbara Klimek
# This class handles:
# - loading DICOM files
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

#  preparation of an empty 3D numpy array for the DICOM volume.
#  Goal:
#   -  set up volume dimensions: slice shape in x-,y- direction and number of slices in z-direction

def prepare_empty_volume(rows, columns, number_of_slices, datatype):
    volume = np.zeros((rows, columns, number_of_slices), dtype=datatype)
    return volume

## fill the 3D volume with sorted DICOM slices.
#  Goal:
#   - get correct slice index from DICOM metadata
#   - to ensure homogenization of the volume, every slice is placed into its correct z-position
#   - the result is a correctly ordered 3D numpy array
def sort_and_fill_volume(datasets, volume3D):

    for dataset in datasets:
        slice_index = int(dataset[0x0020, 0x0013].value)          # get slice index from DICOM metadata
        volume3D[:, :, slice_index] = dataset.pixel_array         # copy pixel data into correct position in 3D volume

    return volume3D

