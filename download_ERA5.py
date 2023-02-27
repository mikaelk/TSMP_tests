import cdsapi
import os

c = cdsapi.Client()

years = ['2010']
months = ['%02d' % int_ for int_ in range(1,13)]
dir_download = '/p/scratch/cjibg36/kaandorp2/data/ERA5_BC'

for year_ in years:
    for month_ in months:
        
        file_ = year_ + '-' + month_ + '.tar.gz'
        
        filename = os.path.join(dir_download,file_)
        print('Downloading %s...' % filename)
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
                'month': month_,
                'year': year_,
            },
            filename)
