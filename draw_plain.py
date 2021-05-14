import netCDF4 as nc
import numpy as np
import cmaps
from wrf import getvar, to_np
import sys
sys.path.append("lib")
from Geo_Draw import Figure4wrf
import Readtime

#以下填写的内容，如果不需要不要进行注释，在最后一段注释不需要的功能即可
#初始化图片
fig_width=      10  #图片的宽
fig_height=     6   #图片高
fig_dpi=        180 #图片DPI
#图片的格式
ver_num,hor_num=    2,2 #一张图片显示子图的行数，列数
cur_num=            1   #第几个子图，用于标记
title = "O_{3} and Wind"  # 子图的标题，如果需要循环作图建议放在下方循环内
title_size=         8.5  #子图的标题
title_y=            1.04    #标题的高度
#地理信息
lake_opt=                               0   #0表示显示湖泊，1表示不显示
lake_linewidth,lake_linecolor =         0.8, 'black'    #湖泊的线宽和线的颜色
coastline_linewidth,coastline_color =   0.8, 'black'    #海岸线的线宽和颜色
precision=                              '10m'   #精度，10m，50m和110m，要加引号
#设置图片显示范围
l_x,r_x,b_y,t_y=    120.8, 122.2, 30.6, 31.8    #图片显示范围，分别是左右下上
more=               0.1     #图片extent的余量
#网格属性
grid_linewidth,grid_color,grid_type=                0, 'gray', ':'    #网格线宽（0表示无网格），线颜色，线型（{'-', '--', '-.', ':', ''）
big_interval_x,big_interval_y =                     0.3, 0.3            #x和y轴的大间隔
small_interval_x,small_interval_y =                 0.3, 0.3            #x和y的小间隔，如果无需小间隔设置和大间隔相同即可
label_size,label_color =                            6, 'black'          #坐标轴字体大小和颜色
tick_length=                                        6                   #坐标轴的高度
xlabellist=['(a)','(b)','(c)','(d)']                                    #x坐标上要添加的东西，如果不需要那么把下面的字体大小改成0
xlabelsize = 10                                                         #x坐标轴的字体大小
#设置数据的变量，时间，高度
path='D:\wrf_simulation\\2meic\\wrfout_d03_2016-07-21_12_2meic'     #读取文件的路径
var_contourf, var_contour=     'o3','rh'    #填充的变量和绘制等高线的变量
chem_w=                         48          #摩尔质量，如果无需摩尔质量输入小于等于0的数字
var_u,var_v=                   'ua','va'    #风速的经度方向和纬度方向
timelist=range(120,132,3)                   #时间的列表，起始，重点，间隔多少
height_contourf, height_contour=0,0         #如果数据没有高度，那么随便填一个数字就行，不要空着

#读取填充数据
cmap=cmaps.NCV_jaisnd                    #填色的颜色类型，具体参考colormap
contourf_opt=0                                   #是否使用默认填色,1表示是
level=np.arange(120, 410, 10)                  #填色的最小值，最大值和间隔
ticks=np.arange(120, 410, 20)                    #设置colorbar的ticks，如果不需要写成None
colorbar_extend='neither'                          #colorbar是否带箭头，'neither'和'both'

#设置等高线数据
level2=np.arange(30, 105, 5)                                   #等高线最小值，最大值和间隔
contour_color,contour_width,contour_style="white",0.8,"solid"   #等高线颜色，宽度和种类（ 'solid', 'dashed', 'dashdot', 'dotted'）
fontsize,fontcolor,fontlabel,fontprecision=0,"white",2,'%1.0f'  #字体的大小，颜色，是否分开轮廓线（0表示是，1表示否），精度（'%1.3f'表示小数点后3位）
alpha=1                                                       #等高线的透明度，0~1之间
contour_opt=0                                                   #0表示不用cmap，1表示用。如果用了1，那么colorbar会默认用contour的cmaps
contour_cmaps=cmaps.seaice_2_r                          #contour用的cmap

#矢量箭头图数据
interval=3                              #风速间隔多少网格点绘制
windspeed_height=0                      #如果是10m高的风速，那么这个参数就随便写，不会有影响
quiver_width,quiver_scale,quiver_color,quiver_headwidth=0.0025,100,'black',4    #箭头的线宽，大小（数字越大越小），颜色，箭头的宽度
alpha2=1                               #箭头的透明度，0~1之间
quiverkey_opt=0                         #是否显示quiverkey
quiverkey_x,quiverkey_y=0.87,1.03       #quiverkey的相对位置，x和y
quiverkey_ws,quiverkey_text,quiverkey_size=4,'4m/s',7   #quiverkey的标注风速，标注字体和字体大小
color_quiver=0                          #这个与cmap_quiver以及ws_map共用，如果需要用颜色来表示风速箭头，那么这里改成1
cmap_quiver=cmaps.amwg_blueyellowred    #quiver的cmap
ws_map=[(0,1),(1,2),(2,3),(3,100)]      #风速cmap对应的几档风速变色

