import numpy as np
import xarray as xr
# import matplotlib.pyplot as plt
import os
import glob
# from scipy import stats
# import re
import datetime
from scipy.interpolate import griddata
from argparse import ArgumentParser

if __name__=="__main__":
    p = ArgumentParser(description="""Regridding ERA5 data""")
    p.add_argument('-month', '--month', default=1, type=int, help='month (1-12) (int)')
    p.add_argument('-year', '--year', default=2010, type=int, help='year (int)')
    
    args = p.parse_args()
    year_ = str(args.year)
    month_ = '%02d' % args.month
    
    
    dir_work = '/p/scratch/cjibg36/kaandorp2/'
    resolution = '109x106'
    grid_dest = xr.load_dataset( os.path.join(dir_work,'TSMP/setup_clm_cordex_%s/inputdata/griddata_cordex_%s.nc' % (resolution,resolution) ) )
    folder_data_in = os.path.join(dir_work, 'data/ERA5_BC/')
    folder_data_out = os.path.join(dir_work, 'TSMP/setup_clm_cordex_%s/atmforcings_nanocean/' % resolution)

    if not os.path.exists(folder_data_out):
        os.mkdir(folder_data_out)


    # Interpolation method
    method_interp = 'nearest'

    # Variables: ERA5 names (in), and required CLM names (out) 
    vars_in = ['Tair','PSurf','Qair','Rainf','SWdown','LWdown','Wind']
    vars_out = ['TBOT','PSRF','QBOT','PRECTmms','FSDS','FLDS','WIND']

    # Variables to copy from the CLM griddata file
    vars_copy = ['LATIXY','LONGXY','LONE','LONW','LATS','LATN','EDGEE','EDGES','EDGEW','EDGEN']

    # don't set this variable to true! CLM seems to need atmosphere data for ocean cells adjacent to land as well -> can be changed in the future
    use_landmask = False # True: have NaN's on ocean gridcells; False: fill NaN's with interpolation


    # initialize output dataset by copying the griddata file
    data_out = grid_dest.copy()
    data_out = data_out.drop_vars(['LANDMASK','AREA'])

    for i2,(v_in, v_out) in enumerate(zip(vars_in,vars_out)):
        print(v_in,v_out)
        filename = v_in + '*' + year_ + month_ + '*'
        file_in = glob.glob(os.path.join( folder_data_in, filename))[0]

        data_in = xr.load_dataset( file_in )
        if i2 == 0:
            data_out['time'] = data_in['time'].copy()

        X,Y = np.meshgrid(data_in['lon'],data_in['lat'])

        data_out_var = np.zeros([len(data_in[v_in]['time']),grid_dest['LANDMASK'].shape[0],grid_dest['LANDMASK'].shape[1]])

        for i1,time_ in enumerate(data_in[v_in]['time']):

            if i1 % 100 == 0:
                print('%i / %i' % (i1, len(data_in[v_in]['time'])) )

            mask_in = ~np.isnan(data_in[v_in][i1,:,:])
            if use_landmask:
                mask_out = (grid_dest['LANDMASK'] == 1)
            else:
                mask_out = np.ones(grid_dest['LANDMASK'].shape,dtype=bool)

            #-------------------- interpolation routine --------------------
            # should be changed to ESMF for conservative interpolation
            data_interp = griddata((X[mask_in],Y[mask_in]),
                                    data_in[v_in][i1,:,:].values[mask_in],
                                    (data_out['LONGXY'].values[mask_out],data_out['LATIXY'].values[mask_out]),
                                    method=method_interp)

            data_i_out = np.nan*np.zeros(mask_out.shape)
            data_i_out[mask_out] = data_interp
            #-------------------- /interpolation routine --------------------

            # add interpolated data to array
            data_out_var[i1,:,:] = data_i_out

        # put array in data_out
        data_out[v_out] = (['time','lat','lon'], data_out_var)

    filename_out = year_+'-'+month_+'.nc'

    data_out.attrs['title'] = 'Regridded bias-corrected ERA5 data'
    data_out.attrs['source_file'] = 'regridded by m.kaandorp, source data doi: 10.24381/cds.20d54e34. Interpolation: %s' % method_interp
    data_out.attrs['creation_date'] = str(datetime.datetime.now())
    data_out.to_netcdf( os.path.join(folder_data_out,filename_out) )