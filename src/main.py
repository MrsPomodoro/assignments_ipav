#################################
# TODO ASSIGNMENT:
# - the task – create 3D numpy array (volume) from list of mixed-up individual loaded DICOM slice images and implement a matplotlib visualization 
#   which allows to select the visualized slice from the volume via a slider, 
# - also implement sliders for windowing ITF functionality (apply an intensity transfer function on the visualized slice) 
# - and implement a ROI selection to derive the ITF parameters from it
#################################

# main.py
# author: Barbara Klimek

from load_dicom_volume import (
    load_dicom_files,
    prepare_empty_volume,
    sort_and_fill_volume
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

print("Volume min intensity:", volume3D.min(),"Volume max intensity:", volume3D.max())

#5. show windowing ITF visualization with slice slider, center slider, width slider and ROI selection
show_windowing(volume3D)