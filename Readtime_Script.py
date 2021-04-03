#这个脚本仅用于读取时间

import netCDF4 as nc
from wrf import getvar,to_np,ALL_TIMES
from datetime import datetime,timedelta

#这个函数用于获取nc文件的时间，同样不建议修改
def get_ncfile_time(ncfile):
    timelist=[]
    time = str(to_np(getvar(ncfile, 'times'))) #这个输出的时间是nc文件中最开始的时间，例如2016-07-21T00:00:00.000000000
    time = time[0:-10] #把最后一些无意义的东西筛掉
    times = getvar(ncfile, 'xtimes', timeidx=ALL_TIMES) #这个输出的是分钟的时间
    formal_datetime = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S') #格式化时间
    for i in times:
        timelist.append(str(formal_datetime + timedelta(minutes=int(i)))) #逐一把分钟加到最开始的时间上，并且格式化，形成全部的utc时间
    return timelist

#仅需要修改一下文件的路径即可
ncfile=nc.Dataset('D:\Data\wrfout_d03_2016-07-21_00_00_00.nc')
timelist=get_ncfile_time(ncfile=ncfile)
for i in range(len(timelist)):
    print("["+str(i)+"]"+timelist[i])