#色块图例数据
label_opt=0                                     #是否采用自定义的色块位置，0表示是，1表示否
rect_place,rect_more='right',0.7                 #设置空白子图的位置（bottom，top，right，left），数值表示空白多少，相对子图的比例
rect1,rect2,rect3,rect4=0.75, 0.15, 0.01, 0.65     #色块图例的位置,分别是 水平位置，垂直位置，水平宽度，垂直宽度
hv_opt='vertical'                               #图例垂直还是水平
label_text='O_{3}浓度(ug/m^3)'                        #图例写什么字
c_label_size,c_tick_size=8,8                   #标签字体大小,刻度字体大小
drawedges_bool=1                                #决定颜色边界是否要画上黑色的线条，0表示否，1表示是
colorbar_ticklength=0                           #colorbar的tick突出长度，如果是0就是不突出

#图片保存数据
#time_str=str(Readtime.get_ncfile_time(nc.Dataset(path),timezone=8)[time_num])  #读取文件的绘图的时间,timezone是时区
#fig_path=str(time_str.replace(":","-"))+'.png'      #保存的文件名，如果需要自己修改则自行添加
fig_path="图1.png"
save_dpi=500            #设置了保存图片的DPI值

#调整子图间距
wspace,hspace=0.25,0.4  #设置了子图的横向间距和纵向间距



ncfile=nc.Dataset(path)
fig = Figure4wrf(fig_width, fig_height, fig_dpi)
for cur_num in range(ver_num*hor_num):
    i=timelist[cur_num]
    title=i
    #数据修改在下面
    factor=getvar(ncfile,var_contourf,timeidx=i)  #如果是华氏度之类的物理量需要换算，可以自行进行修改factor的值
    if chem_w > 0:
        factor = factor * 1000 / 22.4 * chem_w * 273.15 / (getvar(ncfile, 'tk', timeidx=i)) * (getvar(ncfile, 'pressure', timeidx=i)) / 1013.25
    factor2=getvar(ncfile,var_contour,timeidx=i)
    ws1 = getvar(ncfile, var_u, timeidx=i)
    ws2 = getvar(ncfile, var_v, timeidx=i)
    x = to_np(getvar(ncfile, 'lon'))
    y = to_np(getvar(ncfile, 'lat'))
    try:
        a = factor['bottom_top']
        factor = factor[height_contourf, :, :]
        print('填充存在高度')
    except:
        print("填充不存在高度")
    try:
        a = factor2['bottom_top']
        factor2 = factor2[height_contour, :, :]
        print('等高线存在高度')
    except:
        print("等高线不存在高度")
    try:
        a = ws1['bottom_top']
        ws1 = ws1[height_contour, :, :]
        print('风速1存在高度')
    except:
        print("风速1不存在高度")
    try:
        a = ws2['bottom_top']
        ws2 = ws2[height_contour, :, :]
        print('风速2存在高度')
    except:
        print("风速2不存在高度")
    xlabel = xlabellist[cur_num]

    #这里的title可以进行修改
    title = str(Readtime.get_ncfile_time(ncfile,timezone=8)[i])+"  O_{3} and Wind"  # 每个子图的标题

    fig.init_draw(ver_num,hor_num,cur_num+1,title,title_size,title_y)
    #下面是执行函数部分，如果不需要某功能则可以注释，下面做简略介绍：
    #   geo_draw：绘制地理信息
    #   gridline_draw：绘制网格和坐标
    #   contourf_draw：绘制等高线填充
    #   contour_draw：绘制等高线轮廓
    #   quiver_draw：绘制矢量箭头图
    #   colorbar_draw：绘制色块图例
    #   save_fig：保存图片
    #   fig_show：展示图片
    fig.geo_draw(lake_opt, lake_linewidth, lake_linecolor, coastline_linewidth, coastline_color, precision)
    fig.extent_draw(l_x, r_x, b_y, t_y, more)
    fig.gridline_draw(grid_linewidth, grid_color, grid_type, big_interval_x, big_interval_y, small_interval_x,small_interval_y, label_size, label_color, l_x, r_x, b_y, t_y, tick_length,xlabel=xlabel,xlabelsize=xlabelsize)
    fig.contourf_draw(x, y, factor, cmap, level, contourf_opt=contourf_opt,extend=colorbar_extend,)
    # fig.contour_draw(x,y,factor2,level2,contour_color,contour_width,contour_style,fontsize,fontcolor,fontlabel,fontprecision,alpha)
    fig.quiver_draw(x, y, ws1, ws2, interval, quiver_width, quiver_scale, quiver_color, quiver_headwidth, alpha2,quiverkey_opt, quiverkey_x, quiverkey_y, quiverkey_ws, quiverkey_text, quiverkey_size,color_quiver=color_quiver, color_maps=cmap_quiver, ws_map=ws_map)

#由于此处colorbar是绘制一个统一的，因此放在循环外部
fig.colorbar_draw(rect1, rect2, rect3, rect4, label_opt, hv_opt, label_text, c_label_size, c_tick_size, rect_place,rect_more, ticks=ticks, color_quiver=color_quiver,drawedges_bool=drawedges_bool,colorbar_ticklength=colorbar_ticklength)
fig.adjust_subplot(wspace,hspace)
fig.save_fig(fig_path,save_dpi=save_dpi)
#fig.fig_show()

