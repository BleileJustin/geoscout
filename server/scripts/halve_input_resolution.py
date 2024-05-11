import rasterio
from rasterio.enums import Resampling

# Open your existing DEM
# with rasterio.open('data/output_COP30.tif') as dataset:
with rasterio.open('../../data/input/output_COP30.tif') as dataset:
    # Rescale the resolution by a factor of 2 (increase the pixel size)
    data = dataset.read(
        out_shape=(
            dataset.count,
            int(dataset.height / 2),
            int(dataset.width / 2)
        ),
        resampling=Resampling.bilinear
    )

    # scale image transform
    transform = dataset.transform * dataset.transform.scale(
        (dataset.width / data.shape[-1]),
        (dataset.height / data.shape[-2])
    )

# Write the resampled data to a new file
with rasterio.open('../../data/input/output_COP60.tif', 'w',
                   driver='GTiff',
                   height=data.shape[1],
                   width=data.shape[2],
                   count=1,
                   dtype=data.dtype,
                   crs=dataset.crs,
                   transform=transform) as dest:
    dest.write(data)
