#这个是代码库，不要修改

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeat
import matplotlib.ticker as mticker
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import cmaps
import matplotlib as mpl
from matplotlib.font_manager import FontProperties
import Fontprocess
import numpy as np
Simsun = FontProperties(fname=".\\font\SimSun.ttf")
mpl.rcParams['axes.unicode_minus']=False
config = {
    "mathtext.fontset":'stix',
}
mpl.rcParams.update(config)

class Figure4wrf():
    def __init__(self,width,height,dpi):
        plt.close('all')
        self.fig=plt.figure(figsize=(width,height),dpi=dpi)

    def init_draw(self,ver_num,hor_num,cur_num,title,title_size,title_y):
        self.axe=plt.subplot(ver_num,hor_num,cur_num,projection=ccrs.PlateCarree())
        self.axe.set_title(Fontprocess.zhSimsun_enTNR(title),fontproperties=Simsun,fontsize=title_size,y=title_y)
        print("图片初始化完成")

    def geo_draw(self,lake_opt,lake_linewidth,lake_linecolor,coastline_linewidth,coastline_color,precision):
        # 添加海岸线数据
        self.axe.add_feature(cfeat.COASTLINE.with_scale(precision), linewidth=coastline_linewidth,color=coastline_color)
        # 通过下面两行代码可以添加湖泊轮廓线，其他的以此类推
        if lake_opt==0:
            LAKES_border = cfeat.NaturalEarthFeature('physical', 'lakes', precision, edgecolor=lake_linecolor, facecolor='never')
            self.axe.add_feature(LAKES_border, linewidth=lake_linewidth)
            print("绘制湖泊")
        if lake_opt==1:
            print("不绘制湖泊")

    def extent_draw(self,l_x,r_x,b_y,t_y,more,geo_opt):
        if geo_opt==0:
            self.axe.set_extent([l_x - more, r_x+more, b_y - more, t_y+more], crs=ccrs.PlateCarree())
            print("绘制地理图")
        if geo_opt==1:
            self.axe.set_extent([l_x - more, r_x + more, b_y - more, t_y + more])
            print("不绘制地理图")

    def gridline_draw(self,grid_linewidth,grid_color,grid_type,big_interval_x,big_interval_y,small_interval_x,small_interval_y,
                      top_labels,bottom_labels,left_labels,right_labels,label_size,label_color,geo_opt,
                      l_x,r_x,b_y,t_y):
        if geo_opt==0:
            # 绘制网格
            gl = self.axe.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=grid_linewidth, color=grid_color, linestyle=grid_type)
            # 可以控制坐标轴出现的位置，设置False表示隐藏,0表示显示
            if top_labels==0: gl.top_labels = True
            if top_labels==1: gl.top_labels = False
            if bottom_labels==0: gl.bottom_labels = True
            if bottom_labels==1: gl.bottom_labels = False
            if right_labels==0: gl.right_labels = True
            if right_labels==1: gl.right_labels = False
            if left_labels==0: gl.left_labels = True
            if left_labels==1: gl.left_labels = False
            # 自定义给出x轴Locator的位置
            gl.xlocator = mticker.FixedLocator(np.arange(l_x, r_x+big_interval_x, big_interval_x))
            gl.ylocator = mticker.FixedLocator(np.arange(b_y, t_y+big_interval_y, big_interval_y))
            gl.xformatter = LONGITUDE_FORMATTER
            gl.yformatter = LATITUDE_FORMATTER
            gl.xlabel_style = {'size': label_size, "color": label_color, "font": 'Times New Roman'}
            gl.ylabel_style = {'size': label_size, 'color': label_color, "font": 'Times New Roman'}
            # 下面的用于设置minor刻度，不需要就注释掉
            self.axe.set_xticks(np.arange(l_x, r_x, small_interval_x), crs=ccrs.PlateCarree(), minor=True)
            self.axe.set_yticks(np.arange(b_y, t_y, small_interval_y), crs=ccrs.PlateCarree(), minor=True)
            plt.xticks([])
            plt.yticks([])
            print("绘制地理网格")
        if geo_opt==1:
            # 绘制网格
            gl = self.axe.gridlines(draw_labels=True, linewidth=grid_linewidth, color=grid_color, linestyle=grid_type)
            # 可以控制坐标轴出现的位置，设置False表示隐藏,0表示显示
            if top_labels==0: gl.top_labels = True
            if top_labels==1: gl.top_labels = False
            if bottom_labels==0: gl.bottom_labels = True
            if bottom_labels==1: gl.bottom_labels = False
            if right_labels==0: gl.right_labels = True
            if right_labels==1: gl.right_labels = False
            if left_labels==0: gl.left_labels = True
            if left_labels==1: gl.left_labels = False
            # 自定义给出x轴Locator的位置
            gl.xlocator = mticker.FixedLocator(np.arange(l_x, r_x+big_interval_x, big_interval_x))
            gl.ylocator = mticker.FixedLocator(np.arange(b_y, t_y+big_interval_y, big_interval_y))
            gl.xlabel_style = {'size': label_size, "color": label_color, "font": 'Times New Roman'}
            gl.ylabel_style = {'size': label_size, 'color': label_color, "font": 'Times New Roman'}
            # 下面的用于设置minor刻度，不需要就注释掉
            axe_1.set_xticks(np.arange(l_x, r_x, small_interval_x), minor=True)
            axe_1.set_yticks(np.arange(b_y, t_y, small_interval_y), minor=True)
            plt.xticks([])
            plt.yticks([])
            print("绘制非地理网格")

    def contourf_draw(self,x,y,factor,cmap,level):
        self.contourf = self.axe.contourf(x, y, factor, levels=level, cmap=cmap)
        print("最大和最小的值分别是：")
        print(np.max(factor).values, np.min(factor).values)
        print("绘制填充")

    def contour_draw(self,x,y,factor,level,contour_color,linewidth,linestyle,fontsize,fontcolor,fontlabel,fontprecision,alpha):
        contour = self.axe.contour(x, y, factor, levels=level, colors=contour_color, linewidths=linewidth,
                                   linestyles=linestyle,alpha=alpha)
        if fontlabel==0:
            self.axe.clabel(contour, inline=True, fontsize=fontsize, colors=fontcolor, fmt=fontprecision)
        if fontlabel==1:
            self.axe.clabel(contour, inline=False, fontsize=fontsize, colors=fontcolor, fmt=fontprecision)
        print("等高线绘制完毕")

    def quiver_draw(self,x,y,ws1,ws2,interval,quiver_width,quiver_scale,quiver_color,quiver_headwidth,alpha,geo_opt,
                    quiverkey_opt,quiverkey_x,quiverkey_y,quiverkey_ws,quiverkey_text,quiverkey_size):
        x,y,ws1,ws2=x[::interval,::interval],y[::interval,::interval],ws1[::interval,::interval],ws2[::interval,::interval]
        if geo_opt==0:
            quiver = self.axe.quiver(x, y, ws1, ws2, pivot='mid',
                                     width=quiver_width, scale=quiver_scale, color=quiver_color, headwidth=quiver_headwidth,alpha=alpha,
                                     transform=ccrs.PlateCarree())
        if geo_opt==1:
            quiver = self.axe.quiver(x, y, ws1, ws2, pivot='mid',
                                     width=quiver_width, scale=quiver_scale, color=quiver_color, headwidth=quiver_headwidth,alpha=alpha)
        if quiverkey_opt==0:
            # 绘制矢量箭头的图例
            self.axe.quiverkey(quiver, quiverkey_x, quiverkey_y, quiverkey_ws, quiverkey_text,
                               labelpos='E', coordinates='axes', fontproperties={'size': quiverkey_size,'family':'Times New Roman'})

    def colorbar_draw(self,rect1,rect2,rect3,rect4,label_opt,hv_opt,label_text,label_size,tick_size,rect_place,rect_more):
        if label_opt==0:
            if rect_place=='bottom':
                self.fig.subplots_adjust(bottom=rect_more)
            if rect_place=='top':
                self.fig.subplots_adjust(top=rect_more)
            if rect_place=='left':
                self.fig.subplots_adjust(left=rect_more)
            if rect_place=='right':
                self.fig.subplots_adjust(right=rect_more)
            rect = [rect1, rect2, rect3, rect4]  # 分别代表，水平位置，垂直位置，水平宽度，垂直宽度
            cbar_ax = self.fig.add_axes(rect)
            cb = self.fig.colorbar(self.contourf, cax=cbar_ax, orientation=hv_opt,spacing='proportional')  # orientation='vertical'
            cb.set_label(Fontprocess.zhSimsun_enTNR(label_text),fontproperties=Simsun,fontsize=label_size)
            cb.ax.tick_params(labelsize=tick_size)
            #下面两行是指定colorbar刻度字体的方法，绘图的坐标也同样适用
            labels=cb.ax.get_xticklabels()+cb.ax.get_yticklabels()
            [label.set_fontname('Times New Roman') for label in labels]
        if label_opt==1:
            cb = self.fig.colorbar(self.contourf, orientation=hv_opt,spacing='proportional')  # orientation='vertical'
            cb.set_label(Fontprocess.zhSimsun_enTNR(label_text),fontproperties=Simsun,fontsize=label_size)
            cb.ax.tick_params(labelsize=tick_size)
            # 下面两行是指定colorbar刻度字体的方法，绘图的坐标也同样适用
            labels=cb.ax.get_xticklabels()+cb.ax.get_yticklabels()
            [label.set_fontname('Times New Roman') for label in labels]

    def adjust_subplot(self,wspace,hspace):
        plt.subplots_adjust(wspace=wspace, hspace=hspace)

    def save_fig(self,path):
        self.fig.savefig(path)

    def fig_show(self):
        self.fig.show()
        plt.show()
