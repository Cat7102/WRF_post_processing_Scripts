import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties
import matplotlib as mpl
import cartopy.crs as ccrs
import cartopy.feature as cfeat

Simsun = FontProperties(fname="./font/SimSun.ttf")
mpl.rcParams['axes.unicode_minus']=False
config = {"mathtext.fontset":'stix',}
mpl.rcParams.update(config)

fig=plt.figure(figsize=(5,5),dpi=150)   #创建画布
axe=plt.subplot(1,1,1,projection=ccrs.PlateCarree())    #创建子图
axe.set_title('地理图$\mathrm{}$',fontproperties=Simsun,fontsize=12,y=1.05)   #设置子图标题
axe.add_feature(cfeat.COASTLINE.with_scale('10m'), linewidth=1,color='k')
plt.show()  #展示图片