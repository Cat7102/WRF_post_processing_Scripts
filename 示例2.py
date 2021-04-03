from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
from matplotlib import rcParams
Simsun = FontProperties(fname=".\SimSun.ttf")
config = {
    "mathtext.fontset":'stix',
}
rcParams.update(config)

#plt.title(r'宋体 $\mathrm{Times \; New \; Roman}\/\/ \alpha_i > \beta_i$')
plt.title('宋体$\mathrm{\;}$$\mathrm{Times\;New\;Roman}$',fontproperties=Simsun,fontsize=15)
plt.axis('off')
plt.show()
