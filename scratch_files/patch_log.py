import pyabf
import pandas as pd
import os
from datetime import datetime
import glob


def path_log(abf_directory_path):
    abf_filepaths = glob.glob(os.path.join(abf_directory_path, "*.abf"))
    today_str_date = datetime.today().strftime('%Y-%m-%d')
    protocol_list = []
    sweep_count_list = []
    creation_times = []

    for abf_path in abf_filepaths:
        file_creation_time = datetime.fromtimestamp(os.path.getmtime(abf_path)).strftime('%H:%M:%S')
        abf_object = pyabf.ABF(abf_path)
        protocol = abf_object.protocol
        sweeps = abf_object.sweepCount
        protocol_list.append(protocol)
        sweep_count_list.append(sweeps)
        creation_times.append(file_creation_time)

    protocol_list = pd.Series(protocol_list)
    sweep_count_list = pd.Series(sweep_count_list)
    filenames = pd.Series([os.path.basename(i) for i in abf_filepaths])
    creation_times = pd.Series(creation_times)

    df = pd.concat([filenames, protocol_list, sweep_count_list, creation_times], axis=1)
    df.columns = ['Filename', 'Protocol', 'Sweep Count', 'Time']
    df.to_excel(f'Patch Log_Ran_On_{today_str_date}.xlsx')
