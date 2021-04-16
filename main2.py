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
title_size=         12  #子图的标题
title_y=            1.03    #标题的高度
#地理信息
lake_opt=                               0   #0表示显示湖泊，1表示不显示
lake_linewidth,lake_linecolor =         0.8, 'black'    #湖泊的线宽和线的颜色
coastline_linewidth,coastline_color =   0.8, 'black'    #海岸线的线宽和颜色
precision=                              '10m'   #精度，10m，50m和110m，要加引号
#设置图片显示范围
l_x,r_x,b_y,t_y=    120.5, 122.5, 30.3, 32.3    #图片显示范围，分别是左右下上
more=               0.1     #图片extent的余量
geo_opt=            0       #是否绘制地理平面图，0表示是，1表示否
#网格属性
grid_linewidth,grid_color,grid_type=                0.7, 'gray', ':'    #网格线宽，线颜色，线型（{'-', '--', '-.', ':', ''）
big_interval_x,big_interval_y =                     0.5, 0.5            #x和y轴的大间隔
small_interval_x,small_interval_y =                 0.1, 0.1            #x和y的小间隔，如果无需小间隔设置和大间隔相同即可
top_labels,bottom_labels,left_labels,right_labels=  1, 0, 0, 1          #是否隐藏上下左右的坐标，1表示隐藏，0显示
label_size,label_color =                            8, 'black'          #坐标轴字体大小和颜色
#读取填充数据
timestart,timeend,timestep=294,432,2               #设置循环开始的时间，结束的时间和时间步长
path='E:/wrfout_d03_2016-07-21_00-00-00'     #读取文件的路径
ncfile=nc.Dataset(path)     #这行别动
x=getvar(ncfile,'lon')                          #x是经度，y是纬度，也可以自行修改
y=getvar(ncfile,'lat')
cmap=cmaps.amwg_blueyellowred                         #填色的颜色类型，具体参考colormap
level=np.arange(0.002, 800, 2)                  #填色的最小值，最大值和间隔
#设置等高线数据
level2=np.arange(50, 100, 10)                                   #等高线最小值，最大值和间隔
contour_color,contour_width,contour_style="white",0.7,"solid"   #等高线颜色，宽度和种类（ 'solid', 'dashed', 'dashdot', 'dotted'）
fontsize,fontcolor,fontlabel,fontprecision=6,"white",0,'%1.0f'  #字体的大小，颜色，是否分开轮廓线（0表示是，1表示否），精度（'%1.3f'表示小数点后3位）
alpha=0.5                                                       #等高线的透明度，0~1之间
#矢量箭头图数据
interval=2                              #间隔多少网格点绘制
quiver_width,quiver_scale,quiver_color,quiver_headwidth=0.0018,200,'black',3    #箭头的线宽，大小（数字越大越小），颜色，箭头的宽度
alpha2=0.7                               #箭头的透明度，0~1之间
quiverkey_opt=0                         #是否显示quiverkey
quiverkey_x,quiverkey_y=0.93,1.01       #quiverkey的相对位置，x和y
quiverkey_ws,quiverkey_text,quiverkey_size=4,'4m/s',8   #quiverkey的标注风速，标注字体和字体大小
#色块图例数据
label_opt=1                                     #是否采用自定义的色块位置，0表示是，1表示否
rect_place,rect_more='left',0.2                 #设置空白子图的位置（bottom，top，right，left），数值表示空白多少，相对子图的比例
rect1,rect2,rect3,rect4=0.2, 0.1, 0.6, 0.03     #色块图例的位置
hv_opt='vertical'                               #图例垂直还是水平
label_text='no2(ppmv)'                        #图例写什么字
c_label_size,c_tick_size=8,8                   #标签字体大小,刻度字体大小

timelist=Readtime.get_ncfile_time(ncfile,timezone=8)
print(timelist)
for i in range(timestart,timeend+1,timestep):
    #数据修改在下面
    factor=getvar(ncfile,'PM10',timeidx=i)[0,:,:]           #需要绘制填色的变量
    #factor=getvar(ncfile,'T2',timeidx=i)
    #factor=factor-273.15
    factor2=getvar(ncfile,'rh2',timeidx=i)                         #等高线变量
    ws1=ncfile.variables['U10'][i,:,:]     #箭头图的风速u和v的读取
    ws2=ncfile.variables['V10'][i,:,:]
    #修改一些图纸信息
    title = str(timelist[i])  # 每个子图的标题
    # 图片保存数据
    time = str(timelist[i])  # 读取文件的绘图的时间
    print(time)
    fig_path = str(time.replace(":", "-"))+'pm' + '.png'  # 保存的文件名，如果需要自己修改则自行添加

    fig=Figure4wrf(fig_width,fig_height,fig_dpi)
    fig.init_draw(ver_num,hor_num,cur_num,title,title_size,title_y)\
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
    fig.extent_draw(l_x,r_x,b_y,t_y,more,geo_opt)
    fig.gridline_draw(grid_linewidth,grid_color,grid_type,big_interval_x,big_interval_y,small_interval_x,small_interval_y,top_labels,bottom_labels,left_labels,right_labels,label_size,label_color,geo_opt,l_x,r_x,b_y,t_y)
    fig.contourf_draw(x,y,factor,cmap,level)
    #fig.contour_draw(x,y,factor2,level2,contour_color,contour_width,contour_style,fontsize,fontcolor,fontlabel,fontprecision,alpha)
    fig.quiver_draw(x,y,ws1,ws2,interval,quiver_width,quiver_scale,quiver_color,quiver_headwidth,alpha2,geo_opt,quiverkey_opt,quiverkey_x,quiverkey_y,quiverkey_ws,quiverkey_text,quiverkey_size)
    fig.colorbar_draw(rect1,rect2,rect3,rect4,label_opt,hv_opt,label_text,c_label_size,c_tick_size,rect_place,rect_more)
    fig.save_fig(fig_path)
    #fig.fig_show()

