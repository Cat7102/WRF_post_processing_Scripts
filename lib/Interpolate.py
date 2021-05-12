import netCDF4 as nc
from wrf import getvar,ll_to_xy,to_np,vertcross,CoordPair,interplevel
from scipy.interpolate import Rbf
import numpy as np
import time

def calculate_wind_direction_array(ua_array,va_array):
    wdir_array = np.zeros_like(ua_array,dtype=float)
    for i in range(ua_array.shape[0]):#由于tan只能生成-90~90°的角度，而风速角度是0~360，因此需要做处理。其中正北为0度，顺时针为正。
        for j in range(ua_array.shape[1]):
            if ua_array[i,j]>=0 and va_array[i,j]>0:#第三象限
                wdir_array[i,j]=np.arctan(np.divide(ua_array[i,j],va_array[i,j]))*180/np.pi+180
            elif ua_array[i,j]<0 and va_array[i,j]>0:#第二象限
                wdir_array[i,j]=np.arctan(np.divide(ua_array[i,j],va_array[i,j]))*180/np.pi+180
            elif ua_array[i,j]>0 and va_array[i,j]<0:#第四象限
                wdir_array[i,j]=np.arctan(np.divide(ua_array[i,j],va_array[i,j]))*180/np.pi+360
            elif ua_array[i,j]>0 and va_array[i,j]==0:
                wdir_array[i,j]=270
            elif ua_array[i,j]<0 and va_array[i,j]==0:
                wdir_array[i,j]=90
            else:
                wdir_array[i,j]=np.arctan(np.divide(ua_array[i,j],va_array[i,j])) * 180/np.pi
    return wdir_array

def calculate_wind_direction(u,v):
    wdir=None
    if u>=0 and v>0:#第三象限
        wdir=np.arctan(np.divide(u,v))*180/np.pi+180
    elif u<0 and v>0:#第二象限
        wdir=np.arctan(np.divide(u,v))*180/np.pi+180
    elif u>0 and v<0:#第四象限
        wdir=np.arctan(np.divide(u,v))*180/np.pi+360
    elif u>0 and v==0:
        wdir=270
    elif u<0 and v==0:
        wdir=90
    else:
        wdir=np.arctan(np.divide(u,v)) * 180/np.pi
    return wdir

def get_nearest_4points(ncfile,point_lat,point_lon):
    we,sn=to_np(ll_to_xy(ncfile,point_lat,point_lon))
    nearest_point=(to_np(getvar(ncfile,'lat'))[sn,we],to_np(getvar(ncfile,'lon'))[sn,we])
    if nearest_point[0]<point_lat:
        sn1,sn2=sn,sn+1
    if nearest_point[0]>=point_lat:
        sn1,sn2=sn-1,sn
    if nearest_point[1]<point_lon:
        we1,we2=we,we+1
    if nearest_point[1]>=point_lon:
        we1,we2=we-1,we
    print("包围该点的四个最近点的索引：",end='')
    print((sn1,sn2,we1,we2))
    return (sn1,sn2,we1,we2),\
           (to_np(getvar(ncfile,'lat'))[sn1,we1],to_np(getvar(ncfile,'lon'))[sn1,we1]),\
           (to_np(getvar(ncfile,'lat'))[sn1,we2],to_np(getvar(ncfile,'lon'))[sn1,we2]),\
           (to_np(getvar(ncfile,'lat'))[sn2,we1],to_np(getvar(ncfile,'lon'))[sn2,we1]),\
           (to_np(getvar(ncfile,'lat'))[sn2,we2],to_np(getvar(ncfile,'lon'))[sn2,we2])

def interpolate(ncfile,f,point_lat,point_lon,opt=0):
    index, lb_point, rb_point, lt_point, rt_point = get_nearest_4points(ncfile, point_lat, point_lon)
    lat_list = np.array([lb_point[0], rb_point[0], lt_point[0], rt_point[0]])
    lon_list = np.array([lb_point[1], rb_point[1], lt_point[1], rt_point[1]])
    f_list = np.array([f[index[0], index[2]], f[index[0], index[3]], f[index[1], index[2]], f[index[1], index[3]]])
    if opt==0:
        di=np.sqrt((lat_list-point_lat)**2+(lon_list-point_lon)**2)
        weight=(1/di**2)/np.sum((1/di**2))
    if opt==1:
        wx = (point_lon - lon_list[0]) / (lon_list[1] - lon_list[0])
        wy = (point_lat - lat_list[0]) / (lat_list[2] - lat_list[0])
        w00 = (1 - wx) * (1 - wy)
        w01 = wx * (1 - wy)
        w10 = (1 - wx) * wy
        w11 = wx * wy
        weight = np.array([w00, w01, w10, w11])
    point_f=np.sum(f_list*weight)
    print("插值点的数值："+str(point_f))
    return point_f

