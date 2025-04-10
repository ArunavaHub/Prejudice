import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
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


Average_freq_15 = np.loadtxt('e=0.15_N=100_w=0.95.txt')
Average_freq_25 = np.loadtxt('e=0.25_N=100_w=0.95.txt')


freq_15=np.zeros(4)
freq_25=np.zeros(4)
prej_15=0
prej_25=0

for i in range(4):
    freq_15[i]=Average_freq_15[i]+Average_freq_15[4+i]
    freq_25[i]=Average_freq_25[i]+Average_freq_25[4+i]

Strat =[ r'Fairness', r'Altruism', r'Spite',r'Unfairness' ]
x = np.arange(len(Strat))

width = 0.2
gap = 0.02 

fig, ax = plt.subplots(figsize=(12, 8))
bars1 = ax.bar(x - width/2 - gap/2, freq_15, width, label='Prej=0.15')
bars2 = ax.bar(x + width/2 + gap/2, freq_25, width, label='Prej=0.25')

bars1[0].set_color('#9FE2BF')
bars1[1].set_color('#9FE2BF')
bars1[2].set_color('#9FE2BF')
bars1[3].set_color('#9FE2BF')


bars2[0].set_color('#687a67')
bars2[1].set_color('#687a67')
bars2[2].set_color('#687a67')
bars2[3].set_color('#687a67')


custom_legend = [
    plt.Line2D([0], [0], color='#9FE2BF', lw=10,
        marker='s',                  
        markersize=20,               
        markerfacecolor='#9FE2BF',   
        markeredgewidth=1.1,         
        markeredgecolor='black',
        linestyle='None', label=r'$\textrm{Prejudicity}~(e)=0.15$'),
    plt.Line2D([0], [0], color='#687a67', lw=10,
        marker='s',
        markersize=20,
        markerfacecolor='#687a67',
        markeredgewidth=1.1,
        markeredgecolor='black',
        linestyle='None',
    label=r'$\textrm{Prejudicity}~(e)=0.25$'),
]

for i, (bar1, bar2) in enumerate(zip(bars1, bars2)):
    bar1.set_edgecolor('black')
    bar2.set_edgecolor('black')
    

ax.set_ylabel(r'Frequency', fontsize=30)
ax.set_xticks(x)
ax.set_xticklabels(Strat, fontsize=30)
ax.set_yticks([0.0, 0.5, 1.0])
plt.tick_params(axis='x', which='major', width=0, length=10)
plt.tick_params(axis='y', which='major', width=2, length=10)

plt.savefig("Fig5(k).jpg", dpi=500)
plt.show()
