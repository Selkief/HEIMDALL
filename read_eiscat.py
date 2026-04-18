import scipy.io as sio
import matplotlib.pyplot as plt

UHF = sio.loadmat("EISCAT/beata_20260202.mat")
VHF = sio.loadmat("EISCAT/bella_20260202.mat")

print(UHF.keys())
print(UHF["Te"].shape)
print("--------------")
print(VHF.keys())

#plot VHF and UHF electron densities
#plot VHF vs distance as well, and maybe create map/ animation?
#logarithmic colorbar?
xcoord = UHF["t"]
ycoord = UHF["h"]
plt.pcolormesh(xcoord, ycoord, UHF["ne"], vmin=1e8, vmax=1e12)
plt.show()