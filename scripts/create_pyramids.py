# scripts/create_pyramids.py
import xarray as xr
import zarr
import numpy as np
from pathlib import Path

def create_pyramids(input_zarr, output_path, max_zoom=4):
    print("Chargement des données Zarr...")
    ds = xr.open_zarr(input_zarr)
    
    # Forcer un rechunking explicite basé sur les dimensions actuelles
    chunk_sizes = {
        'valid_time': 1,
        'latitude': min(50, ds.dims['latitude']),
        'longitude': min(50, ds.dims['longitude'])
    }
    
    print(f"Rechunking avec: {chunk_sizes}")
    ds = ds.chunk(chunk_sizes)
    
    for zoom in range(max_zoom):
        print(f"\nCréation du niveau de zoom {zoom}")
        scale = 2 ** zoom
        
        try:
            # Rééchantillonner
            coarsened = ds.coarsen(
                latitude=scale,
                longitude=scale,
                boundary='trim'
            ).mean()
            
            # Calculer les nouvelles dimensions
            new_dims = {
                'latitude': len(ds.latitude) // scale,
                'longitude': len(ds.longitude) // scale
            }
            print(f"Nouvelles dimensions: {new_dims}")
            
            # Définir les chunks pour ce niveau
            level_chunks = {
                'valid_time': 1,
                'latitude': min(50, new_dims['latitude']),
                'longitude': min(50, new_dims['longitude'])
            }
            print(f"Chunks pour ce niveau: {level_chunks}")
            
            # Appliquer les nouveaux chunks et forcer le calcul
            coarsened = coarsened.chunk(level_chunks)
            
            # Sauvegarder
            output_zoom = f"{output_path}/zoom_{zoom}"
            print(f"Sauvegarde dans {output_zoom}")
            coarsened.compute().to_zarr(output_zoom, mode='w', safe_chunks=True)
            
            print(f"Niveau de zoom {zoom} créé avec succès")
            
        except Exception as e:
            print(f"Erreur au niveau de zoom {zoom}: {str(e)}")
            print("\nInformations sur le niveau:")
            print(f"Scale: {scale}")
            print(f"Dimensions coarsened: {coarsened.dims if 'coarsened' in locals() else 'N/A'}")
            raise

if __name__ == "__main__":
    try:
        # Créer le dossier de sortie
        Path('data/processed/pyramids').mkdir(parents=True, exist_ok=True)
        
        create_pyramids(
            'data/processed/morocco_climate.zarr',
            'data/processed/pyramids'
        )
        print("\nCréation des pyramides terminée avec succès!")
        
    except Exception as e:
        print(f"\nErreur lors de la création des pyramides: {str(e)}")
        print("\nInformations de debug:")
        ds = xr.open_zarr('data/processed/morocco_climate.zarr')
        print(f"Dimensions originales: {ds.dims}")
        print(f"Chunks originaux: {ds.chunks}")