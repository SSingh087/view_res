import h5py
import numpy as np
import matplotlib.pyplot as plt
from pycbc import transforms

f = h5py.File('./injection.hdf')

mchirp = np.array(f.get('mchirp'))
srcmass1 = np.array(f.get('srcmass1'))
srcmass2 = np.array(f.get('srcmass2'))
t = transforms.MchirpQToMass1Mass2()
q = t.inverse_transform({'mass1': srcmass1, 'mass2': srcmass2})
q = np.array(q.get('q'))

plt.figure(figsize=(10,10))

plt.subplot(221)
plt.hist2d(q, mchirp, cmap='Blues')
plt.xlabel('chirp mass')
plt.ylabel('mass ratio')
plt.colorbar(fraction=.05, pad=0.05,label='number of samples')

plt.subplot(222)
plt.hist2d(srcmass1, srcmass2, cmap='Blues')
plt.xlabel('mass1')
plt.ylabel('mass2')
plt.colorbar(fraction=.05, pad=0.05,label='number of samples')

plt.tight_layout()
plt.savefig('mchirp-description.pdf')
