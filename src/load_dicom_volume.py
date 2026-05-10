# load_dicom_volume.py
#author: Barbara Klimek
# This class handles:
# - loading DICOM files - already done by professor
# - sorting slices
# - creating 3D numpy volume

import numpy as np
import pydicom
import matplotlib.pyplot as plt
import glob

filepath = '../data/Lobus_DICOMs_mixed_up/*.dcm'

# load the DICOM files into list datasets - create helper method
def load_dicom_files(filepath):
    filenames = glob.glob(filepath, recursive=False)
    datasets = []
    for fname in filenames:
        print("loading: {}".format(fname))
        datasets.append(pydicom.dcmread(fname))
    print(len(datasets), ' slices loaded...')
    return datasets

datasets = load_dicom_files(filepath)

# TODO: prepare a 3D numpy array as array of zeros to store the volume intensities,
#  use the same datatype as it is used in the input dicom files, volume dimensions
#  should be the slice shape in x-,y- direction and number of slices in z-direction
#  so that every input slice can go into its correct position

##My solution:

## 1. I explored the loaded DICOM datasets before processing
#  Goal:
# - understand the basic structure of the datasets
# - explore important DICOM metadata
# - identify how the slice order is stored
# - find the DICOM tag for Instance Number
##

print(datasets)  # I found tag for Instance Number (0020,0013)
for dataset in datasets:
    slice_index = dataset[0x0020, 0x0013].value
    print(slice_index)    # check the order of the slice via loop of InstanceNumbers

## 2. I explored the shape and datatype of existing slides to be able to create 3D array
#   Goal:
#   - get the shape (rows and columns) and datatype of one DICOM slice
#   - this is needed to create a new 3D volume with the same properties

# check first DICOM slice
first_dataset = datasets[0]               ##   - used .shape and .dtype  numpy functions exactly as in example03
first_slice = first_dataset.pixel_array   ##   - used .pixel_array  numpy functions exactly as in example04

print("First slice shape:", first_slice.shape)
print("First slice datatype:", first_slice.dtype)
print("Number of slices:", len(datasets))

#define rows, columns and number of slices
rows = first_slice.shape[0]
columns = first_slice.shape[1]
number_of_slices = len(datasets)
datatype = first_slice.dtype

print("Rows:", rows)
print("Columns:", columns)
print("Number of slices:", number_of_slices)
print("Datatype:", datatype)


# 3. I prepared the  function that creates an empty 3D numpy array for the DICOM volume.
# It uses the first slice to ensure homogenization of shape and datatype.
# volume dimensions: slice shape in x-,y- direction and number of slices in z-direction
def prepare_empty_volume(rows, columns, number_of_slices, datatype):
    volume = np.zeros((rows, columns, number_of_slices), dtype=datatype)
    return volume

#calling that function
volume3D = prepare_empty_volume(rows, columns, number_of_slices, datatype)

print("Volume shape:", volume3D.shape)
print("Volume datatype:", volume3D.dtype)


print("Volume min intensity:", volume3D.min())
print("Volume max intensity:", volume3D.max())

##4. Fill the 3D volume with sorted DICOM slices
# Goal:
# - get correct slice index from DICOM metadata
# - copy every slice into correct z-position in the 3D volume


def sort_and_fill_volume(datasets, volume3D):

    for dataset in datasets:

        # get slice index from DICOM metadata
        slice_index = int(dataset[0x0020, 0x0013].value)

        # copy pixel data into correct position in 3D volume
        ## sorting is performed by storing every DICOM slice into the correct z-position in the 3D volume using the Instance Number metadata
        # copy pixel data into correct position in 3D volume
        volume3D[:, :, slice_index] = dataset.pixel_array

    return volume3D

volume3D = sort_and_fill_volume(datasets, volume3D)

print("Volume min intensity:", volume3D.min(),"Volume max intensity:", volume3D.max())