#代码库，不要修改
import netCDF4 as nc
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
    def __init__(self,scale,dpi):
        plt.close('all')
        self.fig=plt.figure(figsize=(scale,scale),dpi=dpi)

    def init_draw(self,title,title_size,title_y):
        self.axe = plt.subplot(1,1,1,projection='polar')
        self.axe.set_title(Fontprocess.zhSimsun_enTNR(title),fontproperties=Simsun,fontsize=title_size,y=title_y)
        print("图片初始化完成")

    def grid_draw(self, r_small, r_big, rad_list, minor_rad_list, r_interval, tick_size,
                  a_gridtype,a_gridcolor,a_gridwidth,r_gridtype,r_gridcolor,r_gridwidth,
                  angle_linewidth,angle_length,
                  circle_list):
        self.axe.set_thetalim(thetamin=0, thetamax=90)
        self.axe.set_rlim(r_small,r_big)
        angle_list = np.rad2deg(np.arccos(rad_list))
        angle_minor_list = np.arccos(minor_rad_list)
        self.axe.set_thetagrids(angle_list, rad_list)
        str_list = []
        for i in np.arange(r_small, r_big, r_interval):
            if i == 1:
                self.axe.text(0, i, s='\n'+Fontprocess.zhSimsun_enTNR('REF'), fontproperties=Simsun,fontsize=tick_size, ha='center', va='top')  # text的第一个坐标是角度（弧度制），第二个是距离
            else:
                self.axe.text(0, i, s='\n'+Fontprocess.zhSimsun_enTNR(str(i)), fontproperties=Simsun,fontsize=tick_size, ha='center', va='top')  # text的第一个坐标是角度（弧度制），第二个是距离
            self.axe.text(np.pi / 2, i, s=Fontprocess.zhSimsun_enTNR(str(i))+'  ', fontproperties=Simsun,fontsize=tick_size, ha='right', va='center')  # text的第一个坐标是角度（弧度制），第二个是距离

        self.axe.set_rgrids([])
        print(self.axe.get_xticklabels())
        print(self.axe.get_yticklabels())
        labels = self.axe.get_xticklabels() + self.axe.get_yticklabels()
        [label.set_fontproperties(FontProperties(fname="./font/Times.ttf",size=tick_size)) for label in labels]

        self.axe.grid(True, linestyle=a_gridtype, axis='x', color=a_gridcolor,linewidth=a_gridwidth)
        self.axe.grid(True, linestyle=r_gridtype, axis='y', color=r_gridcolor,linewidth=r_gridwidth)

        tick = [self.axe.get_rmax(), self.axe.get_rmax() * (1-angle_length)]
        for t in angle_minor_list:
            self.axe.plot([t, t], tick, lw=angle_linewidth, color="k")  # 第一个坐标是角度（角度制），第二个是距离
        for i in circle_list:#[(半径，颜色，线型，线宽)]
            circle = plt.Circle((1, 0), i[0], transform=self.axe.transData._b, facecolor=(0, 0, 0, 0), edgecolor=i[1],
                                linestyle=i[2], linewidth=i[3])
            self.axe.add_artist(circle)

    def label_draw(self,xlabel,xlabel_pad,xlabel_size,anglelabel,anglelabel_pad,anglelabel_size):
        self.axe.set_xlabel(Fontprocess.zhSimsun_enTNR(xlabel), fontproperties=Simsun, labelpad=xlabel_pad, fontsize=xlabel_size)
        self.axe.text(np.deg2rad(45), anglelabel_pad, s=Fontprocess.zhSimsun_enTNR(anglelabel), fontproperties=Simsun,
                      fontsize=anglelabel_size, ha='center', va='bottom', rotation=-45)

    def marker_draw(self,R,RMSE,marker_type,marker_size,marker_color,label=None):
        self.axe.plot(float(np.arccos(R)), 1+RMSE, marker_type,color=marker_color,markersize=marker_size, label=label)

    def text_draw(self,R,r,text,textsize):
        self.axe.text(np.arccos(R), r, s=Fontprocess.zhSimsun_enTNR(text),fontproperties=Simsun, fontsize=textsize)

    def legend_draw(self,loc,labelspacing,markerscale,title=None,markerfont='times',markerfontsize=6,titlefont='simsun',titlesize=8):
        if markerfont=='simsun':
            legend=plt.legend(loc=loc,title=title,prop=FontProperties(fname="./font/SimSun.ttf", size=markerfontsize),
                       labelspacing=labelspacing, markerscale=markerscale)
        if markerfont=='times':
            legend=plt.legend(loc=loc,title=title,prop=FontProperties(fname="./font/Times.ttf", size=markerfontsize),
                       labelspacing=labelspacing, markerscale=markerscale)
        if titlefont=='simsun':
            legend.get_title().set_fontproperties(FontProperties(fname="./font/SimSun.ttf"))
            legend.get_title().set_fontsize(fontsize=titlesize)
        if titlefont=='times':
            legend.get_title().set_fontproperties(FontProperties(fname="./font/Times.ttf"))
            legend.get_title().set_fontsize(fontsize=titlesize)

    def save_fig(self,path,save_dpi):
        self.fig.savefig(path,dpi=save_dpi)

    def fig_show(self):
        plt.show()
