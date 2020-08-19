import numpy as np
import mne

PIDS = [100, 102, 103, 105, 106, 107]

for pid in PIDS:

    raw_fname = 'P%d/%d_EmoWorM_fs256_05hz30hz_raw.fif' % (pid, pid)
    eve_fname = 'P%d/%d_EmoWorM_stim-eve.fif' % (pid, pid)

    raw = mne.io.Raw(raw_fname, preload=True, add_eeg_ref=False, proj=False)
    eve = mne.read_events(eve_fname)

    epo = mne.Epochs(raw, eve, None, -0.2, 2, preload=True, proj=False, 
                     add_eeg_ref=False)

    epo_fname = 'P%d/%d_EmoWorM_epo.fif' % (pid, pid)
    epo.save(epo_fname)
