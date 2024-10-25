# -*- coding: utf-8 -*-

"""
Test of the batman package for the calculation of transit light curves
"""

# We import all the necessary libraries
import batman
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# We create a TransitParams object using the batman package.
# This object allows us to input the planetary and stellar
# parameters of our exoplanet in order to calculate
# the transit lightcurve
params = batman.TransitParams()

# We input the necessary parameters into our TransitParams object.
# We have chosen the WASP-50 b exoplanet.
# All the parameters are taken from https://exoplanet.eu/home/
params.t0 = 0.                     #time of inferior conjunction
params.per = 1.955                 #orbital period (in our case, the units are days)
params.rp = 0.1368                 #planet radius (in units of stellar radii)
params.a = 7.326                   #semi-major axis (in units of stellar radii)
params.inc = 84.74                 #orbital inclination (in degrees)
params.ecc = 0.009                 #eccentricity
params.w = 44.                     #longitude of periastron (in degrees)

# In order to get the Limb Darkening parameters,
# we go to https://exoctk.stsci.edu/limb_darkening
# There, we input the planet name and then download
# the coefficients table for the quadratic profile.
# We use pandas to open the file with the coefficients table.
# We use skipfooter=30 because we only need the rows that
# contain the information about the quadratic profile.
data = pd.read_csv("ExoCTK_results.txt", header=[0], delim_whitespace=True, skiprows=[1], skipfooter=30, engine='python')

# We define the coefficients u1 and u2 as the mean of
# coefficients c1 and c2, respectively, computed from the table.
u1, u2 = data["c1"].mean(), data["c2"].mean()

# We now define the limb darkening coefficients in our
# TransitParams object as the ones computed just above (u1 and u2)
params.u = [u1, u2]                #limb darkening coefficients [u1, u2]
params.limb_dark = "quadratic"     #limb darkening model

# We define the times at which we will calculate the light curve
t = np.linspace(-0.075, 0.075, 1000)

# We run our batman transit model
m = batman.TransitModel(params, t)    #initializes model
flux = m.light_curve(params)          #calculates light curve

# We finally plot the calculated light curve
plt.figure(figsize=(10,6.7))
plt.plot(t, flux, linewidth=3)
plt.title("Transit light curve of WASP-50 b", fontsize=25)
plt.xlabel("Time from central transit [days]", fontsize=20)
plt.ylabel("Relative flux", fontsize=20)
plt.show()