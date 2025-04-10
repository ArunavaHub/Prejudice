import numpy as np
import matplotlib.pyplot as plt
from pylab import rcParams

plt.rcParams.update({
    'text.usetex': True,
    "pgf.texsystem": "pdflatex",
    'pgf.rcfonts': False,
    'font.family': 'serif',
    'font.serif': ['Times New Roman'],
    'axes.labelsize': 20,
    'axes.linewidth': 2.5,
    'xtick.labelsize': 28,
    'ytick.labelsize': 28,
    'legend.fontsize': 22,
})



yticks=[0.0, 0.25, 0.5]

Sfreq_10_15 = np.loadtxt('e=0.15_N=10_w=0.95.txt')
Sfreq_10_25 = np.loadtxt('e=0.25_N=10_w=0.95.txt')
Sfreq_20_15 = np.loadtxt('e=0.15_N=20_w=0.95.txt')
Sfreq_20_25 = np.loadtxt('e=0.25_N=20_w=0.95.txt')
Sfreq_100_15 = np.loadtxt('e=0.15_N=100_w=0.95.txt')
Sfreq_100_25 = np.loadtxt('e=0.25_N=100_w=0.95.txt')

plt.figure(figsize=(13,8))
## Draw the plot======================================================================================
plt.plot(np.arange(0,len(Sfreq_10_15),1),Sfreq_10_15, color='#0000ff', linestyle='dashed', lw=2.0)
plt.plot(np.arange(0,len(Sfreq_10_15),1),Sfreq_20_15,color='red', linestyle='dashed', lw=2.0)
plt.plot(np.arange(0,len(Sfreq_10_15),1),Sfreq_100_15, color='green',linestyle='dashed', lw=2.0)
plt.plot(np.arange(0,len(Sfreq_10_15),1),Sfreq_10_25, color='#0000ff',linestyle='solid', lw=2.0)
plt.plot(np.arange(0,len(Sfreq_10_15),1),Sfreq_20_25, color='red',linestyle='solid', lw=2.0)
plt.plot(np.arange(0,len(Sfreq_10_15),1),Sfreq_100_25, color='green',linestyle='solid', lw=2.0)
# plt.xlim(1,700)
plt.ylim(-0.02,0.52)
plt.xticks(fontsize=28)
plt.yticks(yticks,fontsize=28)
plt.tick_params(axis='x', which='major', width=2, length=10)
plt.tick_params(axis='y', which='major', width=2, length=10)
plt.xlabel(r'$t$', fontsize=30)
plt.ylabel(r'$\alpha_3 +\alpha_7$', fontsize=30)
plt.savefig("Fig3.png",dpi=1000)
plt.show()

