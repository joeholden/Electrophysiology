import pyabf
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.signal import savgol_filter
import numpy as np

path = "C:/Users/Acer/Desktop/2023-07-26 great patch day/ABF/23726020.abf"


def show_trace(abf_file_path, trace_number=0, color='#7852A9', channel=1, smooth=0, x_override=None):
    """
    :param abf_file_path: path to single abf file
    :param trace_number: which sweep do you want to plot
    :param color: accepts hex or written color for plot trace. Default is purple
    :param channel: which channel is to be plotted? 0 or 1
    :param smooth: Do you want to smooth the plot? 0 No, 1 Yes, 2 Yes and display smoothed and un-smoothed data].
    :param x_override: Provide your own x_limits. Accepts a list [x_lower, x_upper]
    :return:
    """
    protocol_times = {
        'LightStimProt': [0.75, 12],
        'AstroVoltClamp': [0.02, 0.14],
        'LightStimVoltClamp': [0.5, 2.7],
    }
    abf = pyabf.ABF(path)
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

    if x_override == None:
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
    plt.legend()
    plt.show()


def show_traces(abf_file_path, channel=1, smooth=0, x_override=None):
    """
    :param abf_file_path: path to single abf file
    :param channel: which channel is to be plotted? 0 or 1
    :param smooth: Do you want to smooth the plot? 0 No, 1 Yes, 2 Yes and display smoothed and un-smoothed data].
    :param x_override: Provide your own x_limits. Accepts a list [x_lower, x_upper]
    :return:
    """
    protocol_times = {
        'LightStimProt': [0.75, 12],
        'AstroVoltClamp': [0.02, 0.14],
        'LightStimVoltClamp': [0.5, 2.7],
    }
    abf = pyabf.ABF(path)
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
    plt.legend()
    plt.show()


show_traces(path, smooth=2)
