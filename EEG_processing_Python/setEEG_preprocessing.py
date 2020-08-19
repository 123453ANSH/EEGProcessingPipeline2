###############################################################################
################### Neuroelectrics 20 ELECTRODE CAP EEG-PREPROCESSING #################################
######################### BY: RIAN BOGLEY & AJ SIMON & ANSH VERMA ##########################
###############################################################################

# MANUAL WORKFLOW
# 1. Ensure filepaths are correct and bad electrodes CSV is updated.
# 2. Run the whole script.
# 3. Run "pre_pp()".
# Loads any raw .bdf files that haven't been read before converting them into
# the .fif format from now on. Drops any channels that are not the main 64
# electrode channels (i.e. EOG, EMG, etc.). Sets digitized electrode locations
# according to standard 10-5 system (primarily for plotting purposes). Checks
# if the file exists within the "bad_channels.csv", if it does, it designates
# any listed channels as 'bads' and saves the file to the "Pre_ICA" folder,
# if it doesn't, it saves the file to the "Pre_Bads" folder for manual bad
# electrode inspection.
# 4. Run "manual_bads()", inspect channels, then run "bads_assign()". Repeat.
# Any files which did not have information listed in the "bad_channels.csv"
# and were thus sent to the "Pre_Bads" folder require manual inspection
# in order to identify any potential bad electrodes. The "manual_bads()"
# function will load the data and plot all 64 channels in a clamped format
# to easily identify any highly distorted channels. Then, the "bads_assign()"
# function first asks if any channels were bad, and if so, which? For any bad
# channels, write the name exactly as they are listed on the plot. Once the
# file has been examined it will be saved to the "Pre_ICA" folder, then when
# "manual_bads()" is run again, it will delete any files that have been
# inspected and exist in "Pre_ICA". Re-run these two commands until the message
# "No files remain." appears, in which case the "Pre_Bads" folder is empty.
# 5. Run "pre_ica()".
# Performs a band-pass filter (1hz-40hz) using the "firwin" design. Resamples
# the data from 2048 to 1024. Interpolates the data of any bad channels from
# surrounding channels. Runs ICA on the data using the "Fast-ICA" method and
# up to 64 components. Saves both the updated file and a separate file
# containing the ICA data to the "Post_ICA" and "Manual_Post_ICA" folders.
# 6. Run "manual_ica()", inspect components, then run "ica_assign()". Repeat.
# The "manual_ica()" function loads a file and it's corresponding ICA data file
# from the "Manual_Post_ICA" folder, then plots the topographical view of each
# of the 64 ICA components as well as plots the sources for all components for
# inspection. Check both the topographical and time series for any components
# that appear to potentially be artifacts to ensure they match the characteristics
# of a blink, or lateral eye movement, etc. Once they are decided upon, run the
# "ica_assign()" function to list any bad components found, ensuring to list them
# as integers (e.g. ICA001 becomes 1, or ICA022 becomes 22), which are then
# zeroed out. Finally, all the channels are re-referenced to the average of
# the data and saved to the "Manual_Preprocessed" folder.

###############################################################################

# AUTO WORKFLOW
# Only use this pathway if all files you wish to preprocess have been examined
# during data collection for bad electrode channels and appropriately entered
# into the "bad_channels.csv", and the automatic ICA artifact detection has
# been fixed in the "auto_ica()" function below.
# 1. Ensure filepaths are correct and bad electrodes CSV is updated.
# 2. Run the whole script.
# 3. Run "full_auto_pp()".
# This will run "pre_pp()", followed by "pre_ica()", followed by "auto_ica()".
# Both "pre_pp()" and "pre_ica" function the same as in the manual workflow,
# but "auto_ica()" currently uses MNE's built-in automatic ICA analysis function
# which has 3 primary statistical criterion (skewness, kurtosis, & variance)
# for determining potential artifacts. Currently, this method is unreliable
# and manual analysis is recommended, but once this function is updated to
# satisfactory standards, this would be the ideal workflow to run. Files run
# this way end up in the "Preprocessed" folder (not "Manual_Preprocessed").

