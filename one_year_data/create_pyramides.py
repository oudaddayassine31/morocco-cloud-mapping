# one_year_data/create_pyramids.py
import xarray as xr
import numpy as np
from pathlib import Path
import shutil

def create_pyramids(input_zarr, output_path, max_zoom=4):
    print("Loading Zarr data...")
    
    # Clean up existing pyramids directory if it exists
    if Path(output_path).exists():
        shutil.rmtree(output_path)
    Path(output_path).mkdir(parents=True, exist_ok=True)
    
    ds = xr.open_zarr(input_zarr)
    
    # Force explicit rechunking based on current dimensions
    chunk_sizes = {
        'valid_time': 1,
        'latitude': min(50, ds.sizes['latitude']),
        'longitude': min(50, ds.sizes['longitude'])
    }
    
    print(f"Initial chunking with: {chunk_sizes}")
    ds = ds.chunk(chunk_sizes)
    
    for zoom in range(max_zoom):
        print(f"\nCreating zoom level {zoom}")
        scale = 2 ** zoom
        
        try:
            # Coarsen the dataset
            coarsened = ds.coarsen(
                latitude=scale,
                longitude=scale,
                boundary='trim'
            ).mean()
            
            # Calculate new dimensions
            new_dims = {
                'latitude': len(ds.latitude) // scale,
                'longitude': len(ds.longitude) // scale
            }
            print(f"Dimensions for zoom {zoom}: {new_dims}")
            
            # Set chunks for this level
            level_chunks = {
                'valid_time': 1,
                'latitude': min(50, new_dims['latitude']),
                'longitude': min(50, new_dims['longitude'])
            }
            print(f"Chunks for zoom {zoom}: {level_chunks}")
            
            # Create output directory
            zoom_dir = Path(output_path) / f"zoom_{zoom}"
            if zoom_dir.exists():
                shutil.rmtree(zoom_dir)
            
            # Save the coarsened data
            print(f"Saving zoom level {zoom} to {zoom_dir}")
            coarsened.chunk(level_chunks).to_zarr(str(zoom_dir), mode='w')
            
            print(f"Successfully created zoom level {zoom}")
            
        except Exception as e:
            print(f"Error creating zoom level {zoom}: {str(e)}")
            raise
            
    print("\nAll pyramid levels created successfully!")

if __name__ == "__main__":
    try:
        create_pyramids(
            'data/processed/morocco_climate.zarr',
            'data/processed/pyramids',
            max_zoom=4
        )
    except Exception as e:
        print(f"Error during pyramid creation: {str(e)}")