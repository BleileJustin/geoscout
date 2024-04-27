# Line of sight geotiff data processing algogrithm
import matplotlib.pyplot as plt
import numpy as np
import math
import rasterio
from rasterio.plot import show

dem = rasterio.open('data/output_COP30.tif')
dem_array = dem.read(1)
transform = dem.transform

plt.imshow(dem_array, cmap='gray')
plt.colorbar()
plt.show()