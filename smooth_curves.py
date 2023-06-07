import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import pandas as pd
import pyabf
import os
from pathlib import Path

# import typhon
# cm = plt.get_cmap('vorticity')
# colors = cm(np.linspace(0.2, 1, 12))

abf_dir = "C:/Users/joema/PycharmProjects/e phys plot/abf_dir/"
excel_dir = "C:/Users/joema/PycharmProjects/e phys plot/excel_dir/"

for root, dirs, files in os.walk(abf_dir):
    for file in files:
        abf_file_path = os.path.join(root, file)
        abf_file_stem = Path(abf_file_path).stem
        abf = pyabf.ABF(abf_file_path)
        figure = plt.figure(figsize=(9, 5))
        colors = plt.cm.Reds(np.linspace(0, 1, abf.sweepCount))

        x_data = abf.sweepX
        df = pd.DataFrame(x_data)

        for sweep in range(abf.sweepCount):
            try:
                abf.setSweep(sweepNumber=sweep, channel=1)
            except ValueError:
                print(abf_file_stem)
                abf.setSweep(sweepNumber=sweep, channel=0)
            y_data = abf.sweepY
            y_savgol = savgol_filter(y_data, 300, 3) # window size 75, polynomial order 4
            plt.plot(x_data, y_savgol, color=colors[sweep], linewidth=3, label=sweep)
            df = pd.concat([df, pd.Series(y_savgol)], axis=1)


        plt.legend()
        plt.close()
        # plt.show()

        trace_names = [f'Trace {i}' for i in range(abf.sweepCount + 1)]
        trace_names[0] = 'Time'
        df.columns = trace_names

        df.to_excel(excel_dir + f'Savgol Smooth_{abf_file_stem}.xlsx')
