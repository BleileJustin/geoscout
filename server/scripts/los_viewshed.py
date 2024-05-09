# Line of sight geotiff data processing algogrithm
import matplotlib.pyplot as plt
import numpy as np
import math
import rasterio
from rasterio.plot import show
from multiprocessing import Pool

dem = rasterio.open('../../data/output_COP30.tif')
dem_array = dem.read(1)
print(dem_array[0][0])
transform = dem.transform

"""
plt.imshow(dem_array, cmap='gray')
plt.colorbar()
plt.title('Digital Elevation Model')
plt.show()
"""




# Determine if the point (x2, y2) is visible from (x1, y1) in dem_array.
def is_visible(dem_array, x1, y1, x2, y2):
    """Determine if the point (x2, y2) is visible from (x1, y1) in dem_array."""
    # Calculate the number of steps for iteration based on the greater of dx or dy
    dx = x2 - x1
    dy = y2 - y1
    steps = max(abs(dx), abs(dy))
 
    # Handle the case when steps is zero
    if steps == 0:
        return False
 
    # Calculate the increments for x and y
    x_inc = dx / steps
    y_inc = dy / steps
 
    # Start from the source point
    x = x1
    y = y1
 
    # Height at the source point
    z = dem_array[int(y1), int(x1)] + 20
 
    # Iterate over the cells between source and target
    for i in range(1, int(steps)):
        x += x_inc
        y += y_inc
 
        # Calculate the elevation of the direct line at this point
        line_elevation = z + (dem_array[int(y2), int(x2)] - z) * (i / steps)
 
        # If the DEM elevation at this point is higher than the direct line, it's not visible
        if dem_array[int(y), int(x)] > line_elevation:
            return False
 
    return True
 
# Starting coords
transmitter_y, transmitter_x = 39.665302, -105.206676

 
# Transforming lat long into grid coordinates
inv_transform = ~transform
transmitter_x, transmitter_y = [
    int(round(coord)) for coord in inv_transform * (transmitter_x, transmitter_y)]
 
# Create an empty array for visibility
visibility_array = np.zeros_like(dem_array)
def process_section(x_range):
    visibility_array_section = np.zeros((dem_array.shape[0], len(x_range)))
    import time
    start = time.time()
    print('Starting section...')
    for i, x in enumerate(x_range):
        if x % 100 == 0:
            print('Column', x, 'in section', visibility_array_section.shape[1], 'of', dem_array.shape[1])
            print('Elapsed time:', float(time.time() - start))
            start = time.time()
        for y in range(dem_array.shape[0]):
            visibility_array_section[y, i] = is_visible(
                dem_array, transmitter_x, transmitter_y, x, y)
    return visibility_array_section

if __name__ == '__main__':
    with Pool() as p:
        x_ranges = [range(i, i+100) for i in range(0, dem_array.shape[1], 100)]
        results = p.map(process_section, x_ranges)
    visibility_array = np.concatenate(results, axis=1)
    print("Saving...")
    with rasterio.open('../../data/result/los.tif', 'w', **dem.meta) as dst:
        dst.write(visibility_array, 1)
    print("Done")

# Plot the visibility array
plt.imshow(visibility_array, cmap='gray')
plt.colorbar()
plt.title('Line of Sight Analysis')
plt.show()