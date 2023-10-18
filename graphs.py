import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
with open('stat.csv', 'r') as f:	
    df=pd.read_csv(f, sep=';', header=0, index_col=None,decimal=',')
fig, ax = plt.subplots()
ax.set_title('Media iterazioni in base a numero nodi - Fidelity')

dfplot=df[df['Nodi']==3].sort_values(by=['Fidelity'])
ax.scatter(dfplot['Fidelity'],dfplot['Media iterazioni'], label='3 nodi', color='red', s=10)
dfplot=df[df['Nodi']==5].sort_values(by=['Fidelity'])
ax.scatter(dfplot['Fidelity'],dfplot['Media iterazioni'], label='5 nodi', color='green', s=10)
dfplot=df[df['Nodi']==7].sort_values(by=['Fidelity'])
ax.scatter(dfplot['Fidelity'],dfplot['Media iterazioni'], label='7 nodi', color='blue',   s=10)
ax.set_xlabel('Fidelity')
ax.set_ylabel('Media iterazioni')
ax.set(xticks=np.arange(0.5,1.01,0.05))
ax.legend()
plt.show()

fig, ax = plt.subplots()
ax.set_title('Media iterazioni in base a numero nodi - Gate Fidelity')

dfplot=df[df['Nodi']==3]
ax.scatter(dfplot['Gate Fidelity'],dfplot['Media iterazioni'], label='3 nodi', color='red', s=10)
dfplot=df[df['Nodi']==5]
ax.scatter(dfplot['Gate Fidelity'],dfplot['Media iterazioni'], label='5 nodi', color='green', s=10)
dfplot=df[df['Nodi']==7]
ax.scatter(dfplot['Gate Fidelity'],dfplot['Media iterazioni'], label='7 nodi', color='blue',    s=10)
ax.set_xlabel('Gate Fidelity')
ax.set_ylabel('Media iterazioni')
ax.set(xticks=np.arange(0.5,1.01,0.05))
ax.legend()
plt.show()


