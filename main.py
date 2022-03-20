import pyabf
import os
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

abf_files = []
file_names_text = []
folder_path = 'C:/Users/joema/PycharmProjects/abf scratch/abf files/rgc/'

for file in os.listdir(folder_path):
    abf = pyabf.ABF(folder_path + file)
    abf_files.append(abf)
    cap_file_t = Path(folder_path + file).stem
    file_names_text.append(cap_file_t)


# Fix the bug that the y axis is formatted from a single sweep not all of them.
def e_phys_plot(f, x_limits, stim, clamp, sweep_range=(0, None), color_scheme='mono', color_range=(0.4, 1)):
    """f accepts an integer value corresponding to the filelocation in abf_files
    x_limits sets the range of x values you want to plot
    stim accepts 'light' or 'current'
    clamp accepts v or i
    sweep_range sets a continuous range of sweeps you want to plot from the abf file. Default is all the sweeps
    color_scheme is default 'mono' for monochrome. If you type 'multi' you can plot each sweep a different color
    if you choose multi, you can change the color range for the traces. It accepts a three-member tuple. The first
        two values define the range of colors from the colormap. Lower numbers are lighter and higher numbers are
        darker. 0 is min and 1 is max."""

    # Inputs assigned
    x_lower, x_upper = x_limits
    color_range_lower, color_range_upper= color_range
    first_sweep, last_sweep = sweep_range
    abf = abf_files[f]
    first_sweep, last_sweep = sweep_range
    if last_sweep is None:
        last_sweep = abf.sweepCount

    # Plot monochrome or multi-color
    mono = False
    if color_scheme == 'mono':
        c = '#3c1361'
        mono = True

    colors = plt.cm.Purples(np.linspace(color_range_lower, color_range_upper, last_sweep - first_sweep + 1))

    # Plot each sweep
    list_of_sweeps = list(range(first_sweep, last_sweep))

    for sweep in range(0, last_sweep - first_sweep):
        abf.setSweep(sweepNumber=list_of_sweeps[sweep], channel=0)
        if mono:
            plt.plot(abf.sweepX, abf.sweepY, color=c)
        else:
            plt.plot(abf.sweepX, abf.sweepY, color=colors[sweep])

    # Format Plots
    y_values = abf.sweepY
    max_y = max(y_values)
    min_y = min(y_values)

    if max_y < 0:
        upper_y_lim = ((-1.01 * max_y) + max_y) + max_y
    else:
        upper_y_lim = 1.01 * max_y
    lower_y_lim = 1.01 * min_y

    plt.ylim(lower_y_lim, upper_y_lim)
    plt.xlim(x_lower, x_upper)
    plt.xlabel('time (ms)', fontsize=17)
    if clamp == 'i':
        plt.ylabel('Voltage (mv)', fontsize=17)
    else:
        plt.ylabel('Current (units?)', fontsize=17)

    if stim == 'light':
        plt.title('Light Stimulation Protocol', fontsize=20)
    else:
        plt.title('Current Stimulation Protocol', fontsize=20)
    plt.show()


e_phys_plot(9, (0, 7.5), color_scheme='multi', stim='light', clamp='i')

