#https://basemaptutorial.readthedocs.io/en/latest/plotting_data.html
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

plt.figure(figsize=(9,5))
map = Basemap(projection='moll', lat_0=0, lon_0=0)

map.drawmapboundary()
map.drawcoastlines()

xs, ys = map(180/np.pi*ra, 180/np.pi*dec)

map.scatter(xs, ys, marker='X', color='black', label='Source')

#for i in range(len(lonss)):
#    plt.annotate("P"+str(i+1), (xs[i],ys[i]), xycoords='data',
#                 xytext=(15,-10), textcoords="offset points")#, fontsize=5)

plt.legend(bbox_to_anchor=(0.3, 1.0))#, fontsize=4, ncol=2)

