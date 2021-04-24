import netCDF4 as nc
import xarray as xr
import numpy as np
import cmaps
from wrf import getvar, to_np, ALL_TIMES
import Fontprocess
from Geo_Draw import Figure4wrf
import Readtime


#以下填写的内容，如果不需要不要进行注释，在最后一段注释不需要的功能即可
#初始化图片
fig_width=      10  #图片的宽
fig_height=     8   #图片高
fig_dpi=        150 #图片DPI
#图片的格式
ver_num,hor_num=    1,1 #一张图片显示子图的行数，列数
cur_num=            1   #第几个子图
title=              "中文宋体 英文Times New Roman 123"    #每个子图的标题
title_size=         12  #子图的标题
title_y=            1.03    #标题的高度
#地理信息
lake_opt=                               0   #0表示显示湖泊，1表示不显示
lake_linewidth,lake_linecolor =         0.8, 'black'    #湖泊的线宽和线的颜色
coastline_linewidth,coastline_color =   0.8, 'black'    #海岸线的线宽和颜色
precision=                              '10m'   #精度，10m，50m和110m，要加引号
#设置图片显示范围
l_x,r_x,b_y,t_y=    110, 130, 20, 40    #图片显示范围，分别是左右下上
more=               0.2     #图片extent的余量
#网格属性
grid_linewidth,grid_color,grid_type=                0.7, 'gray', ':'    #网格线宽，线颜色，线型（{'-', '--', '-.', ':', ''）
big_interval_x,big_interval_y =                     2, 2            #x和y轴的大间隔
small_interval_x,small_interval_y =                 0.2, 0.2            #x和y的小间隔，如果无需小间隔设置和大间隔相同即可
label_size,label_color =                            10, 'black'          #坐标轴字体大小和颜色
tick_length=                                        8                   #坐标轴的高度
#设置数据的变量，时间，高度
path='D:/wrfout_d01_2016-07-21_12-00-00_success'     #读取文件的路径
var_contourf, var_contour=     'o3','rh'    #填充的变量和绘制等高线的变量
chem_w=                         48          #摩尔质量，如果无需摩尔质量输入-1
var_u,var_v=                   'ua','va'    #风速的经度方向和纬度方向
time_num=                       42          #时间的序号
height_contourf, height_contour=0,0         #如果数据没有高度，那么随便填一个数字就行，不要空着
#读取填充数据
cmap=cmaps.amwg_blueyellowred                    #填色的颜色类型，具体参考colormap
contourf_opt=1                                   #是否使用默认填色,1表示是
level=np.arange(200, 8000, 100)                  #填色的最小值，最大值和间隔

#设置等高线数据
level2=np.arange(50, 100, 10)                                   #等高线最小值，最大值和间隔
contour_color,contour_width,contour_style="white",0.7,"solid"   #等高线颜色，宽度和种类（ 'solid', 'dashed', 'dashdot', 'dotted'）
fontsize,fontcolor,fontlabel,fontprecision=6,"white",0,'%1.0f'  #字体的大小，颜色，是否分开轮廓线（0表示是，1表示否），精度（'%1.3f'表示小数点后3位）
alpha=0.5                                                       #等高线的透明度，0~1之间

#矢量箭头图数据
interval=2                              #风速间隔多少网格点绘制
windspeed_height=0                      #如果是10m高的风速，那么这个参数就随便写，不会有影响
quiver_width,quiver_scale,quiver_color,quiver_headwidth=0.0018,60,'black',3    #箭头的线宽，大小（数字越大越小），颜色，箭头的宽度
alpha2=1                               #箭头的透明度，0~1之间
quiverkey_opt=0                         #是否显示quiverkey
quiverkey_x,quiverkey_y=0.93,1.01       #quiverkey的相对位置，x和y
quiverkey_ws,quiverkey_text,quiverkey_size=4,'4m/s',10   #quiverkey的标注风速，标注字体和字体大小
color_quiver=1
cmap=cmaps.amwg_blueyellowred
ws_map=[(0,1),(1,2),(2,3),(3,100)]

