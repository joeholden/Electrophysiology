import pathlib
import pyabf
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.signal import savgol_filter
import numpy as np
import statistics as stats
import pandas as pd
import os
from datetime import datetime
import glob


def show_trace(abf_file_path, path_to_save_fig, trace_number=0, color='#7852A9', channel=1, smooth=0, x_override=None,
               show_legend=True, save_fig=True, display_fig=True):
    """
    Plots a single trace of an .abf file

    :param abf_file_path: path to single abf file
    :param path_to_save_fig: root path to save the figure
    :param trace_number: which sweep do you want to plot
    :param color: accepts hex or written color for plot trace. Default is purple
    :param channel: which channel is to be plotted? 0 or 1
    :param smooth: Do you want to smooth the plot? 0 No, 1 Yes, 2 Yes and display smoothed and un-smoothed data].
    :param x_override: Provide your own x_limits. Accepts a list [x_lower, x_upper]
    :param show_legend: Boolean
    :param save_fig: Boolean
    :param display_fig: Boolean
    :return:
    """
    protocol_times = {
        'LightStimProt': [0.75, 12],
        'AstroVoltClamp': [0.02, 0.14],
        'LightStimVoltClamp': [0.5, 2.7],
    }
    abf = pyabf.ABF(abf_file_path)
    try:
        abf.setSweep(trace_number, channel=channel)
    except ValueError:
        print(f'Sweep value not valid. Sweep ranges equals {abf.sweepCount}')
        print('Displaying default Sweep 0')

    fig = plt.figure(figsize=(9, 6))
    plt.style.use('ggplot')

    if smooth == 0:
        plt.plot(abf.sweepX, abf.sweepY, color=color, label=f'Sweep {trace_number}')
    elif smooth == 1:
        plt.plot(abf.sweepX, savgol_filter(abf.sweepY, 300, 3), color='black')  # window size 300, polynomial order 3)
    elif smooth == 2:
        plt.plot(abf.sweepX, abf.sweepY, color=color, label=f'Sweep {trace_number}')
        plt.plot(abf.sweepX, savgol_filter(abf.sweepY, 300, 3), color='black')   # window size 300, polynomial order 3)

    if x_override is None:
        try:
            plt.xlim(protocol_times[abf.protocol][0],
                     protocol_times[abf.protocol][1])
        except KeyError:
            plt.xlim(0, 9)
    else:
        try:
            plt.xlim(x_override[0], x_override[1])
        except Exception as e:
            print(e)
            plt.xlim(0, 9)

    y_units = abf.sweepUnitsY
    if y_units == 'mV':
        plt.ylabel('Voltage (mV)', fontsize=15)
    elif y_units == 'pA':
        plt.ylabel('Current (pA)', fontsize=15)
    else:
        print(y_units)

    plt.xlabel(f'Time ({abf.sweepUnitsX})', fontsize=15)
    plt.title(f'{abf.protocol}\n{Path(abf_file_path).stem}', fontsize=17)
    if show_legend:
        plt.legend()
    if save_fig:
        plt.savefig(os.path.join(path_to_save_fig, pathlib.Path(abf_file_path).stem + f'_trace{trace_number}.png'))
    if display_fig:
        plt.show()
    try:
        plt.close()
    except Exception as e:
        print(e)


def show_traces(abf_file_path, path_to_save_fig, channel=1, smooth=0, x_override=None, show_legend=True,
                save_fig=True, display_fig=True,):
    """
    Plots All traces of an .abf file

    :param abf_file_path: path to single abf file
    :param path_to_save_fig: Root path to save the figure
    :param channel: which channel is to be plotted? 0 or 1
    :param smooth: Do you want to smooth the plot? 0 No, 1 Yes, 2 Yes and display smoothed and un-smoothed data].
    :param x_override: Provide your own x_limits. Accepts a list [x_lower, x_upper]
    :param show_legend: Boolean
    :param save_fig: Boolean
    :param display_fig: Boolean
    :return:
    """
    protocol_times = {
        'LightStimProt': [0.75, 12],
        'AstroVoltClamp': [0.02, 0.14],
        'LightStimVoltClamp': [0.5, 2.7],
    }
    abf = pyabf.ABF(abf_file_path)
    colors = plt.cm.Spectral(np.linspace(0.4, 1, abf.sweepCount))

    # plot traces
    fig = plt.figure(figsize=(9, 6))
    plt.style.use('ggplot')

    for sweep in range(0, abf.sweepCount):
        try:
            abf.setSweep(sweep, channel=channel)
        except ValueError:
            print(f'Sweep value not valid. Sweep ranges equals {abf.sweepCount}')
            print('Displaying default Sweep 0')

        if smooth == 0:
            plt.plot(abf.sweepX, abf.sweepY, color=colors[sweep], label=f'Sweep {sweep}')
        elif smooth == 1:
            plt.plot(abf.sweepX, savgol_filter(abf.sweepY, 300, 3), color=colors[sweep], linewidth=3,
                     label=f'Sweep {sweep}')  # window size 300, polynomial order 3)
        elif smooth == 2:
            plt.plot(abf.sweepX, abf.sweepY, color=colors[sweep], alpha=0.2)
            plt.plot(abf.sweepX, savgol_filter(abf.sweepY, 300, 3), color=colors[sweep], linewidth=3,
                     label=f'Sweep {sweep}')  # window size 300, polynomial order 3)

    if x_override is None:
        try:
            plt.xlim(protocol_times[abf.protocol][0],
                     protocol_times[abf.protocol][1])
        except KeyError:
            plt.xlim(0, 9)
    else:
        try:
            plt.xlim(x_override[0], x_override[1])
        except Exception as e:
            print(e)
            plt.xlim(0, 9)

    y_units = abf.sweepUnitsY
    if y_units == 'mV':
        plt.ylabel('Voltage (mV)', fontsize=15)
    elif y_units == 'pA':
        plt.ylabel('Current (pA)', fontsize=15)
    else:
        print(y_units)

    plt.xlabel(f'Time ({abf.sweepUnitsX})', fontsize=15)
    plt.title(f'{abf.protocol}\n{Path(abf_file_path).stem}', fontsize=17)
    if show_legend:
        plt.legend()

    if save_fig:
        plt.savefig(os.path.join(path_to_save_fig, pathlib.Path(abf_file_path).stem + '_all_traces.png'))
    if display_fig:
        plt.show()
    try:
        plt.close()
    except Exception as e:
        print(e)


