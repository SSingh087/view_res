import h5py
import numpy as np
import matplotlib.pyplot as plt

f = h5py.File('/work/shashwat.singh/3gsky/TaylorF2/config/injection.hdf')

coa_phase = np.array(f.get('coa_phase'))
comoving_volume  = np.array(f.get('comoving_volume'))
dec = np.array(f.get('dec'))
distance = np.array(f.get('distance'))
inclination = np.array(f.get('inclination'))
polarization = np.array(f.get('polarization'))
ra = np.array(f.get('ra'))
redshift = np.array(f.get('redshift'))
srcmass1 = np.array(f.get('srcmass1'))
srcmass2 = np.array(f.get('srcmass2'))

fig, axes = plt.subplots(nrows=2, ncols=5, figsize=[9.5, 6], dpi=500)

ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10 = axes.flat

ax1.hist(srcmass1)
ax2.hist(srcmass2)
ax3.hist(comoving_volume)
ax4.hist(redshift)
ax5.hist(distance)
ax6.hist(inclination)
ax7.hist(ra)
ax8.hist(dec)
ax9.hist(polarization)
ax10.hist(coa_phase)

ax1.set_title('srcmass1')
ax2.set_title('srcmass2')
ax3.set_title('comoving_volume')
ax4.set_title('redshift')
ax5.set_title('distance')
ax6.set_title('inclination')
ax7.set_title('ra')
ax8.set_title('dec')
ax9.set_title('polarization')
ax10.set_title('coa_phase')

plt.tight_layout()
plt.savefig('population-description.pdf')
