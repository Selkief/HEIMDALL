import scipy.io as sio
from scipy import signal
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import datetime as dt
import numpy as np
import pandas as pd
import xarray as xr


UHF = sio.loadmat("EISCAT/beata_20260202.mat")
VHF = sio.loadmat("EISCAT/bella_20260202.mat")

print(UHF.keys())
print(UHF["ne"].shape)
print("--------------")
print(VHF.keys())
print(VHF["ne"].shape)
print("--------------")

t = UHF["t"].squeeze()
h = UHF["h"].squeeze()
ne = UHF["ne"]

# fix shapes
t = np.squeeze(t)
h = np.squeeze(h)

uhf = xr.DataArray(
    ne,
    dims=("height", "time"),
    coords={
        "time": t,
        "height": h
    }
)
t = VHF["t"].squeeze()
h = VHF["h"].squeeze()
ne = VHF["ne"]

# fix shapes
t = np.squeeze(t)
h = np.squeeze(h)

vhf = xr.DataArray(
    ne,
    dims=("height", "time"),
    coords={
        "time": t,
        "height": h
    }
)

uhf = uhf.assign_coords(time=pd.to_datetime(uhf.time, unit="s"))
vhf = vhf.assign_coords(time=pd.to_datetime(vhf.time, unit="s"))
uhf_30s = uhf.resample(time="30s").interpolate("linear")
vhf_30s = vhf.resample(time="30s").interpolate("linear")

#convert height into distance to radar
theta = np.deg2rad(30.0)
def calc_d(height, angle):
    return height * np.cos(angle)/np.sin(angle)

d_vhf = calc_d(vhf["height"], theta)
d_300 = calc_d(300, theta)
print(f"300km altitude corresponds to {d_300:.1f}km distance")
#find time resolution of radars
time_uhf = uhf_30s["time"]
time_vhf = vhf_30s["time"]
dt1 = np.diff(time_uhf)
dt2 = np.diff(time_vhf)
#print(np.mean(dt1)*1e-9, np.min(dt1)*1e-9, np.max(dt1)*1e-9)
#print(np.mean(dt2), np.min(dt2), np.max(dt2))

#are both arrays correlated?
#correlate at height 300km
uhf_h300 = uhf_30s.sel(height=300, method="nearest")
vhf_h300 = vhf_30s.sel(height=300, method="nearest")
#vhf_h300, uhf_h300 = xr.align(vhf_h300, uhf_h300, join="inner")
uhf_h300 = np.nan_to_num(uhf_h300.values)
vhf_h300 = np.nan_to_num(vhf_h300.values)


corr_1d = signal.correlate(uhf_h300, vhf_h300, "full")

max_corr_1d = np.argmax(corr_1d)
lag_1d = (max_corr_1d - len(corr_1d)//2) * np.mean(dt1)*1e-9/60
lags_1d = signal.correlation_lags(len(vhf_h300), len(uhf_h300))
print("lag 1d correlate", lag_1d, "mins")

n = len(corr_1d)
center = n // 2
lags = (np.arange(n) - center) * np.mean(dt1)*1e-9 /60


#corr = vhf_30s.correlate2d(uhf_h300, vhf_h300, mode="same")
idx = (np.where((VHF["h"]<310)&(VHF["h"]>290)))[0]
print("mean ion velocity at 300km",np.mean(VHF["vi"][idx].ravel()))

plt.figure(figsize=(12,6))
plt.plot(vhf.time, VHF["vi"][idx].ravel())
plt.title("ion velocities (m/s) at 300km")
plt.grid()
plt.show()

plt.scatter(lags_1d, corr_1d, s=1)
plt.title("1D correlation at 300km altitude")
plt.xlabel("lag")
plt.show()

#plot uhf and vhf electron densities
fig = plt.figure(figsize=(12, 6), constrained_layout=True)

ax = fig.add_subplot(211)
uhf_pl = plt.pcolormesh(uhf_30s.time, uhf_30s.height, uhf_30s.values, norm=mcolors.LogNorm(vmin = 1e10, vmax= 1e12), cmap="jet")
plt.colorbar(uhf_pl, ax=ax)
plt.xlabel("time UT")
plt.ylabel("altitude (km)")
plt.title("UHF radar (beata)")

ax = fig.add_subplot(212)
vhf_pl = plt.pcolormesh(vhf_30s.time, vhf_30s.height, vhf_30s.values, norm=mcolors.LogNorm(vmin = 1e10, vmax= 1e12), cmap="jet")
plt.colorbar(vhf_pl, ax=ax)
ax.set_xlabel("time UT")
ax.set_ylabel("altitude (km)")
ax2 = ax.twinx()
ax2.set_ylabel("distance N (km)")
ax2.set_ylim(d_vhf[0], d_vhf[-1])
ax.set_title("VHF radar (bella)")
plt.show()