def iv_curve(excel_save_path, png_save_path, abf_path, mean_or_abs_max='mean', save_fig=True, plot_linear=False,
             save_data=True, print_data=False, display_fig=True):
    """
    Plots current voltage diagram for a single abf file

    :param excel_save_path: Path to directory you want to save IV plot Excel data
    :param png_save_path: Path to directory you want to save IV plot images
    :param abf_path: Path to single abf file
    :param mean_or_abs_max: Do you want the IV curve to use the mean current in the stimulation range
            or the absolute value max? 'mean' or 'max'
    :param save_fig: Boolean
    :param plot_linear: Boolean value if you want to plot a linear line on the plot for rectification reference
    :param save_data: Boolean to save Excel data points
    :param print_data: Boolean to display the Excel data points in console
    :param display_fig: Boolean
    :return:
    """

    abf = pyabf.ABF(abf_path)
    colors = plt.cm.Spectral(np.linspace(0.4, 1, abf.sweepCount))
    voltages = [-95 + 10 * i for i in range(14)]
    currents = []
    max_currents = []

    # Get current values for each sweep
    for sweep in range(abf.sweepCount):
        try:
            abf.setSweep(sweep, channel=1)
        except ValueError:
            abf.setSweep(sweep, channel=0)

        mid_voltage = abf.sweepY[round(50000 * .08)]
        mean_voltage = stats.mean(abf.sweepY[(round(50000 * .06)):round(50000 * .10)])
        min_voltage = min(abf.sweepY[(round(50000 * .06)):round(50000 * .10)])
        max_voltage = max(abf.sweepY[(round(50000 * .06)):round(50000 * .10)])

        if abs(min_voltage) > abs(max_voltage):
            max_abs = min_voltage
        else:
            max_abs = max_voltage

        currents.append(mean_voltage)
        max_currents.append(max_abs)

    # Plot IV curve
    fig = plt.figure(figsize=(9, 6))
    plt.style.use('ggplot')
    if mean_or_abs_max == 'mean':
        plt.scatter(voltages, currents, color='#7852A9')
        plt.plot(voltages, currents, color='#7852A9', label='IV Plot')
    elif mean_or_abs_max == 'max':
        plt.scatter(voltages, max_currents, color='#7852A9')
        plt.plot(voltages, max_currents, color='#7852A9', label='IV Plot')
    else:
        print('Incorrect Spelling of "mean" or "max"')
        raise ValueError

    if plot_linear:
        plt.plot(voltages, voltages, color='#eb9605', label='Linear')

    # Show Zero lines
    plt.axvline(0, color='black', linestyle="--")
    plt.axhline(0, color='black', linestyle="--")

    # Format Plot
    plt.title(f"Current Voltage Diagram\n{Path(abf_path).stem}", fontsize=17)
    plt.ylabel('Current (pA)', fontsize=15)
    plt.xlabel('Voltage (mV)', fontsize=15)
    if save_fig:
        plt.savefig(os.path.join(png_save_path, f'{abf.abfID} _ {abf.protocol}.png'))

    if display_fig:
        plt.show()

    try:
        plt.close()
    except Exception as e:
        print(e)

    if save_data:
        data = pd.DataFrame(pd.Series(voltages))
        data = pd.concat([data, pd.Series(currents)], axis=1)
        data.columns = ['Voltage', 'Current']
        data.to_excel(os.path.join(excel_save_path, f"{abf.abfID}.xlsx"))
        if print_data:
            print(data.head)


def patch_log(abf_directory_path, excel_save_path):
    """
    :param abf_directory_path: Path to the directory containing .abf files
    :param excel_save_path: path to Excel directory to save the file
    :return:
    """
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
    df.to_excel(os.path.join(excel_save_path, f'Patch Log_Ran_On_{today_str_date}.xlsx'))