###############################################################################
############################## INITIALIZATION #################################
###############################################################################

# import modules
import mne, glob, os, pandas as pd

# THESE ARE ALL THE MASTER FILEPATHS, THESE CAN BE CHANGED TO THE APPROPRIATE
# DIRECTORIES AND WILL CHANGE ALL LOCATIONS BELOW IN THE CODE

#location of raw files (.bdf format)
RAW_FILEPATH = 'C:\\Users\\Ansh Verma\\Documents\\EEG_Processing_File_Structure\\Folder Structure\\Raw\\'
#location of files that did not have bad electrode information stored in the
#bad_channels.csv and require manual inspection for faulty electrode channels
PRE_BADS_FILEPATH = 'C:\\Users\\Ansh Verma\\Documents\\EEG_Processing_File_Structure\\Folder Structure\\Pre_Bads\\'
#location of files that have been inspected for potential bad electrode
#channels and are ready for ICA
PRE_ICA_FILEPATH = 'C:\\Users\\Ansh Verma\\Documents\\EEG_Processing_File_Structure\\Folder Structure\\Pre_ICA\\'
#location of all files that have been run through ICA and are ready for auto ICA inspection
POST_ICA_FILEPATH = 'C:\\Users\\Ansh Verma\\Documents\\EEG_Processing_File_Structure\\Folder Structure\\Post_ICA\\'
#location of all files that have been run through ICA and are ready for manual ICA inspection
MANUAL_POST_ICA_FILEPATH = 'C:\\Users\\Ansh Verma\\Documents\\EEG_Processing_File_Structure\\Folder Structure\\Manual_Post_ICA\\'
#location of completely preprocessed files from manual ICA analysis
MANUAL_PREPROCESSED_FILEPATH = 'C:\\Users\\Ansh Verma\\Documents\\EEG_Processing_File_Structure\\Folder Structure\\Manual_Preprocessed\\'
#location of completely preprocessed files from auto ICA analysis
PREPROCESSED_FILEPATH = 'C:\\Users\\Ansh Verma\\Documents\\EEG_Processing_File_Structure\\Folder Structure\\Preprocessed\\'
#location of CSV containing bad electrode information
CSV_FILEPATH = 'C:\\Users\\Ansh Verma\\Documents\\EEG_Processing_File_Structure\\Folder Structure\\bad_channels.csv'

#THESE ARE THE MASTER GLOBS OF FILES IN THE MASTER FILEPATHS, THESE ARE UPDATED
#IN SOME OF THE MANUAL STEPS BELOW, THEREFORE CHANGING THEM HERE ONLY MAY CAUSE
#ERRORS, SO DO NOT CHANGE THESE UNLESS NECESSARY

RAW_FILES = [] # originally RAW_FILES = glob.glob(RAW_FILEPATH  + '*.bdf' )
# the commented out above doesn't add any filepaths to list, but this might be an error of me  

for root, dirs, filenames in os.walk(RAW_FILEPATH ):
    for file in filenames:
        RAW_FILES.append(RAW_FILEPATH + '\\'+file)
#alternative to getting raw_files list full of appropriate files 
        
        
PRE_BADS_FILES = glob.glob(PRE_BADS_FILEPATH + '*.fif')
PRE_ICA_FILES = glob.glob(PRE_ICA_FILEPATH + '*.fif')
POST_ICA_FILES = glob.glob(POST_ICA_FILEPATH + '*.fif')
MANUAL_POST_ICA_FILES = glob.glob(MANUAL_POST_ICA_FILEPATH + '*.fif')
MANUAL_PREPROCESSED_FILES = glob.glob(MANUAL_PREPROCESSED_FILEPATH + '*.fif')
PREPROCESSED_FILES = glob.glob(PREPROCESSED_FILEPATH + '*.fif')

# reads the bad electrode CSV as a pandas dataframe and gets rid of N/A entries
CSV_df = pd.read_csv(CSV_FILEPATH)
csv_df = CSV_df.fillna(0)


        


