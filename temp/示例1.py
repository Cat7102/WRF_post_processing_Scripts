import matplotlib.pyplot as plt
from matplotlib import rcParams

config = {
    "font.family":'serif',
    "mathtext.fontset":'stix',
    "font.serif": ['SimSun'],
}
rcParams.update(config)

#plt.title(r'宋体 $\mathrm{Times \; New \; Roman}\/\/ \alpha_i > \beta_i$')
plt.title(r'宋体 $\mathrm{Times\;New\;Roman}$')
plt.axis('off')
plt.show()