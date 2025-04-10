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

freq_15 = np.zeros(2)
freq_25 = np.zeros(2)

prej_15 = 0
prej_25 = 0

for i in range(4):
    prej_15 += Average_freq_15[i]
    prej_25 += Average_freq_25[i]

freq_15[0] = Average_freq_15[2] + Average_freq_15[4 + 2]
freq_25[0] = Average_freq_25[2] + Average_freq_25[4 + 2]
freq_15[1] = prej_15
freq_25[1] = prej_25

Strat = [r'$x_{\textrm{spite}}$', r'$x_{\textrm{prej}}$']

x = np.arange(len(Strat))

width = 0.2
gap = 0.02

fig, ax = plt.subplots(figsize=(12, 8))
bars1 = ax.bar(x - width / 2 - gap / 2, freq_15, width, label='Prej=0.15')
bars2 = ax.bar(x + width / 2 + gap / 2, freq_25, width, label='Prej=0.25')

## Color bars =======================
bars1[0].set_color('#9FE2BF')
bars1[1].set_color('#9FE2BF')

bars2[0].set_color('#687a67')
bars2[1].set_color('#687a67')

## Legend =============================
custom_legend = [
    plt.Line2D([0], [0], color='#9FE2BF', lw=10,
               marker='s',  
               markersize=20,  
               markerfacecolor='#9FE2BF',  
               markeredgewidth=1.1,  
               markeredgecolor='black', 
               linestyle='None', label=r'$e=0.15$'),
    plt.Line2D([0], [0], color='#687a67', lw=10,
               marker='s',
               markersize=20,
               markerfacecolor='#687a67',
               markeredgewidth=1.1,
               markeredgecolor='black',
               linestyle='None',
               label=r'$e=0.25$'),
]

for bar1, bar2 in zip(bars1, bars2):
    bar1.set_edgecolor('black')
    bar2.set_edgecolor('black')

for bar in bars1:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.2f}',
            ha='center', va='bottom', fontsize=28)

for bar in bars2:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.2f}',
            ha='center', va='bottom', fontsize=28)

ax.set_ylabel(r'Frequency', fontsize=30)
ax.set_xticks(x)
ax.set_xticklabels(Strat, fontsize=30)
ax.xaxis.set_tick_params(pad=10)
ax.set_ylim(0,1.1)
ax.set_yticks([0.0, 0.5, 1.0])
ax.legend(handles=custom_legend, loc='upper left', ncol=1, fontsize=28)
plt.tick_params(axis='x', which='major', width=0, length=0)
plt.tick_params(axis='y', which='major', width=2, length=10)


plt.savefig("INF_bar_spite_prejudice_level.pdf", dpi=1000)
plt.show()
