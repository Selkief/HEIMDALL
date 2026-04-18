#calculate and plot the trajectories of Swarm satellites on a map,
# calculate the radar beam and add it to map, find intersection

import numpy as np
import matplotlib.pyplot as plt
import cdflib
import cartopy.crs as ccrs


dataA = cdflib.CDF("Swarm/Swarm_Alpha.cdf")
dataB = cdflib.CDF("Swarm/Swarm_Bravo.cdf")
dataC = cdflib.CDF("Swarm/Swarm_Charlie.cdf")
#file variables
variables = dataA.cdf_info()
print(f"\nVariables in the file: {variables}")
#convert time to sth readable
time = cdflib.cdfepoch.to_datetime(dataA["Timestamp"])

#TOS = UTC+1, start exp = 18 UTC end = 23 UTC
#  Swarm A and C pass around 21.37 UTC

#radar beam
r = 1344000 #[m] max length of VHF beam (los)
angle = 30 * np.pi/180
d = r * np.cos(angle) #radar beam length in m (distance from Ramfjordmoen)
h = r*np.tan(angle) #radar beam height in m
radar_end = 69.58625 + d/111111 #position on map
radar_beam = [[19.22978, 19.22978], [69.58625,radar_end]]


#find where Swarm intersects the radarbeam
#prints a list of all times where the satellite is within 0.04 degrees of the location
#and returns list of indices
def intersection(position_data, location):
    list = []
    for idx, ele in enumerate(position_data):
        if ele >= location - 0.04:
            if ele <= location + 0.04:
                list.append(idx)
    for i in list:
        print(time[i])
    return list

Ramfj = 19.22978
intersecA = intersection(dataA["longitude"], Ramfj)
print(".....")
intersecB = intersection(dataB["longitude"], Ramfj)
print(".....")
intersecC = intersection(dataC["longitude"], Ramfj)
#coordinates of interest:
A_coord = (dataA["longitude"][intersecA[1]], dataA["latitude"][intersecA[1]])
C_coord = (dataC["longitude"][intersecC[1]], dataC["latitude"][intersecC[1]])


#defines background map
ax = plt.axes(projection=ccrs.PlateCarree())
ax.coastlines()
ax.set_extent([17, 23, 69, 78], crs = ccrs.PlateCarree())
ax.gridlines()
#plots trajectories, radar beam, point of intersection
plt.scatter(dataA["longitude"], dataA["latitude"], s=1, label="Alpha")
plt.scatter(A_coord[0], A_coord[1], s=20, color="black")
plt.scatter(dataC["longitude"], dataC["latitude"], s=1, label="Charlie")
plt.plot(radar_beam[0], radar_beam[1], color="red", label="VHF radar")
plt.annotate("21:36", xy = A_coord, xytext=(3, 0), textcoords="offset points")
#plot Ramfjordmoen for reference
ax.plot(19.22978, 69.58625, 'bo', markersize=7, transform=ccrs.Geodetic())
ax.text(19, 69, 'Ramfjordmoen', transform=ccrs.Geodetic())

plt.legend(loc="upper left")
plt.tight_layout()
plt.show()

