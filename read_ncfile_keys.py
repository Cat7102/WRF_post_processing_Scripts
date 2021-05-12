#这个脚本仅用于读取ncfile的所有keys

import sys
sys.path.append("lib")
from GetKeys import get_ncfile_keys

#path:文件路径
#num:间隔多少个换行
path='D:\wrf_simulation\\2meic\wrfout_d03_2016-07-21_12_2meic'
num=6
print(get_ncfile_keys(path,num))