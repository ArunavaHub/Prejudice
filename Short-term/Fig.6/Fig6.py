import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from pylab import rcParams

rcParams['text.usetex'] = True
rcParams["font.family"] = "Times New Roman"
rcParams["font.size"] = 56
rcParams['axes.linewidth'] = 1.2

Data = np.loadtxt('N=10_w=0.95.txt')

Offer_l_array = np.linspace(0.0, 0.5, 51)
prejudicity_array = np.linspace(0, 0.5, 51)
input_array = []

for i in range(len(prejudicity_array)):
    for k in range(len(Offer_l_array)):
        input_array.append([prejudicity_array[i], Offer_l_array[k]])

Data_spite = []
for i in range(len(input_array)):
    Data_spite.append(Data[i][2]+Data[i][6])
Data_spite = np.array(Data_spite)
spite_data_matrix = Data_spite.reshape(len(prejudicity_array), len(Offer_l_array))


matrix_with_nan = np.where(spite_data_matrix == 1.0, np.nan, spite_data_matrix).astype(float)

max_element = np.nanmax(matrix_with_nan)
index = np.where(matrix_with_nan == max_element)

plt.figure(figsize=(16, 13))

norm = Normalize(vmin=0.0, vmax=0.4)
levels=np.linspace(0.0,0.5,11)

contour = plt.contourf(Offer_l_array, prejudicity_array, matrix_with_nan,
                       cmap='plasma', levels=levels, origin='lower')

cbar = plt.colorbar(contour, shrink=1.0, ticks=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5])
cbar.ax.tick_params(labelsize=32, width=1.5, length=10)
plt.plot([0, 0.5], [0.5,0], color='black', linewidth=1.5, linestyle='-')

ticks = [0.0, 0.25, 0.5]
plt.xticks(ticks, fontsize=56)
plt.yticks(ticks, fontsize=56)

ax = plt.gca()
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

plt.tight_layout()

plt.savefig('N=10_w=0.95.jpg', dpi=500)

plt.show()
