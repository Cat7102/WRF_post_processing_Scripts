#代码库，不要修改

import netCDF4 as nc
from wrf import to_np
import cartopy.crs as ccrs
import cartopy.feature as cfeat
import matplotlib.pyplot as plt
import cmaps
import matplotlib as mpl
from matplotlib.font_manager import FontProperties
import numpy as np
import Fontprocess
Simsun = FontProperties(fname="./font/SimSun.ttf")
Times = FontProperties(fname="./font/Times.ttf")
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
        self.axe = plt.subplot(ver_num, hor_num, cur_num)
        self.axe.set_title(Fontprocess.zhSimsun_enTNR(title),fontproperties=Simsun,fontsize=title_size,y=title_y)
        print("图片初始化完成")

    def extent_draw(self,l_x,r_x,b_y,t_y):
        self.axe.set_xlim(l_x, r_x)
        self.axe.set_ylim(b_y, t_y)
        self.axe.invert_yaxis()  # 翻转纵坐标
        print("绘制图片范围")

    def gridline_draw(self, grid_linewidth, grid_color, grid_type, float_lonlist, str_lonlist, ticks_size,ticks_color,
                      small_p, big_p, big_interval_p, tick_length,ylabel='气压(hPa)',xaxis_show=True,ylabelsize=9, xlabel=None, xlabelsize=None):
        self.axe.grid(color=grid_color, linestyle=grid_type, linewidth=grid_linewidth)
        plt.xticks(float_lonlist, str_lonlist, fontsize=ticks_size, color=ticks_color)  # 这一行代码用于修改刻度的字体
        plt.yticks(fontsize=ticks_size, color=ticks_color)  # 这一行代码用于修改刻度的字体
        self.axe.get_xaxis().set_visible(xaxis_show)
        self.axe.set_yticks(np.arange(small_p, big_p + big_interval_p / 2, big_interval_p))
        self.axe.tick_params(length=tick_length)
        labels = self.axe.get_xticklabels() + self.axe.get_yticklabels()
        [label.set_fontproperties(FontProperties(fname="./font/Times.ttf", size=8)) for label in labels]
        self.axe.set_ylabel(Fontprocess.zhSimsun_enTNR(ylabel), fontproperties=Simsun, fontsize=ylabelsize)
        try:
            if xlabel == None:  # 如果ticks不为None，那么就会报错，然后就可以进入下面的设置ticks
                print("xlabel为空")
        except:
            print("xlabel不为空")
            plt.xlabel(xlabel,fontproperties=FontProperties(fname="./font/Times.ttf",size=xlabelsize))
        print("绘制网格")

    def contourf_draw(self,lonlist,plist,f_vert,cmap,level,extend="neither"):
        self.contourf = self.axe.contourf(lonlist, plist, f_vert, levels=level, cmap=cmap,extend=extend)
        print("绘制填充")

    def quiver_draw(self,ua,va,wa,lonlist,plist,interval,interval_y,start_lat,end_lat,start_lon,end_lon,
                    quiver_width,quiver_scale,quiver_color,quiver_headwidth,alpha):
        ua_vert, va_vert, wa_vert = to_np(ua), to_np(va), to_np(wa)
        ws_vert = np.sqrt(ua_vert ** 2 + va_vert ** 2)
        #计算风向夹角
        wdir_vert = np.arctan2(va_vert, ua_vert) * 180 / np.pi
        line_angel = np.arctan2(end_lat - start_lat, end_lon - start_lon) * 180 / np.pi
        vl_angel = wdir_vert - line_angel
        vl_angel = np.cos(vl_angel / 180 * np.pi)
        ws_vert = ws_vert * vl_angel
        x, y = [], []
        y_temp, ws1, ws2 = plist.tolist(), ws_vert[::interval_y, ::interval], wa_vert[::interval_y, ::interval]
        for i in range(len(y_temp[::interval_y])):
            x.append(lonlist[::interval])
        for i in range(len(lonlist[::interval])):
            y.append(y_temp[::interval_y])
        y = np.array(y)
        y = y.T
        x = np.array(x)

        quiver = self.axe.quiver(x, y, ws1, ws2, pivot='mid',
                            width=quiver_width, scale=quiver_scale, color=quiver_color, headwidth=quiver_headwidth,
                            alpha=alpha)

    def colorbar_draw(self, rect1, rect2, rect3, rect4, hv_opt, label_text, label_size, tick_size,
                      rect_place, rect_more, ticks=None, drawedges_bool=True, colorbar_ticklength=2):
        if rect_place == 'bottom':
            self.fig.subplots_adjust(bottom=rect_more)
        if rect_place == 'top':
            self.fig.subplots_adjust(top=rect_more)
        if rect_place == 'left':
            self.fig.subplots_adjust(left=rect_more)
        if rect_place == 'right':
            self.fig.subplots_adjust(right=rect_more)
        rect = [rect1, rect2, rect3, rect4]  # 分别代表，水平位置，垂直位置，水平宽度，垂直宽度
        cbar_ax = self.fig.add_axes(rect)
        cb = self.fig.colorbar(self.contourf, drawedges=drawedges_bool, cax=cbar_ax, orientation=hv_opt,
                          spacing='uniform')  # orientation='vertical'
        cb.set_label(Fontprocess.zhSimsun_enTNR(label_text), fontproperties=Simsun, fontsize=label_size)
        cb.ax.tick_params(length=colorbar_ticklength)
        # 下面两行是指定colorbar刻度字体的方法，绘图的坐标也同样适用
        # 下面两行是指定colorbar刻度字体的方法，绘图的坐标也同样适用
        labels = cb.ax.get_xticklabels() + cb.ax.get_yticklabels()
        [label.set_fontproperties(FontProperties(fname="./font/Times.ttf", size=tick_size)) for label in labels]
        cb.set_ticks(ticks)

    def smallmap_draw(self,smap_horpos,smap_verpos,smap_horlen,smap_verlen,coastline_width,coastline_color,
                      smap_startlat,smap_endlat,smap_startlon,smap_endlon,
                      plot_startlat,plot_endlat,plot_startlon,plot_endlon,plot_color,plot_linewidth,plot_linestyle,
                      marker,marker_color,marker_size,
                      textlist):
        axe1 = self.fig.add_axes([smap_horpos, smap_verpos, smap_horlen, smap_verlen], projection=ccrs.PlateCarree())
        axe1.add_feature(cfeat.COASTLINE.with_scale("10m"), linewidth=coastline_width, color=coastline_color)
        axe1.set_extent([smap_startlon, smap_endlon,smap_startlat, smap_endlat], crs=ccrs.PlateCarree())
        axe1.plot([plot_startlon, plot_endlon], [plot_startlat, plot_endlat], color=plot_color, linewidth=plot_linewidth,linestyle=plot_linestyle)
        axe1.plot(plot_startlon, plot_startlat, marker=marker, color=marker_color, markersize=marker_size)
        axe1.plot(plot_endlon, plot_endlat, marker=marker, color=marker_color, markersize=marker_size)
        for i in textlist:
            axe1.text(i[0], i[1], i[2],fontproperties=FontProperties(fname="./font/Times.ttf", size=i[3]))

    def adjust_subplot(self,wspace,hspace):
        plt.subplots_adjust(wspace=wspace, hspace=hspace)

    def save_fig(self,path,save_dpi):
        self.fig.savefig(path,dpi=save_dpi)

    def fig_show(self):
        self.fig.show()
        plt.show()