###############################################################################
########################### PRE-PREPROCESSING STEP ############################
###############################################################################

def pre_pp():
    print(len(RAW_FILES))
    for file in RAW_FILES:
        if(file[-2] == "d"): #if the fdt file (must accompany the .set file that this script is loading in)
            #don't load the fdt file in! 
            continue
        else: #if the .set file, run the below 
            print(file)
        # sets up the output filepaths/filenames
            file_name = os.path.basename(os.path.normpath(file))
            pre_bads_filepath = PRE_BADS_FILEPATH + file_name[0:-4] + '_Pre_Bads.fif' 
            pre_ica_filepath = PRE_ICA_FILEPATH + file_name[0:-4] + '_Pre_ICA.fif'
            # checks if this file has already been through this step
            exists = os.path.isfile(pre_ica_filepath) or os.path.isfile(pre_bads_filepath)
        # if already exists, skips this step for this file, if not, runs
            if not exists:
            # imports raw .set data (thereby converting to .fif format)
                raw = mne.io.read_raw_eeglab(file,None, eog=(), preload=True, uint16_codec=None, verbose=None)
            # drops channels so that only EEG channels remain
                drop_channels = raw.ch_names[20:len(raw.ch_names)]
                raw.drop_channels(drop_channels)
            # sets eeg locations to standard 10-5 system
                locations = mne.channels.read_montage(kind='standard_1005')
            # applies digitized locations montage to raw data for visualization
                raw.set_montage(locations, set_dig=True)
            # check if bad electrode data exists in master CSV
                trode_file_list = csv_df['Raw Filename (.bdf format)']
                for bad_trode_filex, bad_trode_file in enumerate(trode_file_list):
                # if listed, add bad electrode to raw file's info & save to "Pre_ICA" folder
                    if RAW_FILEPATH + bad_trode_file == file:
                        raw.info['bads'] = [csv_df.iloc[bad_trode_filex][1]]
                        if raw.info['bads'] == [0]:
                            raw.info['bads'] = []
                            raw.save(pre_ica_filepath)
            # if not listed, save to "Pre_Bads" folder for manual bad electrode inspection
                ica_exists = os.path.isfile(pre_ica_filepath)
                if not ica_exists:
                    raw.save(pre_bads_filepath)


###############################################################################
#################### BAD ELECTRODE MANUAL ASSIGNMENT STEP #####################
###############################################################################

def manual_bads():
    # every time this step is run, the list of files in the "Pre_Bads" folder needs resetting
    PRE_BADS_FILES = glob.glob(PRE_BADS_FILEPATH + '*.fif')
    # if the "Pre_Bads" folder is not empty, runs
    if not PRE_BADS_FILES == []:
        # choose the first file in the folder
        file = PRE_BADS_FILES[0]
        file_name = os.path.basename(os.path.normpath(file))
        # if the file has been run through this step and the bads_assign(),
        # removes the file and re-runs this step to select next file (if any)
        pre_ica_filepath = PRE_ICA_FILEPATH + file_name[0:-8] + 'ICA.fif'
        exists = os.path.isfile(pre_ica_filepath)
        if exists:
            os.remove(file)
            manual_bads()
        # if the file has not been run through this step or bads_assign(), runs
        if not exists:
            raw = mne.io.read_raw_fif(file, preload=True)
            # plots all 64 EEG channels (in a clamped format so that very noisey
            # channels are easier to identify)
            raw.plot(n_channels=20, clipping='clamp')
            # it is recommended to keep these plots open in a separate window
            # while running the next step; "bads_assign()"
            print('When done inspecting for bad electrode channels in this file, run function: "bads_assign()"')
    # if the "Pre_Bads" folder is empty, prints "No files remain."
    else:
        print('No files remain.')


###############################################################################

