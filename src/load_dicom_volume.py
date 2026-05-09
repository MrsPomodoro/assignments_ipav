import numpy as np
import pydicom
import matplotlib.pyplot as plt
import glob

# load the DICOM files into list datasets
filepath = './Lobus_DICOMs_mixed_up/*.dcm'
filenames = glob.glob(filepath, recursive=False)
datasets = []
for fname in filenames:
    print("loading: {}".format(fname))
    datasets.append(pydicom.dcmread(fname))
print(len(datasets), ' slices loaded...')