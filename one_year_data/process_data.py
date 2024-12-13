# one_year_data/process_data.py
import xarray as xr
import zarr
import numpy as np
from pathlib import Path

def process_data():
    # Create necessary directories
    Path('data/processed').mkdir(parents=True, exist_ok=True)
    
    # Load data
    print("Loading data...")
    ds = xr.open_dataset('data/raw/morocco_climate.nc')
    
    # Print dataset information
    print("\nDataset information:")
    print(ds.info())
    
    # Configure chunks using sizes instead of dims
    chunks = {
        'valid_time': 1,
        'latitude': min(100, ds.sizes['latitude']),
        'longitude': min(100, ds.sizes['longitude'])
    }
    
    print("\nConfigured chunks:", chunks)
    
    try:
        # Convert to Zarr with mode='w' to overwrite any existing data
        print("\nStarting Zarr conversion...")
        ds.chunk(chunks).to_zarr(
            'data/processed/morocco_climate.zarr',
            mode='w'  # Add this line
        )
        print("Conversion completed successfully!")
        
        # Verify result
        print("\nVerifying created Zarr file:")
        ds_zarr = xr.open_zarr('data/processed/morocco_climate.zarr')
        print(ds_zarr.info())
        
    except Exception as e:
        print(f"\nError during conversion: {str(e)}")
        
    finally:
        ds.close()

if __name__ == "__main__":
    process_data()