def bads_assign():
    # every time this step is run, the list of files in the "Pre_Bads" folder needs updating
    PRE_BADS_FILES = glob.glob(PRE_BADS_FILEPATH + '*.fif')
    # if the "Pre_Bads" folder is not empty, runs
    if not PRE_BADS_FILES == []:
        # choose the first file in the folder
        file = PRE_BADS_FILES[0]
        file_name = os.path.basename(os.path.normpath(file))
        # checks if the file has been run through this step already, if not, runs
        pre_ica_filepath = PRE_ICA_FILEPATH + file_name[0:-8] + 'ICA.fif'
        exists = os.path.isfile(pre_ica_filepath)
        if not exists:
            raw = mne.io.read_raw_fif(file, preload=True)
            # asks if any electrode channels were bad
            prompt_trodes = input('Are there any bad electrodes? (1 = Yes, 2 = No): ')
            # if bad channels exist, asks to list any channels and designates them as "bads"
            # then saves file to "Pre_ICA" folder
            if prompt_trodes == '1':
                bad_trodes = input('List bad electrodes (separated by commas): ')
                raw.info['bads'] = [bad_trodes]
                raw.save(pre_ica_filepath)
            # if no bad channels, saves to "Pre_ICA" folder without changing "bads"
            elif prompt_trodes == '2':
                raw.save(pre_ica_filepath)
        print('When done assigning bad electrodes to this file, re-run function "manual_bads()" until folder is empty.')
    # if the "Pre_Bads" folder is empty, prints "No files remain."
    else:
        print('No files remain.')


###############################################################################
################################ PRE-ICA STEP #################################
###############################################################################

def pre_ica():
    # ensures that when this function is run, the "Pre_ICA" list is updated
    PRE_ICA_FILES = glob.glob(PRE_ICA_FILEPATH + '*.fif')
    for file in PRE_ICA_FILES:
        file_name = os.path.basename(os.path.normpath(file))
        # sets up output filepaths/filenames for automatic ICA pathway
        post_ica_filepath = POST_ICA_FILEPATH + file_name[0:-11] + 'Post_ICA.fif'
        ica_data_filepath = POST_ICA_FILEPATH + file_name[0:-11] + 'Post_ICA_data.fif'
        # sets up output filepaths/filenames for manual ICA pathway
        manual_post_ica_filepath = MANUAL_POST_ICA_FILEPATH + file_name[0:-11] + 'Post_ICA.fif'
        manual_ica_data_filepath = MANUAL_POST_ICA_FILEPATH + file_name[0:-11] + 'Post_ICA_data.fif'
        # sets up both the manual and automatic preprocessed filepaths/filenames
        # to check if the file has already been run through either pathway
        preprocessed_filepath = PREPROCESSED_FILEPATH + file_name[0:-11] + 'Preprocessed.fif'
        manual_preprocessed_filepath = MANUAL_PREPROCESSED_FILEPATH + file_name[0:-11] + 'Preprocessed.fif'
        # check if post ICA or preprocessed files already exist, if not runs
        exists = os.path.isfile(post_ica_filepath) or os.path.isfile(manual_post_ica_filepath) or os.path.isfile(
            preprocessed_filepath) or os.path.isfile(manual_preprocessed_filepath)
        if not exists:
            raw = mne.io.read_raw_fif(file, preload=True)
            mne.pick_types(raw.info, meg=False, eeg=True, eog=False, stim=False, exclude='bads')
            # performs a band-pass filter between 1.0hz-40.0hz using "firwin" design
            high_cutoff = 40.0
            low_cutoff = 1.0
            raw.filter(l_freq=low_cutoff, h_freq=high_cutoff, fir_design='firwin')
            # downsamples to 1024 from 2048
            raw.resample(sfreq=1024, npad='auto')
            # interpolates any bad electrode channels's data using surrounding electrodes
            raw.interpolate_bads(reset_bads=False, verbose=False)
            # after interpolation of bad channels, resets list of "bads" to empty
            raw.info['bads'] = []
            # performs ica on data using FastICA method, then fits to data
            ica = mne.preprocessing.ICA(random_state=0, n_components=20, method='fastica')
            ica.fit(raw)
            # saves both the file & ICA data to the "Manual_Post_ICA" and "Post_ICA" folders
            raw.save(post_ica_filepath)
            ica.save(ica_data_filepath)
            raw.save(manual_post_ica_filepath)
            ica.save(manual_ica_data_filepath)


