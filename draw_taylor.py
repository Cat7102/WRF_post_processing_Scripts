import cmaps
import sys
sys.path.append("lib")
from Taylor_Draw import Figure4wrf

scale,dpi=10,180    #泰勒图的大小，dpi
title='泰勒图示意图'  #图题
title_size,title_y=12,1.03  #标题大小以及高度
r_small, r_big, r_interval=0,1.6,0.25   #半径r的始末以及间隔
tick_size=8
rad_list=[0,0.2,0.4,0.6,0.7,0.8,0.85,0.9,0.95,0.99,1]           #需要显示数值的主要R的值
minor_rad_list=[0,0.1,0.2,0.3,0.4,0.5,0.6,0.65,0.7,0.75,0.8,0.85,0.86,0.87,0.88,0.89,
                0.9,0.91,0.92,0.93,0.94,0.95,0.96,0.97,0.98,0.99,1]     #需要显示刻度的次要R的值
a_gridtype,a_gridcolor,a_gridwidth=':','blue',0.8     #原点到R的网格线型、颜色、线宽
r_gridtype,r_gridcolor,r_gridwidth=':','green',0.8    #距离r到r的网格线型、颜色、线宽
angle_linewidth,angle_length=0.8,0.02       #R上刻度线的线宽与长度
circle_list=[(0.25,'black','--',0.8),(0.5,'black','--',0.8),
             (0.75,'black','--',0.8),(1,'black','--',0.8)]     #[(半径，颜色，线型，线宽)]
xlabel='Normalized'         #x轴标签的内容
xlabel_pad,xlabel_size=18,8 #x轴标签距离坐标轴的距离与字体大小
anglelabel='COR'            #R上的标签内容
anglelabel_pad,anglelabel_size=1.75,8   #R上标签的距离与字体大小
#画第一个标签的参数
R1,RMSE1=0.85,0.1
marker_type1,marker_size1,marker_color1,label1='o',4.5,'red','Label1'
#画第一个标签的参数
R2,RMSE2=0.97,-0.12
marker_type2,marker_size2,marker_color2,label2='+',4.5,'green','Label2'
#第一个标签上的字
textR1,textr1=0.83,1+0.08   #这里的是标签，不能再输入R与RMSE，要输入极坐标中角度（弧度制）与距离的绝对值
text1,textsize1='Label1',8
#第二个标签上的字
textR2,textr2=0.96,1-0.13
text2,textsize2='Label2',8

#图例
loc='upper right'   #图例位置
labelspacing=1      #图例当中的空格
markerscale=1     #图例标签大小
legend_title="图例"   #图例标题
markerfont,markerfontsize='times',8     #图例中marker的字体与字体大小
titlefont,titlesize='simsun',12  #图例中title的字体与字体大小

path,save_dpi='泰勒图.png',500

fig = Figure4wrf(scale,dpi)
fig.init_draw(title,title_size,title_y)
fig.grid_draw(r_small, r_big, rad_list, minor_rad_list, r_interval,tick_size,a_gridtype,a_gridcolor,a_gridwidth,r_gridtype,r_gridcolor,r_gridwidth,angle_linewidth,angle_length,circle_list)
fig.label_draw(xlabel,xlabel_pad,xlabel_size,anglelabel,anglelabel_pad,anglelabel_size)
fig.marker_draw(R1,RMSE1,marker_type1,marker_size1,marker_color1,label=label1)
fig.marker_draw(R2,RMSE2,marker_type2,marker_size2,marker_color2,label=label2)
fig.text_draw(textR1,textr1,text1,textsize1)
fig.text_draw(textR2,textr2,text2,textsize2)
fig.legend_draw(loc,labelspacing,markerscale,title=legend_title,titlefont=titlefont,titlesize=titlesize,markerfont=markerfont,markerfontsize=markerfontsize)
fig.save_fig(path,save_dpi)
fig.fig_show()