import cdsapi

def download_era5_data():
    client = cdsapi.Client()
    
    request = {
        'format': 'netcdf',
        'product_type': 'monthly_averaged_reanalysis',
        'variable': [
            '2m_temperature',
            'total_precipitation',
        ],
        'year': '2023',
        'month': [
            '01', '02', '03',
        ],
        'time': [
            '00:00',
        ],
        'area': [
            36, -13, 21, 0,  # North, West, South, East
        ],
    }
    
    print("Début du téléchargement...")
    client.retrieve(
        'reanalysis-era5-land-monthly-means',
        request,
        'morocco_climate.nc'
    )
    print("Téléchargement terminé!")

if __name__ == "__main__":
    download_era5_data()