###############################################################################
####################### MANUAL POST-ICA ANALYSIS STEP #########################
###############################################################################

def manual_ica():
    # every time this step is run, the list of files in the "Manual_Post_ICA" folder needs updating
    MANUAL_POST_ICA_FILES = glob.glob(MANUAL_POST_ICA_FILEPATH + '*.fif')
    # creates two glob lists, one for the main files, and one for the corresponding ICA data files
    manual_post_ica_files = glob.glob(MANUAL_POST_ICA_FILEPATH + '*_ICA.fif')
    manual_ica_data_files = glob.glob(MANUAL_POST_ICA_FILEPATH + '*_ICA_data.fif')
    # if "Manual_Post_ICA" folder is not empty, runs
    if not MANUAL_POST_ICA_FILES == []:
        # loads the first file and first ICA data file in the folder
        file = manual_post_ica_files[0]
        file_ica = manual_ica_data_files[0]
        file_name = os.path.basename(os.path.normpath(file))
        # sets up the output filepath/filename and checks if such a file already exists
        manual_preprocessed_filepath = MANUAL_PREPROCESSED_FILEPATH + file_name[0:-12] + 'Preprocessed.fif'
        exists = os.path.isfile(manual_preprocessed_filepath)
        # if it exists, remove the file and corresponding ICA data file from the
        # "Manual_Post_ICA" folder to reduce redundant files from building up.
        # NOTE: An exact copy of the Post_ICA file and ICA data file can be found
        # in the "Post_ICA" folder which is not cleared after automatic runs
        if exists:
            os.remove(file)
            os.remove(file_ica)
            manual_ica()
        # if the file has not been manually preprocessed yet, runs
        if not exists:
            raw = mne.io.read_raw_fif(file, preload=True)
            ica = mne.preprocessing.read_ica(file_ica)
            # plots the 64 ICA components topographically over the digitized
            # electrode location maps
            ica.plot_components()
            # plots the same components as a time series for temporal inspection
            ica.plot_sources(raw)
            # it is recommended to keep these plots open in a separate window
            # while running the next step; "ica_assign()"
            print('When done inspecting for bad electrode channels in this file, run function: "ica_assign()"')
        # if the "Post_ICA" folder is empty, prints "No files remain."
        else:
            print('No files remain.')


###############################################################################

def ica_assign():
    # every time this step is run, the list of files in the "Manual_Post_ICA" folder needs updating
    MANUAL_POST_ICA_FILES = glob.glob(MANUAL_POST_ICA_FILEPATH + '*.fif')
    # creates two glob lists, one for the main files, and one for the corresponding ICA data files
    manual_post_ica_files = glob.glob(MANUAL_POST_ICA_FILEPATH + '*_ICA.fif')
    manual_ica_data_files = glob.glob(MANUAL_POST_ICA_FILEPATH + '*_ICA_data.fif')
    # if "Manual_Post_ICA" folder is not empty, runs
    if not MANUAL_POST_ICA_FILES == []:
        # loads the first file and first ICA data file in the folder
        file = manual_post_ica_files[0]
        file_ica = manual_ica_data_files[0]
        file_name = os.path.basename(os.path.normpath(file))
        # sets up the output filepath/filename and checks if such a file already exists
        manual_preprocessed_filepath = MANUAL_PREPROCESSED_FILEPATH + file_name[0:-12] + 'Preprocessed.fif'
        exists = os.path.isfile(manual_preprocessed_filepath)
        # if no such file is found, runs
        if not exists:
            raw = mne.io.read_raw_fif(file, preload=True)
            ica = mne.preprocessing.read_ica(file_ica)
            # asks if any components were identified as potential artifacts in "manual_ica()"
            prompt_ica = input('Are there any artifacts identified by ICA? (1 = Yes, 2 = No): ')
            # if yes, runs
            if prompt_ica == '1':
                # list any bad components by number as they appeared on the plots
                # (i.e. "ICA001" should be listed as "1", "ICA022" = "22", etc.)
                prompt_bad_comps = input('List artifact components (separated by commas): ')
                # changes input into list of integers for ica.exclude to run properly
                exclusions = [int(s) for s in prompt_bad_comps.split(',')]
                ica.exclude = exclusions
                # zeroes out any components listed for exclusion
                ica.apply(raw)
                # re-references all remaining channels to the average
                raw.set_eeg_reference('average')
                # saves file to "Manual_Preprocessed" folder
                raw.save(manual_preprocessed_filepath)
            # if no, runs
            elif prompt_ica == '2':
                ica.apply(raw)
                # re-references all remaining channels to the average
                raw.set_eeg_reference('average')
                # saves file to "Manual_Preprocessed" folder
                raw.save(manual_preprocessed_filepath)
        print('When done inspecting for bad electrode channels in this file, run function: "manual_ica()"')
    # if the "Manual_Post_ICA" folder is empty, prints "No files remain."
    else:
        print('No files remain.')


