# one_year_data/download_data.py
import cdsapi
import os

def download_era5_data():
    # Create data directories
    os.makedirs('data/raw', exist_ok=True)
    
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
            '01', '02', '03', '04', '05', '06',
            '07', '08', '09', '10', '11', '12',
        ],
        'time': [
            '00:00',
        ],
        'area': [
            36, -13, 21, 0,  # North, West, South, East
        ],
    }
    
    print("Starting download...")
    client.retrieve(
        'reanalysis-era5-land-monthly-means',
        request,
        'data/raw/morocco_climate.nc'
    )
    print("Download completed!")

if __name__ == "__main__":
    download_era5_data()