import cdsapi
from pathlib import Path

def download_era5_data():
    # Create raw data directory if it doesn't exist
    data_dir = Path('data_2023/raw')
    data_dir.mkdir(parents=True, exist_ok=True)
    
    client = cdsapi.Client()
    
    request = {
        'format': 'netcdf',
        'product_type': 'monthly_averaged_reanalysis',
        'variable': [
            '2m_temperature',
            'total_precipitation',
            'relative_humidity',
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
            36, -13, 21, 0,  # North, West, South, East for Morocco
        ],
    }
    
    output_file = data_dir / 'morocco_climate_2023.nc'
    print(f"Starting download to {output_file}...")
    
    try:
        client.retrieve(
            'reanalysis-era5-land-monthly-means',
            request,
            str(output_file)
        )
        print("Download completed successfully!")
        
    except Exception as e:
        print(f"Error during download: {str(e)}")
        raise

if __name__ == "__main__":
    download_era5_data()