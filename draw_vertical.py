import netCDF4 as nc
import xarray as xr
from wrf import getvar,ll_to_xy,to_np,vertcross,CoordPair,interplevel
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeat
import matplotlib.ticker as mticker
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import cmaps
import matplotlib as mpl
from matplotlib.font_manager import FontProperties
import sys
sys.path.append("lib")
import Fontprocess,Readtime
import numpy as np
from matplotlib.colors import Normalize
Simsun = FontProperties(fname="./font/SimSun.ttf")
Times = FontProperties(fname="./font/Times.ttf")
mpl.rcParams['axes.unicode_minus']=False
config = {
    "mathtext.fontset":'stix',
}
mpl.rcParams.update(config)

ncfile=nc.Dataset('D:\wrf_simulation\\2meic\\wrfout_d03_2016-07-21_12_2meic')

time,time3,time4=123,126,129
start_lat,start_lon=31.2,121.39
end_lat,end_lon=31.5,121.575
small_p, big_p=800,1000
big_interval_x,big_interval_p=0.03,50
lat=getvar(ncfile,'lat')
lon=getvar(ncfile,'lon')
height=getvar(ncfile,'height')
hgt=getvar(ncfile,'HGT')
height2earth=height-hgt
cmap=cmaps.NCV_jaisnd
level=np.arange(40,410,10)

#################################################################################################
ua=getvar(ncfile,'ua',timeidx=time)
va=getvar(ncfile,'va',timeidx=time)
wa=getvar(ncfile,'wa',timeidx=time)
wa=wa*10
p=getvar(ncfile,'pressure',timeidx=time)
startpoint=CoordPair(lat=start_lat,lon=start_lon)
endpoint=CoordPair(lat=end_lat,lon=end_lon)

ua_vert=vertcross(ua,p,wrfin=ncfile,start_point=startpoint,end_point=endpoint,latlon=True)
va_vert=vertcross(va,p,wrfin=ncfile,start_point=startpoint,end_point=endpoint,latlon=True)
wa_vert=vertcross(wa,p,wrfin=ncfile,start_point=startpoint,end_point=endpoint,latlon=True)
f=getvar(ncfile,'o3',timeidx=time)
f = f * 1000 / 22.4 * 48 * 273.15 / (getvar(ncfile, 'tk', timeidx=time)) * (getvar(ncfile, 'pressure', timeidx=time)) / 1013.25
f_vert=vertcross(f,p,wrfin=ncfile,start_point=startpoint,end_point=endpoint,latlon=True)

lonlist,latlist,hlist=[],[],[]
plist=to_np(ua_vert.coords['vertical'])
for i in range(len(ua_vert.coords['xy_loc'])):
    s = str(ua_vert.coords['xy_loc'][i].values)
    lonlist.append(float(s[s.find('lon=')+4:s.find('lon=')+12]))
    latlist.append(float(s[s.find('lat=')+4:s.find('lat=')+12]))
for i in range(big_p,small_p-big_interval_p,-big_interval_p):
    hlist.append(float(np.max(interplevel(height2earth,p,i)).values))
hlist=np.array([int(i) for i in hlist])

fig=plt.figure(figsize=(10,8.5),dpi=150)
axe=plt.subplot(3,1,1) #这里可以设置多个子图，第一个参数表示多少行，第二个表示多少列，第三个表示第几个子图
axe.set_title(Fontprocess.zhSimsun_enTNR(str(Readtime.get_ncfile_time(ncfile,timezone=8)[time])),fontproperties=Simsun,fontsize=12,y=1.03)

str_lonlist,float_lonlist=[],[]
a=np.mgrid[0:len(lonlist)-1:complex(str(int(round((end_lon+big_interval_x-start_lon)/big_interval_x))) + 'j')]
a=np.around(a,decimals=0)
for i in range(int((end_lon+big_interval_x-start_lon)/big_interval_x)):
    float_lonlist.append(lonlist[int(a[i])])
    lo,la=round(lonlist[int(a[i])],2),round(latlist[int(a[i])],2)
    str_lonlist.append(str(lo)+'°E'+"\n"+str(la)+'°N')
axe.set_xlim(lonlist[0], lonlist[-1])
axe.set_ylim(small_p, big_p)  # 设置图的范围

