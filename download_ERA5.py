import cdsapi
import os

c = cdsapi.Client()

years = [2010]
months = ['%i' % int_ for int_ in range(1,13)]
dir_download = '/p/scratch/cjibg36/kaandorp2/data/'

for year_ in years:
    for month_ in months:
        
        filename = os.path.join(dir_download,
        c.retrieve(
            'derived-near-surface-meteorological-variables',
            {
                'version': '2.1',
                'format': 'tgz',
                'variable': [
                    'near_surface_air_temperature', 'near_surface_specific_humidity', 'near_surface_wind_speed',
                    'rainfall_flux', 'surface_air_pressure', 'surface_downwelling_longwave_radiation',
                    'surface_downwelling_shortwave_radiation',
                ],
                'reference_dataset': 'cru',
                'month': '01',
                'year': '2006',
            },
            '2006-01.tar.gz')
