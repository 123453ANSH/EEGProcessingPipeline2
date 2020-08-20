# EEGProcessingPipeline2
EEG Processing Pipeline in python

This EEG Processing pipeline starts with the preprocessing step. For preprocessing, this pipeline has two separate scripts, each of which processes EEG data from a different source file type. The two EEG scripts are below:

Script 1 - EEG_preprocessing.py - can preprocess EEG data from the .bdf file type.

Script 2 - setEEG_preprocessing.py - can preprocess EEG data from the .set file type. This is the file type Matlab stores EEG data in, so using this script allows one to use Matlab stored EEG data to conduct the EEG analysis.

Both process EEG data as described in Step 1. 

Step 1 - 

Preprocesses EEG data to get rid of artifact data from bad electrodes and applies several processing filters to the rest of data. Users can preprocess the EEG data in two different ways: manual or automatic removal of bad electrodes. Following this, both ways apply processing filters to the rest of the data.

-------------------------------------------------------------------------------------------------------------------------------------------------

Next is the postprocessing step. The postprocessing step and which .py files to use for this step are described below: 

Step 2 -

Conducts Epoch and Independent Component Analysis to visualize and see patient neuronal response to stimulus. Allows for comparison of different EEG recordings of the same patient with statistics that indicate change in behavior of neuronal signals. Comparison feature allows comparison of a participants' EEG recordings from pre, post, and followup trials in a research study. 

Note - the above only works for .bdf file types, and can be done by using the "analyze_Alan" and "analyze100_alan" scripts. Direction for how to use the scripts are in the scripts. For .set files, "SegmentingEEGDataFinal" is the script to do the above analysis; however, this script is not complete yet. Therefore, the above analysis cannot be done for EEG data in .set files.

-----------------------------------------------------------------------------------------------------------------------------------------------------
The entire EEG processing pipeline relies on the "Folder Structure" in this repository. This folder structure holds EEG data in very specific ways while the EEG processing is being conducted. Please read the directions in "EEG_preprocessing.py" and "setEEG_preprocessing.py" to understand how this folder structure holds data during the analysis process. Download and use this folder structure while processing EEG data.

Notes - 

1) No example data is provided because the file sizes are too big to be uploaded onto GitHub. Please contact me directly at anshverma@berkeley.edu for the example data.

2) Example formatting for the bad_channels csv has been provided. Copy this formatting while inputting your filenames and bad electrodes for the analysis to work.
