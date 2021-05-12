#这个脚本仅用于读取时间

import netCDF4 as nc
import sys
sys.path.append("lib")
from Readtime import get_ncfile_time

#仅需要修改一下文件的路径即可
ncfile=nc.Dataset('D:\wrf_simulation\\2meic\wrfout_d03_2016-07-21_12_2meic')
timelist=get_ncfile_time(ncfile=ncfile)
for i in range(len(timelist)):
    print("["+str(i)+"]"+timelist[i])