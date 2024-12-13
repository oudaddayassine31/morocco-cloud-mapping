# scripts/process_data.py
import xarray as xr
import zarr
import numpy as np
from pathlib import Path

def process_data():
    # Créer les dossiers nécessaires
    Path('data/processed').mkdir(parents=True, exist_ok=True)
    
    # Charger les données
    print("Chargement des données...")
    ds = xr.open_dataset('morocco_climate.nc')
    
    # Afficher les informations du dataset
    print("\nInformations sur le dataset:")
    print(ds.info())
    
    # Créer des chunks dynamiquement
    chunks = {}
    for dim in ds.dims:
        if 'time' in dim.lower():
            chunks[dim] = 1
        elif 'lat' in dim.lower() or 'lon' in dim.lower():
            chunks[dim] = min(100, ds.dims[dim])
    
    print("\nChunks configurés:", chunks)
    
    try:
        # Convertir en Zarr
        print("\nDébut de la conversion en Zarr...")
        ds.chunk(chunks).to_zarr('data/processed/morocco_climate.zarr')
        print("Conversion terminée avec succès!")
        
        # Vérifier le résultat
        print("\nVérification du fichier Zarr créé:")
        ds_zarr = xr.open_zarr('data/processed/morocco_climate.zarr')
        print(ds_zarr.info())
        
    except Exception as e:
        print(f"\nErreur lors de la conversion: {str(e)}")

if __name__ == "__main__":
    process_data()