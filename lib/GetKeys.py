import netCDF4 as nc
import numpy as np

def get_ncfile_keys(path,num):
    ncfile=nc.Dataset(path)
    n=1
    key_list,key_list_temp=[],[]
    for i in ncfile.variables.keys():
        i=' '+i+' '
        key_list_temp.append(i)
        if n%num==0:
            key_list.append(key_list_temp)
            key_list_temp=[]
        if n==len(ncfile.variables.keys()):
            key_list.append(key_list_temp)
        n+=1
    return np.array(key_list,dtype=object)
