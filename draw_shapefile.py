import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.font_manager import FontProperties
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
Times = FontProperties(fname="./font/Times.ttf")
#Simsun = FontProperties(fname="./font/SimSun.ttf")
from matplotlib_scalebar.scalebar import ScaleBar

def add_north(ax, labelsize=15, loc_x=0.95, loc_y=0.9, width=0.03, height=0.1, pad=0.12,font_x=121,font_y=31):
    """
    画一个比例尺带'N'文字注释
    主要参数如下
    :param ax: 要画的坐标区域 Axes实例 plt.gca()获取即可
    :param labelsize: 显示'N'文字的大小
    :param loc_x: 以文字下部为中心的占整个ax横向比例
    :param loc_y: 以文字下部为中心的占整个ax纵向比例
    :param width: 指南针占ax比例宽度
    :param height: 指南针占ax比例高度
    :param pad: 文字符号占ax比例间隙
    :return: None
    """
    minx, maxx = ax.get_xlim()
    miny, maxy = ax.get_ylim()
    ylen = maxy - miny
    xlen = maxx - minx
    left = [minx + xlen*(loc_x - width*.5), miny + ylen*(loc_y - pad)]
    right = [minx + xlen*(loc_x + width*.5), miny + ylen*(loc_y - pad)]
    top = [minx + xlen*loc_x, miny + ylen*(loc_y - pad + height)]
    center = [minx + xlen*loc_x, left[1] + (top[1] - left[1])*.4]
    triangle = mpatches.Polygon([left, top, right, center], color='k')
    ax.text(s='N',
            x=font_x,
            y=font_y,
            fontsize=labelsize,
            fontproperties='Times New Roman',
            horizontalalignment='center',
            verticalalignment='bottom')
    ax.add_patch(triangle)

geo_data=gpd.read_file("D:\Data\论文\\4.毕业论文\毕业论文\图片及流程图等\地理绘图shape文件\shapefile\上海市.shp")
fig=plt.figure()
axe=plt.subplot(1,1,1)
geo_data.plot(ax=axe,color='#e8f1ff',edgecolor='#a4c7fc')

plt.tick_params(top=True,bottom=True,left=True,right=True)
plt.tick_params(labeltop=True,labelleft=True,labelright=True,labelbottom=True)
axe.xaxis.set_major_formatter(LongitudeFormatter())
axe.yaxis.set_major_formatter(LatitudeFormatter())
labels = axe.get_xticklabels() + axe.get_yticklabels()
[label.set_fontproperties(FontProperties(fname="./font/Times.ttf", size=8)) for label in labels]

add_north(axe,loc_x=0.07,loc_y=0.98,height=0.05,width=0.02,font_x=120.894,font_y=31.82,labelsize=11)

s1=axe.plot(121.43454,31.39692,'mo',label="气象站点",markersize=4.5)   #58362宝山
s2=axe.plot(121.47454,31.39692,'rd',label="化学污染物分析点",markersize=4.5)   #58362宝山
axe.text(121.45454,31.34692,"58362",ha='center',fontproperties='Times New Roman',fontsize=7)
axe.plot(121.7833,31.05,'mo',markersize=4.5)   #58369南汇
axe.text(121.7833,31.00,"58369",ha='center',fontproperties='Times New Roman',fontsize=7)
axe.plot(121.50,31.67,'mo',markersize=4.5)     #58366崇明
axe.text(121.50,31.62,"58366",ha='center',fontproperties='Times New Roman',fontsize=7)
axe.plot(121.533,31.233,'rd',markersize=4.5)   #58370浦东
axe.text(121.533,31.183,"58370",ha='center',fontproperties='Times New Roman',fontsize=7)
axe.plot(121.35,30.73,'rd',markersize=4.5)     #58460金山
axe.text(121.35,30.68,"58460",ha='center',fontproperties='Times New Roman',fontsize=7)

# Create scale bar
scalebar = ScaleBar(100000, "m", length_fraction=0.072,font_properties={'family': 'Times New Roman', 'weight': 'normal', 'size': 8},
                    location=8,width_fraction=0.005)
axe.add_artist(scalebar)

legend=plt.legend(loc='upper right',title="站点类型",prop=FontProperties(fname="./font/SimSun.ttf", size=6),labelspacing=1,markerscale=0.7)
legend.get_title().set_fontproperties('Simsun')
legend.get_title().set_fontsize(fontsize = 8)
legend._legend_box.align ="left"
fig.savefig("站点.png",dpi=500)
#plt.show()