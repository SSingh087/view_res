import h5py
import numpy
from pycbc.inference.io import loadfile
from pycbc.cosmology import distance_from_comoving_volume
from pycbc.conversions import snr_from_loglr
import healpy as hp
from numpy import pi
import glob

def idx_to_radec(index, nside):
    theta, phi = hp.pixelfunc.pix2ang(nside, index)
    return -(theta-pi/2.), pi*2. - phi

def radec_to_idx(ra, dec, nside):
    return hp.pixelfunc.ang2pix(nside, -dec + pi / 2.0, 2.0 * pi - ra)

fnames = glob.glob('inference/*INFERENCE*.hdf')
inj = h5py.File('/work/shashwat.singh/3gsky/dummy-nhm/config/injection.hdf', 'r')
injtime = inj['tc']

data = {}
for k in ['d50', 'd90', 'a50', 'a90', 'snr']:
    data[k] = numpy.zeros(len(injtime), dtype=numpy.float32)

for i, fname in enumerate(fnames):
    f = loadfile(fname, 'r')
    s = f.read_samples(['ra', 'dec', 'comoving_volume', 'loglr'])
    
    inj_idx = abs(injtime - f.attrs['trigger_time']).argmin()
    
    ra = s['ra']
    dec = s['dec']
    
    dist = distance_from_comoving_volume(s['comoving_volume'])
    snr = snr_from_loglr(s['loglikelihood'] - f['samples'].attrs['lognl'])
    snrp = snr.max()

    dist = numpy.sort(dist)
    d50 = dist[int(len(dist)*0.5)]
    d90 = dist[int(len(dist)*0.9)]

    nside = 10
    k = 100
    l = 0
    while k > 30 or l < 10:
        nside = int(nside * 1.5)
        area = 4 * pi * numpy.degrees(1.0)**2.0
        npix = hp.nside2npix(nside)

        parea = area / npix
        idx = radec_to_idx(ra, dec, nside)
        idx, count = numpy.unique(idx, return_counts=True)
        l = count.argsort()[::-1]

        idx = idx[l]
        count = count[l]
        wcount = count.cumsum() / len(ra)
        
        l = numpy.searchsorted(wcount, 0.5)
        a50 = l * parea

        l = numpy.searchsorted(wcount, 0.9)
        a90 = l * parea
        k = count[l]

    data['a90'][inj_idx] = a90
    data['a50'][inj_idx] = a50
    data['d90'][inj_idx] = d90
    data['d50'][inj_idx] = d50
    data['snr'][inj_idx] = snrp

    print(i, len(fnames), snrp, a90)

o = h5py.File('./summ.hdf', 'w')
for k in data:
    o[k] = data[k]
o.close()
