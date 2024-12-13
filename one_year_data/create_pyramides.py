import xarray as xr
import zarr
import numpy as np
from pathlib import Path

def create_pyramids(input_zarr, output_path, max_zoom=4):
    print(f"Loading Zarr dataset from {input_zarr}...")
    ds = xr.open_zarr(input_zarr)
    
    # Create output directory if it doesn't exist
    Path(output_path).mkdir(parents=True, exist_ok=True)
    
    # Configure base chunking
    chunk_sizes = {
        'valid_time': 1,
        'latitude': min(50, ds.sizes['latitude']),
        'longitude': min(50, ds.sizes['longitude'])
    }
    
    print(f"Base chunking configuration: {chunk_sizes}")
    ds = ds.chunk(chunk_sizes)
    
    for zoom in range(max_zoom):
        print(f"\nGenerating zoom level {zoom}")
        scale = 2 ** zoom
        
        try:
            # Coarsen the dataset
            coarsened = ds.coarsen(
                latitude=scale,
                longitude=scale,
                boundary='trim'
            ).mean()
            
            # Calculate dimensions for this zoom level
            new_dims = {
                'latitude': len(ds.latitude) // scale,
                'longitude': len(ds.longitude) // scale
            }
            print(f"Dimensions for zoom level {zoom}: {new_dims}")
            
            # Configure chunks for this zoom level
            level_chunks = {
                'valid_time': 1,
                'latitude': min(50, new_dims['latitude']),
                'longitude': min(50, new_dims['longitude'])
            }
            print(f"Chunks for zoom level {zoom}: {level_chunks}")
            
            # Apply chunking and save
            coarsened = coarsened.chunk(level_chunks)
            output_zoom = f"{output_path}/zoom_{zoom}"
            print(f"Saving to {output_zoom}")
            
            coarsened.compute().to_zarr(output_zoom, mode='w', safe_chunks=True)
            print(f"Zoom level {zoom} created successfully")
            
        except Exception as e:
            print(f"Error at zoom level {zoom}: {str(e)}")
            raise

if __name__ == "__main__":
    try:
        input_zarr = 'data_2023/processed/morocco_climate_2023.zarr'
        output_path = 'data_2023/processed/pyramids'
        
        # Create pyramids directory
        Path(output_path).mkdir(parents=True, exist_ok=True)
        
        create_pyramids(input_zarr, output_path)
        print("\nPyramid creation completed successfully!")
        
    except Exception as e:
        print(f"\nError during pyramid creation: {str(e)}")
        # Print debug information
        ds = xr.open_zarr('data_2023/processed/morocco_climate_2023.zarr')
        print(f"Original dimensions: {ds.sizes}")
        print(f"Original chunks: {ds.chunks}")