###############################################################################
######################## AUTO POST-ICA ANALYSIS STEP ##########################
###############################################################################

def auto_ica():
    # creates two glob lists, one for the main files, and one for the corresponding ICA data files
    post_ica_files = glob.glob(POST_ICA_FILEPATH + '*_ICA.fif')
    post_ica_ica_files = glob.glob(POST_ICA_FILEPATH + '*_ICA_data.fif')
    # converts the two glob lists into a dictionary
    post_ica_dict = {'EEG': post_ica_files, 'Components': post_ica_ica_files}
    # converts the dictionary into a Pandas dataframe with two columns "EEG" & "Components"
    post_ica_df = pd.DataFrame(post_ica_dict, columns=['EEG', 'Components'])
    post_ica_df_eeg = post_ica_df['EEG']
    # loops through each file & corresponding ICA data file in the "Post_ICA" folder
    for filex, file in enumerate(post_ica_df_eeg):
        file_name = os.path.basename(os.path.normpath(file))
        # sets up the output filepath/filename and checks if such a file already exists
        # if not, runs
        preprocessed_filepath = PREPROCESSED_FILEPATH + file_name[0:-12] + 'Preprocessed.fif'
        exists = os.path.isfile(preprocessed_filepath)
        if not exists:
            raw = mne.io.read_raw_fif(file, preload=True)
            file_ica = post_ica_df.iloc[filex][1]
            ica = mne.preprocessing.read_ica(file_ica)
            # runs MNE's automatic artifact detection function on the raw data
            # this function has three main criterion for deciding which components
            # are potentially artifacts:
            # skewness: "skew_criterion = None"
            # kurtosis: "kurt_criterion = None"
            # variance: "var_criterion = None"
            # any combination of these can be used, for example:
            # if none are used, it will run all three types of analysis
            # if all three are used, it will run none (this renders the function null)
            # to just run kurtosis, it would look like:
            # "ica.detect_artifacts(raw, skew_criterion = None, var_criterion = None)"
            ica.detect_artifacts(raw)
            # zeroes out any components automatically identified as artifacts
            ica.apply(raw)
            # re-references all remaining channels to the average
            raw.set_eeg_reference('average')
            # saves file to "Preprocessed" folder
            raw.save(preprocessed_filepath)


###############################################################################
###############################################################################        
###############################################################################
            

def full_auto_pp():
    # runs all functions in the automatic pathway
    pre_pp()
    pre_ica()
    auto_ica()
    PRE_ICA_FILES = glob.glob(PRE_ICA_FILEPATH + '*.fif')
    POST_ICA_FILES = glob.glob(POST_ICA_FILEPATH + '*.fif')
    PREPROCESSED_FILES = glob.glob(PREPROCESSED_FILEPATH + '*.fif')
