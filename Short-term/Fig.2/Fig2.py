import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from pylab import rcParams



plt.rcParams.update({
    'text.usetex': True,
    'font.family': 'serif',
    'font.serif': ['Times New Roman'],
    'axes.labelsize': 20,
    'axes.linewidth':2.5,
    'xtick.labelsize': 28,
    'ytick.labelsize': 28,
    'legend.fontsize': 20,
})



# Load data
Data_10 = np.loadtxt('N=10_w=0.95.txt')
Data_20 = np.loadtxt('N=20_w=0.95.txt')
Data_100 = np.loadtxt('N=100_w=0.95.txt')

prejudice_array=np.linspace(0, 0.4, 50)
Prej_spite_10=np.zeros(len(prejudice_array))
Prej_spite_20=np.zeros(len(prejudice_array))
Prej_spite_100=np.zeros(len(prejudice_array))

prej_individual_10=np.zeros(len(prejudice_array))
prej_individual_20=np.zeros(len(prejudice_array))
prej_individual_100=np.zeros(len(prejudice_array))

for i in range(len(prejudice_array)): 
    Prej_spite_10[i]=Data_10[i][2]
    Prej_spite_20[i]=Data_20[i][2]
    Prej_spite_100[i]=Data_100[i][2]

    prej_ind_10=0
    prej_ind_20=0
    prej_ind_100=0
    for j in range(4):
        prej_ind_10+=Data_10[i][j]
        prej_ind_20+=Data_20[i][j]
        prej_ind_100+=Data_100[i][j]
    prej_individual_10[i]=prej_ind_10
    prej_individual_20[i]=prej_ind_20
    prej_individual_100[i]=prej_ind_100



xticks=[0.0,0.2,0.4]
yticks=[0.0,0.5,1.0]

fig= plt.subplots(figsize=(10, 9))
plt.plot(prejudice_array, Prej_spite_10, '#007894', markersize=3.5, label=r'$N=10$',lw=2.2, linestyle= '--')
plt.plot(prejudice_array, Prej_spite_20, '#007894', markersize=3.5, label=r'$N=20$',lw=2.2, linestyle= 'dotted')
plt.plot(prejudice_array, Prej_spite_100, '#007894', markersize=3.5, label=r'$N=100$',lw=2.2, linestyle= 'solid')

plt.plot(prejudice_array, prej_individual_10, 'k', markersize=3.5, label=r'$N=10$',lw=2.2, linestyle= '--', alpha=1.0)
plt.plot(prejudice_array, prej_individual_20, 'k', markersize=3.5, label=r'$N=20$',lw=2.2, linestyle= 'dotted', alpha=1.0)
plt.plot(prejudice_array, prej_individual_100, 'k', markersize=3.5, label=r'$N=100$',lw=2.2, linestyle= 'solid', alpha=1.0)

plt.xlabel(r'$e$', fontsize=30)
plt.ylim(0,1.0)
plt.axvline(x=0.2, ls='solid', lw=2.2, color='#aaa9ab')
plt.axhline(y=0.5, ls='solid', lw=2.2, color='k')
plt.yticks(yticks, fontsize=28)
plt.xticks(xticks,fontsize=28)
plt.tick_params(axis='both', which='major', width=2, length=10)
plt.text(x=0.208, y=0.6, s=r'$e=e_c$', fontsize=30, ha='center', va='center', rotation=90)

ax = plt.gca()  # Get current axis
ax.text(-0.1, 0.25, r'$x_{\textrm{spite}}$', color='#007894',fontsize=30, rotation=90, transform=ax.transAxes, va='center')
ax.text(-0.1, 0.75, r'$x_{\textrm{prej}}$', color='k',fontsize=30, rotation=90, transform=ax.transAxes, va='center')


plt.savefig("Fig2.pdf", dpi=1000)

plt.show()

