# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 16:23:23 2019

@author: Ansh Verma
"""
# documentation on how to create epochs (what this script is for) - https://martinos.org/mne/dev/auto_tutorials/epochs/plot_epoching_and_averaging.html#tut-epoching-and-averaging
# documentation on find_events function - https://martinos.org/mne/dev/generated/mne.find_events.html

def plottingdata(): 
    import os
    import mne 

    PREPROCESSED_FILEPATH = 'C:\\Users\\Ansh Verma\\Documents\\EEG_Processing_File_Structure\\Folder Structure\\Preprocessed'
   
    for root, dirs, filenames in os.walk(PREPROCESSED_FILEPATH):
        PREPROCESSED_FILEPATH = 'C:\\Users\\Ansh Verma\\Documents\\EEG_Processing_File_Structure\\Folder Structure\\Preprocessed'
        for file in filenames:
            raw = mne.io.read_raw_fif(PREPROCESSED_FILEPATH + '\\' + file, preload=True)
            raw.info()

            raw.set_eeg_reference('average', projection=True)  # set EEG average reference
            order = np.arange(raw.info['nchan'])
            print(order)
            #see mne documentation for a fuller explanation of the below 
            #essentially, the below can only be used when the "stim" channel is with the EEG channels
          #  order[9] = 312  # We exchange the plotting order of two channels
          # order[20] = 20  # to show the trigger channel as the 10th channel.
            raw.plot(n_channels=21, order=order, block=True)
         
            
def something(): #attempting to see if can actually find the event field in .set file struct
    #it is there, because when graphing the above function the eventmarkers are present (it has to find this data from somewhere!)
    import os
    import mne 
    PREPROCESSED_FILEPATH = 'C:\\Users\\Ansh Verma\\Documents\\EEG_Processing_File_Structure\\Folder Structure\\Preprocessed'
    for root, dirs, filenames in os.walk(PREPROCESSED_FILEPATH):
            raw = mne.io.read_raw_fif(PREPROCESSED_FILEPATH + '\\' + file, preload=True)
            events = mne.find_events(raw, 'latency')
            print('Found %s events, first five:' % len(events))
            print(events[:5])

        #below is to create the epochs, which can only happen if we can locate the events
         #   baseline = (None, 0.0)  
         #   epochs = mne.Epochs(raw, events=events, event_id=event_id, tmin=tmin,tmax=tmax, baseline=baseline, reject = None,picks=('meg', 'eog'))  # only include MEG and EOG
         #   epochs.plot(block=True)

            
            
        