#axe.grid(color='gray', linestyle=':', linewidth=0.7)
axe.invert_yaxis()#翻转纵坐标
plt.xticks(float_lonlist,str_lonlist,fontsize=8, color='black')  # 这一行代码用于修改刻度的字体
plt.xlabel('(a)',fontproperties=FontProperties(fname="./font/Times.ttf",size=10))
plt.yticks(fontsize=8, color='black')  # 这一行代码用于修改刻度的字体
#axe.get_xaxis().set_visible(False)
axe.set_yticks(np.arange(small_p,big_p+big_interval_p/2,big_interval_p))
axe.tick_params(labelcolor='black', length=3)
labels = axe.get_xticklabels() + axe.get_yticklabels()
[label.set_fontproperties(FontProperties(fname="./font/Times.ttf", size=8)) for label in labels]
axe.set_ylabel(Fontprocess.zhSimsun_enTNR('气压(hPa)'),fontproperties=Simsun,fontsize=9)

contourf = axe.contourf(lonlist, plist, f_vert,levels=level,cmap=cmap)

interval=1
interval_y=2
ua_vert,va_vert,wa_vert=to_np(ua_vert),to_np(va_vert),to_np(wa_vert)
ws_vert=np.sqrt(ua_vert**2+va_vert**2)
wdir_vert = np.arctan2(va_vert,ua_vert)*180/np.pi
line_angel=np.arctan2(end_lat-start_lat,end_lon-start_lon)*180/np.pi
vl_angel=wdir_vert-line_angel
vl_angel=np.cos(vl_angel/180*np.pi)
ws_vert=ws_vert*vl_angel
x,y1=[],[]
y, ws1, ws2 = plist.tolist(), ws_vert[::interval_y, ::interval], wa_vert[::interval_y,::interval]
for i in range(len(y[::interval_y])):
    x.append(lonlist[::interval])
for i in range(len(lonlist[::interval])):
    y1.append(y[::interval_y])
y=np.array(y1)
y=y.T
x=np.array(x)

quiver = axe.quiver(x, y, ws1, ws2, pivot='mid',
                         width=0.001, scale=150, color='black', headwidth=4,
                         alpha=1)
'''
axe_2=axe.twinx()
axe_2.set_ylim(hlist[0],hlist[-1])
axe_2.set_yticks(np.mgrid[hlist[0]:hlist[-1]:complex(str(int(hlist.shape[0])) + 'j')])
round_hlist=np.around(hlist,-1)
axe_2.set_yticklabels(round_hlist)
axe_2.tick_params(labelcolor='black', length=3)
labels = axe_2.get_xticklabels() + axe_2.get_yticklabels()
[label.set_fontproperties(FontProperties(fname="./font/Times.ttf", size=8)) for label in labels]
'''
#################################################################################################

#################################################################################################
time_=time3
ua=getvar(ncfile,'ua',timeidx=time_)
va=getvar(ncfile,'va',timeidx=time_)
wa=getvar(ncfile,'wa',timeidx=time_)
wa=wa*10
p=getvar(ncfile,'pressure',timeidx=time_)
startpoint=CoordPair(lat=start_lat,lon=start_lon)
endpoint=CoordPair(lat=end_lat,lon=end_lon)

ua_vert=vertcross(ua,p,wrfin=ncfile,start_point=startpoint,end_point=endpoint,latlon=True)
va_vert=vertcross(va,p,wrfin=ncfile,start_point=startpoint,end_point=endpoint,latlon=True)
wa_vert=vertcross(wa,p,wrfin=ncfile,start_point=startpoint,end_point=endpoint,latlon=True)
f=getvar(ncfile,'o3',timeidx=time_)
f = f * 1000 / 22.4 * 48 * 273.15 / (getvar(ncfile, 'tk', timeidx=time_)) * (getvar(ncfile, 'pressure', timeidx=time_)) / 1013.25
f_vert=vertcross(f,p,wrfin=ncfile,start_point=startpoint,end_point=endpoint,latlon=True)

axe=plt.subplot(3,1,2) #这里可以设置多个子图，第一个参数表示多少行，第二个表示多少列，第三个表示第几个子图
axe.set_title(Fontprocess.zhSimsun_enTNR(str(Readtime.get_ncfile_time(ncfile,timezone=8)[time_])),fontproperties=Simsun,fontsize=12,y=1.03)

str_lonlist,float_lonlist=[],[]
a=np.mgrid[0:len(lonlist)-1:complex(str(int(round((end_lon+big_interval_x-start_lon)/big_interval_x))) + 'j')]
a=np.around(a,decimals=0)
for i in range(int((end_lon+big_interval_x-start_lon)/big_interval_x)):
    float_lonlist.append(lonlist[int(a[i])])
    lo,la=round(lonlist[int(a[i])],2),round(latlist[int(a[i])],2)
    str_lonlist.append(str(lo)+'°E'+"\n"+str(la)+'°N')
