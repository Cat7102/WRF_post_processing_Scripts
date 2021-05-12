#这个库禁止修改

import netCDF4 as nc
from wrf import getvar,to_np,ALL_TIMES
from datetime import datetime,timedelta

#这个函数用于获取nc文件的时间，同样不建议修改
def get_ncfile_time(ncfile,timezone=0):
    timelist=[]
    time = str(to_np(getvar(ncfile, 'times'))) #这个输出的时间是nc文件中最开始的时间，例如2016-07-21T00:00:00.000000000
    time = time[0:-10] #把最后一些无意义的东西筛掉
    times = getvar(ncfile, 'xtimes', timeidx=ALL_TIMES) #这个输出的是分钟的时间
    formal_datetime = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S') #格式化时间
    for i in times:
        timelist.append(str(formal_datetime + timedelta(minutes=int(i)+60*timezone))) #逐一把分钟加到最开始的时间上，并且格式化
    return timelist

def get_ncfile_alltime(ncfile):
    time = getvar(ncfile, 'xtimes', timeidx=ALL_TIMES) #这个输出的是分钟的时间
    print(int(time.shape[0]))
    return int(time.shape[0])

