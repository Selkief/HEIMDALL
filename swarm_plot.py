import numpy as np
import matplotlib.pyplot as plt
import cdflib

dataA= cdflib.CDF("Swarm/Swarm_Alpha2.cdf")
dataC= cdflib.CDF("Swarm/Swarm_Charlie2.cdf")
variables = dataA.cdf_info()
print(f"\nVariables in the file: {variables}")
#convert time to sth readable
time = cdflib.cdfepoch.to_datetime(dataA["Timestamp"])

#print(dataC["vicrx"])
plt.plot(time, dataC["B_NEC"])
plt.show()

plt.plot(time, dataC["Ehx"])
plt.show()