axe.set_xlim(lonlist[0], lonlist[-1])
axe.set_ylim(small_p, big_p)  # 设置图的范围

axe.invert_yaxis()#翻转纵坐标
plt.xticks(float_lonlist,str_lonlist,fontsize=8, color='black')  # 这一行代码用于修改刻度的字体
plt.xlabel('(b)',fontproperties=FontProperties(fname="./font/Times.ttf",size=10))
plt.yticks(fontsize=8, color='black')  # 这一行代码用于修改刻度的字体
axe.set_yticks(np.arange(small_p,big_p+big_interval_p/2,big_interval_p))
axe.tick_params(labelcolor='black', length=3)
#axe.get_xaxis().set_visible(False)
labels = axe.get_xticklabels() + axe.get_yticklabels()
[label.set_fontproperties(FontProperties(fname="./font/Times.ttf", size=8)) for label in labels]
axe.set_ylabel(Fontprocess.zhSimsun_enTNR('气压(hPa)'),fontproperties=Simsun,fontsize=9)

contourf = axe.contourf(lonlist, plist, f_vert,levels=level,cmap=cmap)

interval=1
interval_y=2
ua_vert,va_vert,wa_vert=to_np(ua_vert),to_np(va_vert),to_np(wa_vert)
ws_vert=np.sqrt(ua_vert**2+va_vert**2)
wdir_vert = np.arctan2(va_vert,ua_vert)*180/np.pi
line_angel=np.arctan2(end_lat-start_lat,end_lon-start_lon)*180/np.pi
vl_angel=wdir_vert-line_angel
vl_angel=np.cos(vl_angel/180*np.pi)
ws_vert=ws_vert*vl_angel
x,y1=[],[]
y, ws1, ws2 = plist.tolist(), ws_vert[::interval_y, ::interval], wa_vert[::interval_y,::interval]
for i in range(len(y[::interval_y])):
    x.append(lonlist[::interval])
for i in range(len(lonlist[::interval])):
    y1.append(y[::interval_y])
y=np.array(y1)
y=y.T
x=np.array(x)

quiver = axe.quiver(x, y, ws1, ws2, pivot='mid',
                    width=0.001, scale=150, color='black', headwidth=4,alpha=1)

#################################################################################################

#################################################################################################
time_=time4
ua=getvar(ncfile,'ua',timeidx=time_)
va=getvar(ncfile,'va',timeidx=time_)
wa=getvar(ncfile,'wa',timeidx=time_)
wa=wa*10
p=getvar(ncfile,'pressure',timeidx=time_)
startpoint=CoordPair(lat=start_lat,lon=start_lon)
endpoint=CoordPair(lat=end_lat,lon=end_lon)

ua_vert=vertcross(ua,p,wrfin=ncfile,start_point=startpoint,end_point=endpoint,latlon=True)
va_vert=vertcross(va,p,wrfin=ncfile,start_point=startpoint,end_point=endpoint,latlon=True)
wa_vert=vertcross(wa,p,wrfin=ncfile,start_point=startpoint,end_point=endpoint,latlon=True)
f=getvar(ncfile,'o3',timeidx=time_)
f = f * 1000 / 22.4 * 48 * 273.15 / (getvar(ncfile, 'tk', timeidx=time_)) * (getvar(ncfile, 'pressure', timeidx=time_)) / 1013.25
f_vert=vertcross(f,p,wrfin=ncfile,start_point=startpoint,end_point=endpoint,latlon=True)

axe=plt.subplot(3,1,3) #这里可以设置多个子图，第一个参数表示多少行，第二个表示多少列，第三个表示第几个子图
axe.set_title(Fontprocess.zhSimsun_enTNR(str(Readtime.get_ncfile_time(ncfile,timezone=8)[time_])),fontproperties=Simsun,fontsize=12,y=1.03)

str_lonlist,float_lonlist=[],[]
a=np.mgrid[0:len(lonlist)-1:complex(str(int(round((end_lon+big_interval_x-start_lon)/big_interval_x))) + 'j')]
a=np.around(a,decimals=0)
for i in range(int((end_lon+big_interval_x-start_lon)/big_interval_x)):
    float_lonlist.append(lonlist[int(a[i])])
    lo,la=round(lonlist[int(a[i])],2),round(latlist[int(a[i])],2)
    str_lonlist.append(str(lo)+'°E'+"\n"+str(la)+'°N')
