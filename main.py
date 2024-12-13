from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
import xarray as xr
import numpy as np
from pathlib import Path
import io
from PIL import Image
import mercantile
import uvicorn

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data directory
DATA_DIR = Path("data/processed/pyramids")

def tile_bounds(x, y, z):
    tile = mercantile.Tile(x, y, z)
    bounds = mercantile.bounds(tile)
    return {
        'west': bounds.west,
        'east': bounds.east,
        'north': bounds.north,
        'south': bounds.south
    }

@app.get("/")
async def root():
    return {"message": "Morocco Climate Data API", "status": "running"}

@app.get("/api/tiles/{z}/{x}/{y}")
async def get_tile(z: int, x: int, y: int, variable: str = 't2m', time: int = 0):
    try:
        # Verify data directory exists
        if not DATA_DIR.exists():
            return Response(
                status_code=500,
                content=f"Data directory not found: {DATA_DIR}",
                media_type="text/plain"
            )

        zoom_file = DATA_DIR / f"zoom_{z}"
        if not zoom_file.exists():
            return Response(
                status_code=404,
                content=f"Zoom level {z} not found",
                media_type="text/plain"
            )

        # Get tile bounds
        bounds = tile_bounds(x, y, z)
        
        # Load data
        ds = xr.open_zarr(zoom_file)
        
        if variable not in ds:
            return Response(
                status_code=404,
                content=f"Variable {variable} not found",
                media_type="text/plain"
            )

        # Select data
        data = ds[variable].isel(valid_time=time)
        
        # Select region
        data_slice = data.sel(
            latitude=slice(bounds['north'], bounds['south']),
            longitude=slice(bounds['west'], bounds['east'])
        )

        # Create Morocco mask
        lats = data_slice.latitude.values
        lons = data_slice.longitude.values
        lon_mesh, lat_mesh = np.meshgrid(lons, lats)
        
        morocco_mask = (
            (lat_mesh >= 21) & 
            (lat_mesh <= 36) & 
            (lon_mesh >= -13) & 
            (lon_mesh <= 0)
        )
        
        # Apply mask to data
        data_array = data_slice.values
        data_array = np.where(morocco_mask, data_array, np.nan)
        
        # Resize to 256x256
        if data_slice.shape != (256, 256):
            # Handle NaN values before resizing
            data_array_filled = np.nan_to_num(data_array, nan=0)
            img_temp = Image.fromarray(data_array_filled.astype(np.float32))
            img_temp = img_temp.resize((256, 256), Image.BILINEAR)
            data_array = np.array(img_temp)
            
            # Resize mask as well
            mask_temp = Image.fromarray(morocco_mask.astype(np.uint8) * 255)
            mask_temp = mask_temp.resize((256, 256), Image.NEAREST)
            resized_mask = np.array(mask_temp) > 0
            
            # Reapply mask after resizing
            data_array = np.where(resized_mask, data_array, np.nan)
        
        # Normalize data
        if variable == 't2m':
            vmin, vmax = 273.15, 313.15  # 0°C to 40°C
        else:
            vmin, vmax = 0, 0.00035  # 0 to 100mm
        
        data_array = np.clip(data_array, vmin, vmax)
        norm_data = (data_array - vmin) / (vmax - vmin)
        
        # Handle NaN values in normalization
        norm_data = np.nan_to_num(norm_data, nan=0)
        
        # Convert to image
        img_data = (norm_data * 255).astype(np.uint8)
        
        # Apply colormap
        from matplotlib import cm
        colormap = cm.get_cmap('RdYlBu_r' if variable == 't2m' else 'Blues')
        colored_data = (colormap(img_data) * 255).astype(np.uint8)
        
        # Set transparency for areas outside Morocco
        if data_slice.shape != (256, 256):
            colored_data[~resized_mask] = [0, 0, 0, 0]
        else:
            colored_data[~morocco_mask] = [0, 0, 0, 0]
        
        # Create and save image
        img = Image.fromarray(colored_data)
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        
        return Response(content=img_byte_arr, media_type="image/png")
        
    except Exception as e:
        print(f"Error processing tile {z}/{x}/{y}: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response(
            status_code=500,
            content=str(e),
            media_type="text/plain"
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)