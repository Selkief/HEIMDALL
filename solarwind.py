import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#read files and rename header to sth more usable
MFI = pd.read_csv("AC_K0_MFI_4000249.csv", skiprows=56)
MFI = MFI.rename(columns={"EPOCH__yyyy-mm-ddThh:mm:ss.sssZ":"time", "[PRELIM]_<|B|>__nT": "B abs", "[PRELIM]_BX_GSE_(@_x_)_nT": "Bx", "[PRELIM]_BY_GSE_(@_y_)_nT":"By", "[PRELIM]_BZ_GSE_(@_z_)_nT":"Bz"}) 
SWE = pd.read_csv("AC_K0_SWE_4000249.csv", skiprows=58)
SWE = SWE.rename(columns={"EPOCH_yyyy-mm-ddThh:mm:ss.sssZ":"time", "[PRELIM]_SW_H_NUM_DENSITY_#/cc":"n", "[PRELIM]_SW_BULK_SPEED_km/s":"v"})

#convert the data into arrays of floats (was strings initially)
B_abs = np.array(MFI["B abs"][:-3]).astype(float)
Bx = np.array(MFI["Bx"][:-3]).astype(float)
By = np.array(MFI["By"][:-3]).astype(float)
Bz = np.array(MFI["Bz"][:-3]).astype(float)
n = np.array(SWE["n"][:-3]).astype(float)
v = np.array(SWE["v"][:-3]).astype(float)
avg_v = np.mean(v)
print("average solar wind speed", avg_v)

#convert time into usable format for plots
time = pd.to_datetime(MFI["time"][:-3])


fig, axs = plt.subplots(3,1)
axs[0].plot(time, B_abs, label = "|B|")
axs[0].plot(time, Bx, label = "Bx")
axs[0].plot(time, By, label = "By")
axs[0].plot(time, Bz, label = "Bz")
axs[0].legend()
axs[0].set_title("magnetic field components")
axs[0].set_ylabel("nT")
axs[1].plot(time, n)
axs[1].set_title("SW number density")
axs[1].set_ylabel("cm^-3")
axs[2].plot(time, v)
axs[2].set_title("SW bulk speed")
axs[2].set_ylabel("km/s")
for ax in axs.flat:
    ax.grid(True)
plt.suptitle("Solarwind data ACE")
plt.tight_layout()
plt.show()