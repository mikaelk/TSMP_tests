# Import the ParFlow TCL package
lappend auto_path /p/project/cjibg36/kaandorp2/TSMP_patched/bin/JUWELS_3.1.0MCT_clm-pfl 
set ::env(PARFLOW_DIR) /p/project/cjibg36/kaandorp2/TSMP_patched/parflow
package require parflow
namespace import Parflow::*

pfset FileVersion 4

pfset Process.Topology.P 9
pfset Process.Topology.Q 9
pfset Process.Topology.R 1
# THE COMPUTATIONAL GRID IS A (BOX) THT CONTAINS THE MAIN PROBLEM. THIS CAN EITHER BE EXACTLY THE SIZE
# OF THE PROBLEM OR LARGER. A BOX GEOMETRY IN PARFLOW CAN BE ASIGNED BY EITHER SPECIFYING COORDINATES FOR
# TWO CORNERS OF THE BOX OR GRID SIZE AND NUMBER OF CELLS IN X,Y, AND Z.
#------------------------------------------------------------------------
# Computational Grid: It Defines The Grid Resolutions within The Domain
#------------------------------------------------------------------------
pfset ComputationalGrid.Lower.X                  0.0
pfset ComputationalGrid.Lower.Y                  0.0
pfset ComputationalGrid.Lower.Z                  0.0

pfset ComputationalGrid.DX                       50000.0
pfset ComputationalGrid.DY                       50000.0
pfset ComputationalGrid.DZ                       1.0

pfset ComputationalGrid.NX                       111
pfset ComputationalGrid.NY                       108
pfset ComputationalGrid.NZ                       1

#-----------------------------------------------------------------------------
# Domain
#-----------------------------------------------------------------------------
pfset Domain.GeomName                            domain

#--------------------------------------------------------
# Distribute Files 
#--------------------------------------------------------
set data [pfload -sa /p/project/cjibg36/kaandorp2/TSMP_patched/tsmp_cordex_111x108_debugleap/input_pf/EUR-11_TSMP_FZJ-IBG3_CLMPFLDomain_111x108_XSLOPE_TPS_HydroRIVER_sea_streams_corr.sa]
pfsave $data -pfb /p/project/cjibg36/kaandorp2/TSMP_patched/tsmp_cordex_111x108_debugleap/run_20120224-20120302/EUR-11_TSMP_FZJ-IBG3_CLMPFLDomain_111x108_XSLOPE_TPS_HydroRIVER_sea_streams_corr.pfb
pfdist /p/project/cjibg36/kaandorp2/TSMP_patched/tsmp_cordex_111x108_debugleap/run_20120224-20120302/EUR-11_TSMP_FZJ-IBG3_CLMPFLDomain_111x108_XSLOPE_TPS_HydroRIVER_sea_streams_corr.pfb
set data [pfload -sa /p/project/cjibg36/kaandorp2/TSMP_patched/tsmp_cordex_111x108_debugleap/input_pf/EUR-11_TSMP_FZJ-IBG3_CLMPFLDomain_111x108_YSLOPE_TPS_HydroRIVER_sea_streams_corr.sa]
pfsave $data -pfb /p/project/cjibg36/kaandorp2/TSMP_patched/tsmp_cordex_111x108_debugleap/run_20120224-20120302/EUR-11_TSMP_FZJ-IBG3_CLMPFLDomain_111x108_YSLOPE_TPS_HydroRIVER_sea_streams_corr.pfb
pfdist /p/project/cjibg36/kaandorp2/TSMP_patched/tsmp_cordex_111x108_debugleap/run_20120224-20120302/EUR-11_TSMP_FZJ-IBG3_CLMPFLDomain_111x108_YSLOPE_TPS_HydroRIVER_sea_streams_corr.pfb
