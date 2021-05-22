import netCDF4 as nc
import numpy as np
import cmaps
from wrf import getvar, to_np, CoordPair, vertcross, interplevel
import sys
sys.path.append("lib")
from Vert_Draw import Figure4wrf
import Readtime

#以下填写的内容，如果不需要不要进行注释，在最后一段注释不需要的功能即可
#初始化图片
fig_width=      10  #图片的宽
fig_height=     6   #图片高
fig_dpi=        180 #图片DPI

#图片的格式
ver_num,hor_num=    3,1 #一张图片显示子图的行数，列数
cur_num=            1   #第几个子图，用于标记
title = "O_{3} and Wind"  # 子图的标题，如果需要循环作图建议放在下方循环内
title_size=         12  #子图的标题
title_y=            1.03    #标题的高度

#设置图片显示范围
small_p,big_p=800, 1000             #图片显示范围，分别是气压的最小和最大值
start_lat,start_lon=31.2,121.39     #插值线条的起始经纬度
end_lat,end_lon=31.5,121.575        #插值线条的末经纬度
#网格属性
grid_linewidth,grid_color,grid_type=                0, 'gray', ':'    #网格线宽（0表示无网格），线颜色，线型（{'-', '--', '-.', ':', ''）
big_interval_lon,big_interval_p =                   0.03,50            #x和y轴的大间隔
xlabelsize,ylabelsize =                            9, 9          #坐标轴字体大小
xaxis_show=                                        True                   #坐标轴的高度
xlabellist=['(a)','(b)','(c)']                                    #x坐标上要添加的东西，如果不需要那么就注释
ylabel='气压(hPa)'                                                   #y轴标签内容
tick_length = 2                                                         #x轴和y轴tick的伸出长度
ticks_size=8                                                        #x和y轴刻度的大小
ticks_color='black'                                                 #x和y轴刻度字体颜色

#设置数据的变量，时间，高度
path='D:\wrf_simulation\\2meic\\wrfout_d03_2016-07-21_12_2meic'     #读取文件的路径
var_contourf=     'o3'    #填充的变量
chem_w=           48          #摩尔质量，如果无需摩尔质量输入小于等于0的数字
timelist=[117,120,123]                   #时间的列表

#读取填充数据
cmap=cmaps.NCV_jaisnd                    #填色的颜色类型，具体参考colormap
level=np.arange(40,410,10)                  #填色的最小值，最大值和间隔
ticks=np.arange(40,410,20)                    #设置colorbar的ticks，如果不需要写成None
colorbar_extend='neither'                          #colorbar是否带箭头，'neither'和'both'

#矢量箭头图数据
interval,interval_y=1,2                 #风速间隔多少网格点绘制,分别表示x轴和y轴上的间隔
wa_beilv=10                             #垂直风速的倍率
quiver_width,quiver_scale,quiver_color,quiver_headwidth=0.001,150,'black',4    #箭头的线宽，大小（数字越大越小），颜色，箭头的宽度
alpha=1                               #箭头的透明度，0~1之间

#色块图例数据
rect_place,rect_more='right',0.8                 #设置空白子图的位置（bottom，top，right，left），数值表示空白多少，相对子图的比例
rect1,rect2,rect3,rect4=0.84, 0.1, 0.01, 0.6     #色块图例的位置,分别是 水平位置，垂直位置，水平宽度，垂直宽度
hv_opt='vertical'                               #图例垂直还是水平
label_text='O_{3}浓度(ug/m^3)'                        #图例写什么字
c_label_size,c_tick_size=8,8                   #标签字体大小,刻度字体大小
drawedges_bool=True                              #决定颜色边界是否要画上黑色的线条，False表示否，True表示是
colorbar_ticklength=2                           #colorbar的tick突出长度，如果是0就是不突出

#添加小地图
smap_horpos,smap_verpos,smap_horlen,smap_verlen=0.8,0.74,0.14,0.14
coastline_width,coastline_color=0.7,'black'
smap_startlat,smap_endlat,smap_startlon,smap_endlon=30.5, 32, 120.7, 122.1
plot_color,plot_linewidth,plot_linestyle='red',1,'dashed'
marker,marker_color,marker_size='o','red',2.5
textlist=[[start_lon,start_lat,'A',8],[end_lon,end_lat,'A'+"'",8]]

#调整子图间距
wspace,hspace=0.25,0.5  #设置了子图的横向间距和纵向间距

#图片保存数据
fig_path="图1.png"
save_dpi=500            #设置了保存图片的DPI值


