#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=5
#SBATCH --time=1:59:00
#SBATCH --partition=devel
#SBATCH --job-name=regrid_ERA5
#SBATCH --output=out/out.%j
#SBATCH --error=out/err.%j
#SBATCH --account=jibg36
#SBATCH --array=24135-24139%5
# m.kaandorp@fz-juelich.de
# atmospheric files to be processed need to have the format yyyy-mm.nc and need to contain all variables
#

module load Stages/2023  
module load Intel/2022.1.0  ParaStationMPI/5.8.0-1-mt
module load CDO/2.1.1
module load GCCcore/.11.3.0
module load netcdf4-python/1.6.1-serial
module load xarray/2022.9.0

year_start=2010
month_start=1
year_end=2020
month_end=12

i_start=$((year_start*12+month_start))
i_end=$((year_end*12+month_end))

# input atmospheric data
dir_atm_in=/p/scratch/cjibg36/kaandorp2/data/ERA5
# output folder, make sure it exists
dir_atm_out=/p/scratch/cjibg36/kaandorp2/data/ERA5_EUR-11_CLM
# dir containing the grid description file for the destination grid & the corresponding CLM griddata*.nc file
dir_static=/p/project/cjibg36/kaandorp2/TSMP_setups/static

# example file to calculate the input grid description file
name_atm_example=2010-01.nc
# output griddes
name_griddes_out=EUR-11_TSMP_FZJ-IBG3_CLMPFLDomain_444x432_griddes.txt
# clm griddata*.nc file
name_griddata_clm=griddata_CLM_EUR-11_TSMP_FZJ-IBG3_CLMPFLDomain_444x432.nc


# Make griddescription file of the input atmospheric dataset
if [ ! -f $dir_atm_in/griddes_in.txt ]
then
    echo "Calculating input grid description"
    cdo griddes $dir_atm_in/$name_atm_example > $dir_atm_in/griddes_in.txt
else
    echo "Griddescription input exists"
fi

# Calculate remapping weights from atm to clm grid
if [ ! -f $dir_atm_out/remapweights.nc ]
then
    echo "Calculating remapping weights"
    cdo gencon,$dir_static/$name_griddes_out -setgrid,$dir_atm_in/griddes_in.txt $dir_atm_in/$name_atm_example $dir_atm_out/remapweights.nc
else
    echo "Remapping weights exist"
fi


func(){
    index=$1
    y=$((index/12))
    m=$((index%12+1))
    
    echo "Processing year: ${y}, month: ${m}"
    name="$(printf "%04d-%02d.nc" $y $m)"
    name_out1="$(printf "%04d-%02d_EUR11.nc" $y $m)"
    name_out2="$(printf "%04d-%02d_EUR11_CLM.nc" $y $m)"
    name_tmp1="$(printf "tmp1_%04d-%02d.nc" $y $m)"
    name_tmp2="$(printf "tmp2_%04d-%02d.nc" $y $m)"
    
    file_in=$dir_atm_in/$name
    file_tmp1=$dir_atm_out/$name_tmp1
    file_tmp2=$dir_atm_out/$name_tmp2
    ls -l $file_in

    echo "calculating wind speed..."
    ## calculate wind speed
    cdo expr,'WIND=sqrt(u10*u10+v10*v10)' $file_in $file_tmp1
    ## add wind speed to dataset
    cdo merge $file_in $file_tmp1 $file_tmp2
    rm $file_tmp1
    cdo delvar,u10,v10 $file_tmp2 $file_tmp1
    rm $file_tmp2

    echo "giving variables CLM names..."
    ## change ERA5 to CLM names
    cdo chvar,d2m,Tdew,t2m,TBOT,msdwlwrf,FLDS,msdwswrf,FSDS,sp,PSRF,mtpr,PRECTmms $file_tmp1 $file_tmp2
    rm $file_tmp1

    echo "remapping the data..."
    ## remap
    cdo -L -f nc4c -remap,$dir_static/$name_griddes_out,$dir_atm_out/remapweights.nc $file_tmp2 $file_tmp1
    rm $file_tmp2
    ## rotated lon/lat to 'normal' lon/lat
    cdo setgridtype,curvilinear $file_tmp1 $dir_atm_out/$name_out1
    rm $file_tmp1
    echo "Remapped data written to: $dir_atm_out/$name_out1"

    python make_atmforcing_CLM_ready.py -i $dir_atm_out/$name_out1 -s $dir_static/$name_griddata_clm -o $dir_atm_out/$name_out2
    echo "CLM ready forcing writting to: $dir_atm_out/$name_out2"

}

## process a single month, example: number=year*12+month, e.g. -> 2010-01 is 24121)
# func 24125

## process a bunch of months at the same time
func $SLURM_ARRAY_TASK_ID
