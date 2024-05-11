import rasterio
import matplotlib.pyplot as plt

shed = rasterio.open('data/output/los.tif')
shed_array = shed.read(1)
print(shed_array[0][0])
transform = shed.transform


plt.imshow(shed_array, cmap='gray')
plt.colorbar()
plt.title('Viewshed Computation')
plt.show()