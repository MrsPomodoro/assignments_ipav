# main.py
# author: Barbara Klimek

from load_dicom_volume import (
    load_dicom_files,
    prepare_empty_volume,
    sort_and_fill_volume
)

# path to DICOM files
filepath = '../data/Lobus_DICOMs_mixed_up/*.dcm'

# load datasets
datasets = load_dicom_files(filepath)

# get information from first slice
first_slice = datasets[0].pixel_array

rows = first_slice.shape[0]
columns = first_slice.shape[1]
number_of_slices = len(datasets)
datatype = first_slice.dtype

# create empty 3D volume
volume3D = prepare_empty_volume(
    rows,
    columns,
    number_of_slices,
    datatype
)

# sort slices and fill volume
volume3D = sort_and_fill_volume(datasets, volume3D)
