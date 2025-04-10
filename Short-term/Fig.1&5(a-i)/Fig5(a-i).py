import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

plt.rcParams.update({
    'text.usetex': True,
    'font.family': 'serif',
    'font.serif': ['Times New Roman'],
    'axes.labelsize': 20,
    'axes.linewidth': 1.5,
    'xtick.labelsize': 18,
    'ytick.labelsize': 18,
    'legend.fontsize': 16,
})


Strat = [r'Fairness', r'Altruism', r'Spite', r'Unfairness']
x = np.arange(len(Strat))
N_values = [10, 20, 100]
w_values = [0.05, 0.5, 0.95]

width = 0.2
gap = 0.05

fig, axes = plt.subplots(3, 3, figsize=(18, 12))
fig.subplots_adjust(hspace=0.4, wspace=0.3)

for i, w in enumerate(w_values):
    for j, N in enumerate(N_values):
        ax = axes[i, j]
        Average_freq_15 = np.loadtxt(f'e=0.15_N={N}_w={w}.txt')
        Average_freq_25 = np.loadtxt(f'e=0.25_N={N}_w={w}.txt')

        freq_15=np.zeros(4)
        freq_25=np.zeros(4)

        for k in range(4):
            freq_15[k]=Average_freq_15[k]+Average_freq_15[4+k]
            freq_25[k]=Average_freq_25[k]+Average_freq_25[4+k]

        bars1 = ax.bar(x - width/2 - gap/2, freq_15, width, label='Prej=0.15')
        bars2 = ax.bar(x + width/2 + gap/2, freq_25, width, label='Prej=0.25')
        for bar in bars1:
            bar.set_color('#9FE2BF')
            bar.set_edgecolor('black')

        for bar in bars2:
            bar.set_color('#687a67')
            bar.set_edgecolor('black')
        ax.set_xticks(x)
        ax.set_xticklabels(Strat, fontsize=16)
        ax.set_yticks([0.0, 0.5, 1.0])
        ax.tick_params(axis='y', which='major', width=1, length=5)
        ax.tick_params(axis='x', which='major', width=0, length=5)

        if j == 0:
            ax.set_ylabel(f"$w = {w}$", fontsize=22, labelpad=50, loc='center')

            ax.text(
                -0.2, 0.5,
                'Frequency',
                va='center', rotation='vertical', fontsize=18, transform=ax.transAxes
            )
        
        if i == 0:
            ax.set_title(f"$N = {N}$", fontsize=20, pad=20)

# Add a common legend
handles = [
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

fig.legend(
    handles=handles,                
    loc='lower center',              
    fontsize=16,                     
    ncol=2,                          
    bbox_to_anchor=(0.5, -0.01),     
    frameon=False                   
)


# Save and show the plot
plt.savefig("Fig5(a-i).jpg", dpi=500, bbox_inches="tight")
plt.show()
