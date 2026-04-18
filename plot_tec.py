# https://pysatmadrigal.readthedocs.io/en/main/examples/ex_gnss_tec.html
# https://cartopy.readthedocs.io/stable/index.html

###downloads TEC data from 02.02.2026 from Madrigal database and creates an polar-view animation over the whole day###
import datetime as dt
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pysat
import pysatMadrigal as pysat_mad
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.path as mpath
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#load TEC data into folder
pysat.params['data_dirs'] = "C:/Users/skief/Documents/UiT/semester8/HEIMDALL"
vtec = pysat.Instrument(inst_module=pysat_mad.instruments.gnss_tec, tag='vtec')
ftime = dt.datetime(2026, 2, 2)
ftime_stop = dt.datetime(2026, 2,4)
if not ftime in vtec.files.files.index:
    vtec.download(start=ftime,  stop = ftime_stop, user='Selma+Kiefersauer', password='ski045@uit.no')
vtec.load(date=ftime, end_date=ftime_stop)
print(vtec.variables)

#extend coordinates
coords = {}
for ckey in ['gdlat', 'glon']:
    coords[ckey] = list(vtec[ckey].values)
    coords[ckey].append(vtec.meta[ckey, vtec.meta.labels.max_val])
    coords[ckey] = np.array(coords[ckey])

#create polar view map as circle
data_crs = ccrs.PlateCarree()
fig = plt.figure()
ax = fig.add_subplot(111, projection=ccrs.NorthPolarStereo())
ax.coastlines()
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.OCEAN)
ax.gridlines()
ax.set_extent([-180,180, 40,90], crs = ccrs.PlateCarree())
theta = np.linspace(0, 2*np.pi, 100)
center, radius = [0.5, 0.5], 0.5
verts = np.vstack([np.sin(theta), np.cos(theta)]).T
circle = mpath.Path(verts * radius + center)
ax.set_boundary(circle, transform=ax.transAxes)

# plot TEC on polar view as colormesh
itime = 0 #[0,288] interval
vmin = vtec.meta['tec', vtec.meta.labels.min_val]
#vmax = np.ceil(vtec['tec'][0].max().values / 10.0) * 10.0
cmap = plt.colormaps["jet"]
con = ax.pcolormesh(coords['glon'], coords['gdlat'],vtec['tec'].values[itime], vmin=vmin, vmax=50, transform=data_crs, cmap = cmap)
#define labels, axis, title, ...
ax.set_facecolor('0.9')
ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(60))
ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator(30))
ax.set_xlabel('Geographic Longitude ($^\circ$)')
ax.set_ylabel('Geodedic Latitude ($^\circ$)')
cbar = plt.colorbar(mappable=con, ax=ax, location='right', fraction=.1, pad=.01,
             label='VTEC ({:s})'.format(vtec.meta['tec', vtec.meta.labels.units]))
title = plt.suptitle('{:s} {:s} at {:s}'.format(vtec.platform.upper(), vtec.tag.upper(),
    vtec.index[itime].strftime('%d %b %Y %H:%M:%S UT')), fontsize=14)

# animation update function
def update(frame):
    con.set_array(vtec['tec'].values[frame].flatten())  # update data
    title.set_text('{:s} {:s} at {:s}'.format(
        vtec.platform.upper(), vtec.tag.upper(),
        vtec.index[frame].strftime('%d %b %Y %H:%M:%S UT')))
    return con, title

# create animation (loops over 576 frames, 100ms interval) and save as gif
ani = animation.FuncAnimation(fig, update, frames=576, interval=100, blit=False)
ani.save('tec_animation2.mp4', writer='ffmpeg')
plt.tight_layout()
#plt.show()