axe.set_xlim(lonlist[0], lonlist[-1])
axe.set_ylim(small_p, big_p)  # 设置图的范围

axe.invert_yaxis()#翻转纵坐标
plt.xticks(float_lonlist,str_lonlist,fontsize=8, color='black')  # 这一行代码用于修改刻度的字体
plt.xlabel('(c)',fontproperties=FontProperties(fname="./font/Times.ttf",size=10))
plt.yticks(fontsize=8, color='black')  # 这一行代码用于修改刻度的字体
axe.set_yticks(np.arange(small_p,big_p+big_interval_p/2,big_interval_p))
axe.tick_params(labelcolor='black', length=3)
labels = axe.get_xticklabels() + axe.get_yticklabels()
[label.set_fontproperties(FontProperties(fname="./font/Times.ttf", size=8)) for label in labels]
axe.set_ylabel(Fontprocess.zhSimsun_enTNR('气压(hPa)'),fontproperties=Simsun,fontsize=9)

contourf = axe.contourf(lonlist, plist, f_vert,levels=level,cmap=cmap)

interval=1
interval_y=2
ua_vert,va_vert,wa_vert=to_np(ua_vert),to_np(va_vert),to_np(wa_vert)
ws_vert=np.sqrt(ua_vert**2+va_vert**2)
wdir_vert = np.arctan2(va_vert,ua_vert)*180/np.pi
line_angel=np.arctan2(end_lat-start_lat,end_lon-start_lon)*180/np.pi
vl_angel=wdir_vert-line_angel
vl_angel=np.cos(vl_angel/180*np.pi)
ws_vert=ws_vert*vl_angel
x,y1=[],[]
y, ws1, ws2 = plist.tolist(), ws_vert[::interval_y, ::interval], wa_vert[::interval_y,::interval]
for i in range(len(y[::interval_y])):
    x.append(lonlist[::interval])
for i in range(len(lonlist[::interval])):
    y1.append(y[::interval_y])
y=np.array(y1)
y=y.T
x=np.array(x)

quiver = axe.quiver(x, y, ws1, ws2, pivot='mid',
                    width=0.001, scale=150, color='black', headwidth=4,alpha=1)

#################################################################################################

fig.subplots_adjust(right=0.8)
rect = [0.84, 0.1, 0.01, 0.6]  # 分别代表，水平位置，垂直位置，水平宽度，垂直宽度
cbar_ax = fig.add_axes(rect)
cb = fig.colorbar(contourf, drawedges=True, cax=cbar_ax, orientation='vertical',spacing='uniform')  # orientation='vertical'
cb.set_label(Fontprocess.zhSimsun_enTNR("O_{3}浓度(ug/m^3)"), fontproperties=Simsun, fontsize=10)
cb.ax.tick_params(length=2)
# 下面两行是指定colorbar刻度字体的方法，绘图的坐标也同样适用
# 下面两行是指定colorbar刻度字体的方法，绘图的坐标也同样适用
labels = cb.ax.get_xticklabels() + cb.ax.get_yticklabels()
[label.set_fontproperties(FontProperties(fname="./font/Times.ttf", size=8)) for label in labels]
level2=np.arange(40,410,20)
cb.set_ticks(level2)

axe_5=fig.add_axes([0.8,0.74,0.14,0.14],projection=ccrs.PlateCarree())
axe_5.add_feature(cfeat.COASTLINE.with_scale("10m"), linewidth=0.7,color="black")
axe_5.set_extent([120.7, 122.1, 30.5, 32], crs=ccrs.PlateCarree())
axe_5.plot([lonlist[0],lonlist[-1]],[latlist[0],latlist[-1]],color='red')
axe_5.plot(lonlist[0],latlist[0],marker='o',color='red',markersize=2.5)
axe_5.plot(lonlist[-1],latlist[-1],marker='o',color='red',markersize=2.5)
axe_5.text(lonlist[1]-0.15,latlist[1]-0.15,'C',fontproperties=FontProperties(fname="./font/Times.ttf", size=8))
axe_5.text(lonlist[-1]+0.05,latlist[-1]+0.05,'C'+"'",fontproperties=FontProperties(fname="./font/Times.ttf", size=8))

plt.subplots_adjust(wspace=0.2, hspace=0.55)

fig.savefig("剖面图-o3-baoshan",dpi=500)
fig.show()
plt.show()
