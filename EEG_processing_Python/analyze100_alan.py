import mne
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# try reading as bdf
# fname = '100_emoDRWM.bdf'
# raw = mne.io.read_raw_edf(fname, preload=True)
# won't work, cannot read events from stim channel

# read the converted fif file
#fname = '100_EmoWorM.fif'
fname = '102_EmoWorM.fif'
raw = mne.io.Raw(fname, preload=True, add_eeg_ref=False)

# re-reference to the two mastoids
raw._data[:72] -= raw._data[67:69].mean(0)

raw.filter(l_freq=1, h_freq=30, n_jobs='cuda')

# plot the stim channel
# plt.plot(raw[-1][0][0])

# list the unique stim values
# print np.unique(raw[-1][0][0])

# extract the events
eve = mne.find_events(raw, stim_channel='Status')

# the value for distractor is 9994495
naps = eve[eve[:, 2]==9994495]
#naps = eve[eve[:, 2]==14188799]

# epoch the data
epo = mne.Epochs(raw, naps, None, tmin=-0.5, tmax=1, baseline=(None, 0),
                 preload=True, proj=False,
                 add_eeg_ref=False)

X = epo.get_data()

# read the behavioral data
bhv = np.genfromtxt('emo_results_20141124.txt', delimiter=',', dtype=None)
pdata = bhv[bhv['f1']=='Monica']

neu_pv = np.logical_and(pdata['f6']==0, pdata['f8']/2==0)
neg_pv = np.logical_and(pdata['f6']==0, pdata['f8']/2==1)
neu_wm = np.logical_and(pdata['f6']==1, pdata['f8']/4==0)
neg_wm = np.logical_and(pdata['f6']==1, pdata['f8']/4==1)

# compare the 4 conditions in an anova for each channel for each time point
F, p = stats.f_oneway(X[neu_pv], X[neg_pv], X[neu_wm], X[neg_wm])
sig = p<0.001

# plot the data
fig = plt.figure()
a = 0.1
ylim = [-5e-5, 5e-5]
for n in range(72):
    
    x = X[:, n].mean(0)
    e = X[:, n].std(0)/np.sqrt(X.shape[0])
    ax = fig.add_subplot(9, 8, n+1)
    #ax.plot(epo.times, x)
    #ax.fill_between(epo.times, x-e, x+e, alpha=0.5)
    
    for cond, c in zip([neu_pv, neg_pv, neu_wm, neg_wm], ['c', 'm', 'b', 'r']):
        ax.plot(epo.times, X[cond, n].mean(0), c)
        ax.fill_between(epo.times,
                        X[cond, n].mean(0)-X[cond, n].std(0),
                        X[cond, n].mean(0)+X[cond, n].std(0),
                        color=c, alpha=a)
    
    if sig[n].sum() > 0:
        for s in np.where(sig[n]):
            ax.plot([epo.times[s], epo.times[s]], ylim, 'k', alpha=0.1)
    
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(epo.ch_names[n])
    ax.plot([0, 0], ylim, 'k--')
    ax.set_ylim(ylim)   
    

plt.show()

