import glob
import h5py

fnames = glob.glob('summ.hdf')

files = {}
for fname in fnames:
    net = 'ET'
    time = '300'
    time = int(time)
    
    if net not in files:
        files[net] = {}
        
    files[net][time] = fname 

# use instead stellar formation rate prior
from pycbc.cosmology import cosmological_quantity_from_redshift, redshift
from numpy.random import uniform
from scipy.stats import gaussian_kde
import pylab
import numpy

inj = h5py.File('/work/shashwat.singh/3gsky/dummy-nhm/config/injection.hdf', 'r')
idist = inj['distance'][:]

# crude finite differencing is sufficient here

# stellar rate density from modified by cosmological time dilation
# https://arxiv.org/pdf/1403.0007.pdf
def stellar_rate(z):
    return 0.015 * (1 + z) ** 2.7 / (1 + ((1 + z) / 2.9) ** 5.6) / (1 + z)

z = redshift(idist)
cp = cosmological_quantity_from_redshift(redshift(idist + 0.01), 'comoving_volume')
cm = cosmological_quantity_from_redshift(redshift(idist - 0.01), 'comoving_volume')
w = (cp - cm) * stellar_rate(z)
w /= w.sum()


# Sets the assumed rate per volume
local_rate = 300
local_vol = cosmological_quantity_from_redshift(0.1, 'comoving_volume')
rate = local_vol / 1e9 * local_rate / w[redshift(idist) < 0.1].sum()
w *= rate

print(w.sum())

asizes = [0.1, 1, 10, 100, 1000, 44000]
alabel = ['A$_{90} <$ 0.1 deg$^2$', 
          'A$_{90} <$ 1 deg$^2$',
          'A$_{90} <$ 10 deg$^2$',
          'A$_{90} <$ 100 deg$^2$',
          'A$_{90} <$ 1000 deg$^2$',
          'All Sky']

def process(select):
    a90 = {}
    d90 = {}
    times = {}
    for net in files:
        for time in files[net]:
            fname = files[net][time]
            f = h5py.File(fname, 'r')
            print(f.keys())
            snr = f['snr'][:]
            k = snr > 12

            if net not in times:
                times[net] = []
            times[net].append(time)

            if net not in a90:
                a90[net] = {}
            for s in asizes:
                if s not in a90[net]:
                    a90[net][s] = []
                
                ak =  f['a90'][:] < s
                #print(f['a90'][:].min())
                wf = w[k & ak & select]
                e = ((wf ** 2.0).sum() / len(wf) - (wf.sum() / len(wf)) ** 2.0)
                e = (len(wf) * e) ** 0.5
                a90_num = wf.sum() 
                
                
                ds = idist[k & ak & select]
                l = ds.argsort()
                ds = ds[l]
                wcount = wf[l].cumsum() / wf.sum()

                if len(wcount) < 2:
                    dmax = 0
                else:
                    lmax = numpy.searchsorted(wcount, 0.9)
                    dmax = ds[lmax]
                
                a90[net][s].append((a90_num, e, dmax)) 

    for k in a90:
        times[k] = numpy.array(times[k])
        l = times[k].argsort()
        times[k] = times[k][l]
        for k2 in asizes:
            a90[k][k2] = numpy.array(a90[k][k2])[l]
    return times, a90

netname = {'ET':('E', 'solid', 's', 'purple')}

pylab.rc('text', usetex=True)
for dlimit in [20000, 1000, 500]:
    f, axs = pylab.subplots(2, 3, figsize=[9.5, 11], dpi=200, sharex=True, sharey='row')

    #total = cosmological_quantity_from_redshift(redshift(dlimit), 'comoving_volume')
    #rate = total / 1e9 * 300
    rate = w[idist < dlimit].sum()
    print(rate)
    
    for j, (s, aname) in enumerate(zip(asizes, alabel)):
        ps = []
        ls = []

        pylab.sca(axs[j // 3][j % 3])

        if dlimit < 20000:
            paname = aname + ', d$_L < {}$ Mpc'.format(dlimit)
        else:
            paname = aname + ', d$_L < 20$ Gpc'.format(dlimit)
        
        pylab.text(0.1, 0.95, paname,
         horizontalalignment='left',
         verticalalignment='center',
         backgroundcolor='white',
         transform = pylab.gca().transAxes)

        select = idist < dlimit
        times, a90 = process(select)
        print(times, a90)
        for i, net in enumerate(list(netname.keys())):
                label = net if j == 0 else None

                if net in netname:
                    label, lstyle, marker, color = netname[net]

                val = a90[net][s][:,0]
                print(val)
                e = a90[net][s][:,1]

                pylab.axhspan(rate, 1e6, linestyle='--', linewidth=1, color='grey')
                l = pylab.errorbar(times[net] / 60.0, val, yerr=e, marker=marker,
                                label=label, c=color, linestyle=lstyle, alpha=0.9)      

        if j == 5:
            pylab.legend(title='Detector Network', ncol=2, fontsize=9)

        pylab.yscale('log')
        pylab.xscale('log')
        pylab.xlim(xmin=35, xmax=0.9)

        if j >= 3:
            pylab.ylim(ymin=0.1, ymax=3e5 if rate > 1e5 else rate * 2.5)
        else:
            pylab.ylim(ymin=0.1, ymax=3e3 if rate > 1e3 else rate * 2.5)

        pylab.grid(which='major', color='darkgray')
        pylab.grid(which='minor', linewidth=0.4, color='lightgray')

        if j == 0 or j == 3:
            pylab.ylabel('Observations [$\\textrm{yr}^-1$]', fontsize=10)
        if j == 4:
            pylab.xlabel('Time to Merger [Minutes]', fontsize=10)

    pylab.tight_layout()
    pylab.subplots_adjust(wspace=.04, hspace=.05)
    pylab.savefig('area-{}.pdf'.format(dlimit))

for i, net in enumerate(list(netname.keys())):
    for j, (s, aname) in enumerate(zip(asizes, alabel)):
        for dlimit in [20000, 1000, 500]:
            select = idist < dlimit
            times, a90 = process(select)

            label = net if j == 0 else None

            if net in netname:
                label, lstyle, marker, color = netname[net]

            val = a90[net][s][:,0]
            e = a90[net][s][:,1]

            print(net, s, dlimit, times[net], val)

