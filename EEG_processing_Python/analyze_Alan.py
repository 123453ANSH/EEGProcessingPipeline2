import mne
import numpy as np
import matplotlib.pyplot as plt
import time

t0 = time.time()

mne.set_log_level(False)

# load the behavioral data
col_names = ['data', 'first', 'last', 'age', 'gender', 'block_num',
             'block_type', 'trial_num', 'trial_type', 'correct', 'rt']
bhv = np.genfromtxt('emo_results_20141124.txt', delimiter=',', dtype=None,
                    names=col_names)

lout = mne.layouts.read_layout('biosemi64.lout', path='.')
pid = 100
name = 'Cammie'
#pids = [100, 102, 103]
#names = ['Cammie', 'AJ', 'Monica']
#for pid, name in zip(pids, names):
if True:
    eve_fname = '%d_EmoWorM-eve.fif' % pid
    raw_fname = '%d_EmoWorM_fs256_1hz30hz_raw.fif' % pid

    # read the raw data
    raw = mne.io.Raw(raw_fname, preload=True, add_eeg_ref=False)
    raw.ch_names[:69] = lout.names
 
    # read the events
    eve = mne.read_events(eve_fname)
    eve[:, 0] /= 8

    # replace Fpz with EXG8
    raw._data[32] = raw._data[71]    

    # define the channels
    picks = range(69)

    # epoch the data
    epo = mne.Epochs(raw, eve, 33023, -0.2, 1, proj=False, preload=True,
                     picks=picks) 

    # perform ica on the data
    ica = mne.preprocessing.ICA(n_components=69)
    ica.fit(epo)

    # get the corresponding behavioral data
    pdata = bhv[bhv['first']==name]
    
    btype = pdata['block_type']
    emo = pdata['trial_type'] / (2*btype+2)
    
    

    evo = [epo[emo.astype(bool)].average(), epo[~emo.astype(bool)].average()]

    # reconstruct epochs from ica sources
    src_epo = ica.get_sources(epo)

    n = 0
    X = src_epo.get_data()[:, n, :]

    fig = mne.viz.plot_ica_components(ica, picks=n, ch_type='eeg',
                                      layout=lout)
    ax1 = fig.get_axes()[0]
    ax1.set_position([0, 0, 0.5, 1])
    
    ax2 = fig.add_axes([0.55, 0.55, 0.4, 0.4])
    ax2.imshow(X)
    bbx = list(ax2.get_position().bounds)
    bbx[1] = 0.05

    ax3 = fig.add_axes(bbx)
    ax3.plot(epo.times, X.mean(0))
    ax3.fill_between(X.mean(0)-X.std(0), X.mean(0)+X.std(0))

    fig.canvas.draw()

print time.time()-t0
plt.show()
