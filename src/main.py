# main.py
# author: Barbara Klimek

from load_dicom_volume import (
    load_dicom_files,
    prepare_empty_volume,
    sort_and_fill_volume
)
from visualisation import (
    show_54th_slice,
    show_slice_slider
)
from windowing import show_windowing

# 1. load datasets
filepath = '../data/Lobus_DICOMs_mixed_up/*.dcm'
datasets = load_dicom_files(filepath)

# 2. get information from first slice -> rows, columns, number_of_slices and datatype
first_slice = datasets[0].pixel_array

rows = first_slice.shape[0]
columns = first_slice.shape[1]
number_of_slices = len(datasets)
datatype = first_slice.dtype

# 3. create empty 3D volume
volume3D = prepare_empty_volume(
    rows,
    columns,
    number_of_slices,
    datatype
)

#4.  sort slices and fill new 3d volume
volume3D = sort_and_fill_volume(datasets, volume3D)

#5. visualize the 54th slice image after sorting
show_54th_slice(volume3D)

#6. visualize slices with slider
show_slice_slider(volume3D)

#7. show windowing
show_windowing(volume3D)