ncfile=nc.Dataset(path)
lat=getvar(ncfile,'lat')
lon=getvar(ncfile,'lon')
height=getvar(ncfile,'height')
hgt=getvar(ncfile,'HGT')
height2earth=height-hgt
startpoint = CoordPair(lat=start_lat, lon=start_lon)
endpoint = CoordPair(lat=end_lat, lon=end_lon)
fig = Figure4wrf(fig_width, fig_height, fig_dpi)
for cur_num in range(ver_num*hor_num):
    i=timelist[cur_num]
    title=i
    #数据修改在下面
    factor=getvar(ncfile,var_contourf,timeidx=i)  #如果是华氏度之类的物理量需要换算，可以自行进行修改factor的值
    if chem_w > 0:
        factor = factor * 1000 / 22.4 * chem_w * 273.15 / (getvar(ncfile, 'tk', timeidx=i)) * (getvar(ncfile, 'pressure', timeidx=i)) / 1013.25
    ua = getvar(ncfile, 'ua', timeidx=i)
    va = getvar(ncfile, 'va', timeidx=i)
    wa = getvar(ncfile, 'wa', timeidx=i)
    wa = wa * 10
    p = getvar(ncfile, 'pressure', timeidx=i)
    f_vert = vertcross(factor, p, wrfin=ncfile, start_point=startpoint, end_point=endpoint, latlon=True)
    ua_vert = vertcross(ua, p, wrfin=ncfile, start_point=startpoint, end_point=endpoint, latlon=True)
    va_vert = vertcross(va, p, wrfin=ncfile, start_point=startpoint, end_point=endpoint, latlon=True)
    wa_vert = vertcross(wa, p, wrfin=ncfile, start_point=startpoint, end_point=endpoint, latlon=True)
    x = to_np(getvar(ncfile, 'lon'))
    y = to_np(getvar(ncfile, 'lat'))
    xlabel = xlabellist[cur_num]
    lonlist, latlist, hlist = [], [], []
    plist = to_np(ua_vert.coords['vertical'])
    for i in range(len(ua_vert.coords['xy_loc'])):
        s = str(ua_vert.coords['xy_loc'][i].values)
        lonlist.append(float(s[s.find('lon=') + 4:s.find('lon=') + 12]))
        latlist.append(float(s[s.find('lat=') + 4:s.find('lat=') + 12]))
    for i in range(big_p, small_p - big_interval_p, -big_interval_p):
        hlist.append(float(np.max(interplevel(height2earth, p, i)).values))
    hlist = np.array([int(i) for i in hlist])
    str_lonlist, float_lonlist = [], []
    a = np.mgrid[0:len(lonlist) - 1:complex(str(int(round((end_lon + big_interval_lon - start_lon) / big_interval_lon))) + 'j')]
    a = np.around(a, decimals=0)
    for i in range(int((end_lon + big_interval_lon - start_lon) / big_interval_lon)):
        float_lonlist.append(lonlist[int(a[i])])
        lo, la = round(lonlist[int(a[i])], 2), round(latlist[int(a[i])], 2)
        str_lonlist.append(str(lo) + '°E' + "\n" + str(la) + '°N')

    #这里的title可以进行修改
    title = str(Readtime.get_ncfile_time(ncfile,timezone=8)[i])+"  O_{3} and Wind"  # 每个子图的标题

    fig.init_draw(ver_num,hor_num,cur_num+1,title,title_size,title_y)
    #下面是执行函数部分，如果不需要某功能则可以注释，下面做简略介绍：
    #   gridline_draw：绘制网格和坐标
    #   contourf_draw：绘制等高线填充
    #   contour_draw：绘制等高线轮廓
    #   quiver_draw：绘制矢量箭头图
    #   colorbar_draw：绘制色块图例
    #   save_fig：保存图片
    #   fig_show：展示图片
    fig.extent_draw(start_lon, end_lon, small_p, big_p)
    fig.gridline_draw(grid_linewidth, grid_color, grid_type, float_lonlist, str_lonlist, ticks_size,ticks_color,small_p, big_p, big_interval_p, tick_length,ylabel=ylabel,xaxis_show=xaxis_show,ylabelsize=ylabelsize, xlabel=xlabel, xlabelsize=xlabelsize)
    fig.contourf_draw(lonlist,plist,f_vert,cmap,level,extend=colorbar_extend)
    fig.quiver_draw(ua_vert,va_vert,wa_vert,lonlist,plist,interval,interval_y,start_lat,end_lat,start_lon,end_lon,quiver_width,quiver_scale,quiver_color,quiver_headwidth,alpha)

#由于此处colorbar是绘制一个统一的，因此放在循环外部
fig.colorbar_draw(rect1, rect2, rect3, rect4, hv_opt, label_text, c_label_size, c_tick_size, rect_place, rect_more, ticks=ticks, drawedges_bool=drawedges_bool, colorbar_ticklength=colorbar_ticklength)
fig.smallmap_draw(smap_horpos,smap_verpos,smap_horlen,smap_verlen,coastline_width,coastline_color,smap_startlat,smap_endlat,smap_startlon,smap_endlon,latlist[0],latlist[-1],lonlist[0],lonlist[-1],plot_color,plot_linewidth,plot_linestyle,marker,marker_color,marker_size,textlist)
fig.adjust_subplot(wspace,hspace)
fig.save_fig(fig_path,save_dpi=save_dpi)
fig.fig_show()