#色块图例数据
label_opt=1                                     #是否采用自定义的色块位置，0表示是，1表示否
rect_place,rect_more='left',0.2                 #设置空白子图的位置（bottom，top，right，left），数值表示空白多少，相对子图的比例
rect1,rect2,rect3,rect4=0.2, 0.1, 0.6, 0.03     #色块图例的位置
hv_opt='vertical'                               #图例垂直还是水平
colorbar_extend='both'                          #colorbar是否带箭头，'neither'和'both'
label_text='温度坐标(℃)'                        #图例写什么字
c_label_size,c_tick_size=8,8                   #标签字体大小,刻度字体大小

#图片保存数据
time_str=str(Readtime.get_ncfile_time(nc.Dataset(path),timezone=8)[time_num])  #读取文件的绘图的时间,timezone是时区
fig_path=str(time_str.replace(":","-"))+'.png'      #保存的文件名，如果需要自己修改则自行添加




fig=Figure4wrf(fig_width,fig_height,fig_dpi)
fig.init_draw(ver_num,hor_num,cur_num,title,title_size,title_y)
ncfile=nc.Dataset(path)
factor=getvar(ncfile,var_contourf,timeidx=time_num)
if factor>0:
    factor=factor*1000/22.4*chem_w*273.15/(getvar(ncfile,'tk',timeidx=time_num))
factor2=getvar(ncfile,var_contour,timeidx=time_num)
ws1=getvar(ncfile,var_u,timeidx=time_num)
ws2=getvar(ncfile,var_v,timeidx=time_num)
x=to_np(getvar(ncfile,'lon'))
y=to_np(getvar(ncfile,'lat'))
try:
    a=factor['bottom_top']
    factor=factor[height_contour,:,:]
    print('填充存在高度')
except:
    print("填充不存在高度")
try:
    a=factor2['bottom_top']
    factor2=factor2[height_contour,:,:]
    print('等高线存在高度')
except:
    print("等高线不存在高度")
try:
    a=ws1['bottom_top']
    ws1=ws1[height_contour,:,:]
    print('风速1存在高度')
except:
    print("风速1不存在高度")
try:
    a=ws2['bottom_top']
    ws2=ws2[height_contour,:,:]
    print('风速2存在高度')
except:
    print("风速2不存在高度")
#下面是执行函数部分，如果不需要某功能则可以注释，下面做简略介绍：
#   geo_draw：绘制地理信息
#   gridline_draw：绘制网格和坐标
#   contourf_draw：绘制等高线填充
#   contour_draw：绘制等高线轮廓
#   quiver_draw：绘制矢量箭头图
#   colorbar_draw：绘制色块图例
#   save_fig：保存图片
#   fig_show：展示图片
fig.geo_draw(lake_opt,lake_linewidth,lake_linecolor,coastline_linewidth,coastline_color,precision)
fig.extent_draw(l_x,r_x,b_y,t_y,more)
fig.gridline_draw(grid_linewidth,grid_color,grid_type,big_interval_x,big_interval_y,small_interval_x,small_interval_y,label_size,label_color,l_x,r_x,b_y,t_y,tick_length)
#fig.contourf_draw(x,y,factor,cmap,level,contourf_opt)
#fig.contour_draw(x,y,factor2,level2,contour_color,contour_width,contour_style,fontsize,fontcolor,fontlabel,fontprecision,alpha)
fig.quiver_draw(x,y,ws1,ws2,interval,quiver_width,quiver_scale,quiver_color,quiver_headwidth,alpha2,quiverkey_opt,quiverkey_x,quiverkey_y,quiverkey_ws,quiverkey_text,quiverkey_size,color_quiver=color_quiver,color_maps=cmap,ws_map=ws_map)
fig.colorbar_draw(rect1,rect2,rect3,rect4,label_opt,hv_opt,label_text,c_label_size,c_tick_size,rect_place,rect_more,colorbar_extend=colorbar_extend,ticks=ws_map,color_quiver=color_quiver)
#fig.save_fig(fig_path)
fig.fig_show()

