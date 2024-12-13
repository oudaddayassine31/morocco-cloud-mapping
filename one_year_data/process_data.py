import xarray as xr
import zarr
import numpy as np
from pathlib import Path

def process_data():
    # Create processed data directory
    processed_dir = Path('data_2023/processed')
    processed_dir.mkdir(parents=True, exist_ok=True)
    
    input_file = Path('data_2023/raw/morocco_climate_2023.nc')
    output_file = processed_dir / 'morocco_climate_2023.zarr'
    
    print("Loading NetCDF dataset...")
    try:
        ds = xr.open_dataset(input_file)
        
        # Print dataset information
        print("\nDataset information:")
        print(ds.info())
        
        # Convert temperature from Kelvin to Celsius
        if 't2m' in ds:
            ds['t2m'] = ds['t2m'] - 273.15
            ds['t2m'].attrs['units'] = 'celsius'
        
        # Convert precipitation to mm/day if needed
        if 'tp' in ds:
            ds['tp'] = ds['tp'] * 1000  # Convert m to mm
            ds['tp'].attrs['units'] = 'mm'
        
        # Configure chunks based on actual dimension names
        chunks = {
            'valid_time': 1,
            'latitude': min(100, ds.sizes['latitude']),
            'longitude': min(100, ds.sizes['longitude'])
        }
        
        print("\nConfigured chunks:", chunks)
        
        # Convert to Zarr format
        print("\nStarting Zarr conversion...")
        ds.chunk(chunks).to_zarr(output_file, mode='w')
        print("Zarr conversion completed successfully!")
        
        # Verify the created Zarr file
        print("\nVerifying Zarr file:")
        ds_zarr = xr.open_zarr(output_file)
        print(ds_zarr.info())
        
    except Exception as e:
        print(f"\nError during processing: {str(e)}")
        raise

if __name__ == "__main__":
    process_data()