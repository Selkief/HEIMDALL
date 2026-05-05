import scipy.io as sio
from scipy import signal
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import datetime as dt
import numpy as np


UHF = sio.loadmat("EISCAT/beata_20260202.mat")
VHF = sio.loadmat("EISCAT/bella_20260202.mat")

print(UHF.keys())
print(UHF["ne"].shape)
print("--------------")
print(VHF.keys())
print(VHF["ne"].shape)

#plot VHF and UHF electron densities
#plot VHF vs distance as well
time_uhf = []
for ele in UHF["t"][0]:
    ele = dt.datetime.fromtimestamp(ele, tz=dt.timezone.utc)
    time_uhf.append(ele)
time_vhf = []
for ele in VHF["t"][0]:
    ele = dt.datetime.fromtimestamp(ele, tz=dt.timezone.utc)
    time_vhf.append(ele)

#convert height into distance to radar
theta = np.deg2rad(30.0)
def calc_d(height, angle):
    return height * np.cos(angle)/np.sin(angle)

d_vhf = calc_d(VHF["h"], theta)

#are both arrays correlated?
#remove nan values before correlating (else get empty list)
uhf = np.nan_to_num(UHF["ne"])
vhf = np.nan_to_num(VHF["ne"])
corr = signal.correlate2d(uhf, vhf, mode="same")

#find strongest corr lag
#filter to get rid of noise spikes and find max (or find all values above some threshold!!)
corr = signal.medfilt2d(corr, 3)
max_corr = np.argmax(corr)
#I only care about time correlation, but argmax gives me index that counts all rows as well?
lag = max_corr % uhf.shape[1]

#find time resolution of uhf plot
delta_t = (time_uhf[1]-time_uhf[0])
lag_time = delta_t * lag
print("2d correlate", delta_t, lag, lag_time)

plt.figure(figsize=(12,6))
plt.imshow(corr)
plt.title("2d correlation between radar signals, median filtered(3x3)")
plt.show()

#correlate in 1d at height 300km to compare
corr_1d = signal.correlate(uhf[14,:], vhf[14,:], "same")
max_corr_1d = np.argmax(corr_1d)
lag_1d = max_corr_1d*delta_t

print("lag 1d correlate", lag_1d)

plt.plot(corr_1d)
plt.show()

#plot uhf and vhf electron densities
fig = plt.figure(figsize=(12, 6), constrained_layout=True)

ax = fig.add_subplot(211)
uhf = plt.pcolormesh(time_uhf, UHF["h"], UHF["ne"], norm=mcolors.LogNorm(vmin = 1e10, vmax= 1e12), cmap="jet")
plt.colorbar(uhf, ax=ax)
plt.xlabel("time UT")
plt.ylabel("altitude (km)")
plt.title("UHF radar (beata)")

ax = fig.add_subplot(212)
vhf = ax.pcolormesh(time_vhf, VHF["h"], VHF["ne"], norm=mcolors.LogNorm(vmin = 1e10, vmax= 1e12), cmap="jet")
fig.colorbar(vhf, ax=ax)
ax.set_xlabel("time UT")
ax.set_ylabel("altitude (km)")
ax2 = ax.twinx()
ax2.set_ylabel("distance N (km)")
ax2.set_ylim(d_vhf[0], d_vhf[-1])
ax.set_title("VHF radar (bella)")
plt.show()