import pyabf
import matplotlib.pyplot as plt
import numpy as np
import statistics as stats
from pathlib import Path
import pandas as pd

excel_save_path = ""
n = 4
abf_path = f"abf_dir/2353100{n}.abf"
abf = pyabf.ABF(abf_path)
colors = plt.cm.Spectral(np.linspace(0, 1, abf.sweepCount))
voltages = [-95 + 10 * i for i in range(14)]
currents = []

for sweep in range(abf.sweepCount):
    abf.setSweep(sweep, channel=0)
    plt.plot(abf.sweepX, abf.sweepY, color=colors[sweep])
    plt.xlim(0.02, 0.14)
    plt.ylim(-200, 200)
    mid_voltage = abf.sweepY[round(50000 * .08)]
    mean_voltage = stats.mean(abf.sweepY[(round(50000*.06)):round(50000*.10)])
    currents.append(mean_voltage)
# plt.show()
#
plt.close()
plt.style.use('ggplot')
plt.scatter(voltages, currents, color='purple')
plt.plot(voltages, currents, color='purple', label='IV Plot')
plt.plot(voltages, voltages, color='green', label='Linear')
plt.axvline(0, color='black', linestyle="--")
plt.axhline(0, color='black', linestyle="--")
plt.title(f"Current Voltage Diagram: {Path(abf_path).stem}", fontsize=17)
plt.ylabel('Current (pA)')
plt.xlabel('Voltage (mV)')
plt.show()

data = pd.DataFrame(pd.Series(voltages))
data = pd.concat([data, pd.Series(currents)], axis=1)
data.columns = ['Voltage', 'Current']
data.to_excel(excel_save_path)
print(data.head)
