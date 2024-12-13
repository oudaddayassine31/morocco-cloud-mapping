from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
import xarray as xr
import numpy as np
from pathlib import Path
import io
from PIL import Image
import mercantile
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data directory
DATA_DIR = Path("data_2023/processed/pyramids")

# Updated variable configurations with corrected ranges
VARIABLE_CONFIGS = {
    't2m': {
        'vmin': -5,     # Celsius
        'vmax': 45,     # Celsius
        'colormap': 'RdYlBu_r',
        'description': 'Temperature at 2m height',
        'convert_func': lambda x: x  # No conversion needed, data already in Celsius
    },
    'tp': {
        'vmin': 0,
        'vmax': 200,    # Adjusted based on actual data range
        'colormap': 'Blues',
        'description': 'Total precipitation',
        'convert_func': lambda x: x*1000  # No conversion needed, keeping original units
    }
}

@app.get("/")
async def root():
    return {
        "message": "Morocco Climate Data API",
        "status": "running",
        "variables": list(VARIABLE_CONFIGS.keys()),
        "time_range": {"start": 0, "end": 11}
    }

@app.get("/api/debug/{variable}")
async def debug_variable(variable: str):
    try:
        zoom_file = DATA_DIR / "zoom_0"
        ds = xr.open_zarr(zoom_file)
        var_data = ds[variable].isel(valid_time=0)
        
        # Get raw statistics
        raw_stats = {
            "min": float(var_data.min()),
            "max": float(var_data.max()),
            "mean": float(var_data.mean()),
            "shape": var_data.shape
        }
        
        # Get converted statistics
        conv_func = VARIABLE_CONFIGS[variable]['convert_func']
        conv_data = conv_func(var_data)
        conv_stats = {
            "min": float(conv_data.min()),
            "max": float(conv_data.max()),
            "mean": float(conv_data.mean())
        }
        
        return {
            "raw_stats": raw_stats,
            "converted_stats": conv_stats,
            "config": VARIABLE_CONFIGS[variable]
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/tiles/{z}/{x}/{y}")
async def get_tile(z: int, x: int, y: int, variable: str = 't2m', time: int = 0):
    try:
        logger.info(f"Processing tile request: z={z}, x={x}, y={y}, variable={variable}, time={time}")
        
        zoom_file = DATA_DIR / f"zoom_{z}"
        if not zoom_file.exists():
            return Response(
                status_code=404,
                content=f"Zoom level {z} not found",
                media_type="text/plain"
            )

        bounds = tile_bounds(x, y, z)
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

        # Convert values according to variable type
        data_array = VARIABLE_CONFIGS[variable]['convert_func'](data_slice.values)
        
        # Create and apply Morocco mask
        lats = data_slice.latitude.values
        lons = data_slice.longitude.values
        lon_mesh, lat_mesh = np.meshgrid(lons, lats)
        
        morocco_mask = (
            (lat_mesh >= 21) & 
            (lat_mesh <= 36) & 
            (lon_mesh >= -13) & 
            (lon_mesh <= 0)
        )
        
        # Apply mask
        data_array = np.where(morocco_mask, data_array, np.nan)
        
        # Log data range for debugging
        valid_data = data_array[~np.isnan(data_array)]
        if len(valid_data) > 0:
            logger.info(f"Data range for {variable}: min={valid_data.min():.4f}, max={valid_data.max():.4f}")
        
        # Resize to 256x256
        if data_slice.shape != (256, 256):
            data_array_filled = np.nan_to_num(data_array, nan=0)
            img_temp = Image.fromarray(data_array_filled.astype(np.float32))
            img_temp = img_temp.resize((256, 256), Image.BILINEAR)
            data_array = np.array(img_temp)
            
            mask_temp = Image.fromarray(morocco_mask.astype(np.uint8) * 255)
            mask_temp = mask_temp.resize((256, 256), Image.NEAREST)
            resized_mask = np.array(mask_temp) > 0
            
            data_array = np.where(resized_mask, data_array, np.nan)
        
        # Get normalization range
        var_config = VARIABLE_CONFIGS[variable]
        vmin = var_config['vmin']
        vmax = var_config['vmax']
        
        # Normalize data
        data_array = np.clip(data_array, vmin, vmax)
        norm_data = (data_array - vmin) / (vmax - vmin)
        norm_data = np.nan_to_num(norm_data, nan=0)
        
        # Convert to image
        img_data = (norm_data * 255).astype(np.uint8)
        
        # Apply colormap
        from matplotlib import cm
        colormap = cm.get_cmap(var_config['colormap'])
        colored_data = (colormap(img_data) * 255).astype(np.uint8)
        
        # Set transparency for areas outside Morocco
        mask = resized_mask if data_slice.shape != (256, 256) else morocco_mask
        colored_data[~mask] = [0, 0, 0, 0]
        
        # Create image
        img = Image.fromarray(colored_data)
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        
        return Response(content=img_byte_arr, media_type="image/png")
        
    except Exception as e:
        logger.error(f"Error processing tile: {str(e)}", exc_info=True)
        return Response(
            status_code=500,
            content=str(e),
            media_type="text/plain"
        )

def tile_bounds(x, y, z):
    tile = mercantile.Tile(x, y, z)
    bounds = mercantile.bounds(tile)
    return {
        'west': bounds.west,
        'east': bounds.east,
        'north': bounds.north,
        'south': bounds.south
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)