def interpolate_grid(ncfile,f,point_lat_array,point_lon_array,opt=0):
    f_array=[]
    for i in range(len(point_lat_array)):
        f_templist=[]
        for j in range(len(point_lon_array)):
            f_templist.append(interpolate(ncfile,f,point_lat_array[i],point_lon_array[j],0))
            print("当前位置：",end='')
            print(i,j)
        f_array.insert(0,f_templist)
    return np.array(f_array)

def get_pressure_layer(pressure,start_p,end_p):
    start_layer,end_layer=None,None
    for i in range(len(pressure)):
        if pressure[i]<end_p:#end_p设置的是大的气压，具体原因是坐标轴的设置于相反的问题
            start_layer=i-1
            break
    for i in range(len(pressure)):
        if pressure[i]<start_p:#start_p设置的是小i的气压，具体原因是坐标轴的设置于相反的问题
            end_layer=i
            break
    print('原压力为：')
    print(pressure)
    bool=np.allclose(np.diff(pressure[start_layer:end_layer+1]),
                     (pressure[start_layer:end_layer+1][-1]-pressure[start_layer:end_layer+1][0])/(end_layer-start_layer+1))
    print('展示两数之差：')
    print(np.diff(pressure[start_layer:end_layer+1]))
    print((pressure[start_layer:end_layer+1][-1]-pressure[start_layer:end_layer+1][0])/(end_layer-start_layer+1))
    return bool,start_layer,end_layer

def interpolate_vert(ncfile,start_lat,end_lat,start_lon,end_lon,var,time,start_p,end_p,interval_p):
    startpoint = CoordPair(lat=start_lat, lon=start_lon)
    endpoint = CoordPair(lat=end_lat, lon=end_lon)
    height = getvar(ncfile, 'height')
    hgt = getvar(ncfile, 'HGT')
    p=getvar(ncfile,'pressure',timeidx=time)
    f=getvar(ncfile,var,timeidx=time)
    p_height = p[:, 0, 0]
    bool,start_layer,end_layer=get_pressure_layer(p_height,start_p,end_p)
    p_level = np.mgrid[p_height[start_layer].values:p_height[end_layer].values:complex(str(end_layer-start_layer+1) + 'j')]
    f_vert = vertcross(f, p, wrfin=ncfile,levels=p_level, start_point=startpoint, end_point=endpoint, latlon=True)
    if var=='wa':
        f_vert=f_vert*200
        print(f_vert)
    #处理插值数据的维度
    p_vert_list = f_vert.coords['vertical'].values
    print("插值的压力为：",end='')
    print(p_vert_list)
    lon_vert_list,lat_vert_list = [],[]
    for i in range(len(f_vert.coords['xy_loc'])):
        s = str(f_vert.coords['xy_loc'][i].values)
        lon_vert_list.append(float(s[s.find('lon=') + 4:s.find('lon=') + 16]))
        lat_vert_list.append(float(s[s.find('lat=') + 4:s.find('lat=') + 16]))
    lon_vert_list=np.array(lon_vert_list)
    lat_vert_list=np.array(lat_vert_list)
    lon_vert_list=np.around(lon_vert_list,decimals=2)
    lat_vert_list = np.around(lat_vert_list, decimals=2)
    h_vert_list = []
    h2h=height-hgt
    for i in range(end_p,start_p-interval_p,-interval_p):
        h_vert_list.append(float(np.max(interplevel(h2h, p, i)).values))
    print("对应的高度为：",end='')
    print(h_vert_list)
    lat_vert_list=np.mgrid[lat_vert_list[0]:lat_vert_list[-1]:complex(str(len(lat_vert_list)) + 'j')]
    lon_vert_list=np.mgrid[lon_vert_list[0]:lon_vert_list[-1]:complex(str(len(lon_vert_list)) + 'j')]
    return f_vert,lat_vert_list,lon_vert_list,p_vert_list,h_vert_list

