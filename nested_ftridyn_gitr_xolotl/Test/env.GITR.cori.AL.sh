#!/bin/bash
##module unload cray-hdf5-parallel #TEST TEST TEST
module load cray-netcdf
module load boost #1.70.0  #1.63 no longer available
module load cray-mpich

export LIBCONFIGDIR=/global/homes/t/tyounkin/code/libconfigBuild/gnu
export LIBCONFIGLIB=$LIBCONFIGDIR/lib
export LIBCONFIGPP_LIBRARIES=lconfig++
export LIBCONFIGPP_LIBRARY=lconfig++
export LIBCONFIGPP_STATIC_LIBRARY=
export LIBCONFIG_INCLUDE_DIR=$LIBCONFIGDIR/include
export LIBCONFIGPP_INCLUDE_DIR=$LIBCONFIGDIR/include
export LIBCONFIG_LIBRARY=lconfig
export THRUST_INCLUDE_DIRS=/global/homes/t/tyounkin/code/thrust/include
export NETCDF_CXX_INCLUDE_DIR=$NETCDF_DIR/include
export NETCDF_CXX_LIBRARY=$NETCDF_DIR/lib
export NETCDF_INCLUDE_DIR=$NETCDF_DIR/lib
export NETCDF_INCLUDE_DIRS=$NETCDF_DIR/include
export NETCDF_LIBRARIES=$NETCDF_DIR/lib
export NETCDF_LIBRARY=$NETCDF_DIR/lib

#from GITR's main env file:
#module load cray-parallel-netcdf
#module load netcdf
#module load netcdf-cxx
##module load netcdf4
#PATH=$PATH:/home/tqd/code/netcdfBuild/bin:/home/tqd/code/netcdfcxx/bin
##prepend-path     PKG_CONFIG_PATH /home/dg6/code/netcdf/gnu/lib/pkgconfig 
#LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/tqd/code/netcdfBuild/bin:/home/tqd/code/netcdfcxx/bin
export NETCDF_CXX_BASEDIR=/opt/cray/pe/netcdf/4.6.1.3/GNU/8.2
#export  NETCDFCXX4=/home/tqd/code/netcdfcxx  
#export  NETCDFDIR=/home/tqd/code/netcdfBuild/lib 
#export  NETCDFCXX4DIR=/home/tqd/code/netcdfcxx/lib 
#export  NETCDFINCLUDE=/home/tqd/code/netcdfBuild/include 
#export  NETCDFCXX4INCLUDE=/home/tqd/code/netcdfcxx/include 
#export  NETCDFLIB=netcdf 
#export  NETCDFLIB_CPP=netcdf_c++
export PYTHONPATH=/global/homes/t/tyounkin/code/netcdfPython/lib.linux-x86_64-2.7:$PYTHONPATH


export ATOM=/project/projectdirs/atom

################
# Cori specfic
################

export ATOM_CORI=$ATOM/atom-install-cori
export GITR_PATH=$ATOM/atom-install-cori/GITR
export FTRIDYN_PATH=$ATOM/atom-install-cori/fractal-tridyn
#PATH=/global/homes/t/tyounkin/code/python2.7.14/bin/:$PATH

#PYTHONPATHS
export PYTHONPATH=$GITR_PATH/ftridyn:/global/homes/t/tyounkin/code/mpi4pyBuild/lib.linux-x86_64-2.7:$PYTHONPATH:$FTRIDYN_PATH/utils:$GITR_PATH/python:/project/projectdirs/atom/users/tyounkin/libconfPython/lib/python2.7/site-packages/

export PYTHONPATH=$PYTHONPATH:/global/homes/t/tyounkin/code/libconfPython/lib/python2.7/site-packages/
