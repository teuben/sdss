#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parameter drive Continuum subtraction in a fits cube

  Created on Mon Sep 13 16:34:32 2021
  @author: Eliz

"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import astropy 
from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.io import fits
from astropy.io import ascii
from astropy.wcs import WCS

#path = '/Users/Eliz/Documents/UMD/GBO_workshop/'
# file = 'Skynet_59471_Cold_dark_cloud_mapping_62107_10934.cyb.fits'
#file = 'dark_cloud_obs_2_gal_1420_MHz_line.fits'
#ofile = 'dark_cloud_2_gal_baseline_rmv.fits'
ifile = sys.argv[1]
ofile = sys.argv[2]

hdu = fits.open(ifile)[0]
head = hdu.header
data = hdu.data

data = data[0, :, :, :]

# header['OBSERVER'] = 'sdss_grp1'

# h = fits.PrimaryHDU(data, header = header)
# savefile = 'dark_cloud_fits_fix.cyb.fits'
# hdu.writeto(path + savefile, overwrite = True)

plt.figure(1)
plt.clf()
plt.imshow(data[180,:,:], origin = 'lower')

freq = np.arange(head['CRVAL3'], head['CRVAL3'] + head['CDELT3']*head['NAXIS3'], head['CDELT3'])
print(head['CRVAL3'])

x = 140
y = 58

plt.figure(2)
plt.clf()
# plt.plot(wave_array, data[:,y,x])
plt.plot(data[:,y,x])
# plt.xlabel('Frequency (um)')
# plt.ylabel('Flux (Jy/pixel)')


i1 = 170
i2 = 270

beg = 100
end = 300

ind = np.zeros(len(freq), dtype = bool)
ind[i1:i2] = True
ind[0:beg] = True
ind[end:] = True
ind = ~ind

cube = np.zeros_like(data)

# remove a first order polynomial
for x in range(np.shape(data)[2]):
    for y in range(np.shape(data)[1]):
        if np.isnan(data[:,y,x]).all():
            cube[:,y,x] =  data[:,y,x]
        else:
            loop_wave = freq[ind]
            loop_data = data[ind, y, x]
            nan = np.isnan(loop_data)
            fit = np.polyfit(loop_wave[~nan], loop_data[~nan], 3)
            p = np.poly1d(fit)
            cube[:,y,x] = data[:,y,x] - p(freq)
            


x1 = 140
y1 = 54
plt.figure(5)
plt.clf()
plt.plot(data[:,y1,x1], label = 'orig')
plt.plot(cube[:,y1,x1], label = 'Baseline removed')
plt.xlabel('Freq')
plt.ylabel('Flux (Jy/pixel)')
plt.legend(loc = 'best')

sub_cube = cube[beg:end,:,:]

head['NAXIS3'] = end - beg
head['CRVAL3'] = freq[beg]

del head['CTYPE4']
del head['CRVAL4']
del head['NAXIS4']
del head['CRPIX4']
del head['CDELT4']

linemap = np.nansum(cube[i1:i2, :, :], axis = 0)

plt.figure(6)
plt.clf()
plt.imshow(linemap, origin = 'lower')


h = fits.PrimaryHDU(sub_cube, header = head)

h.writeto(ofile, overwrite = True)

mom0 = np.nansum(cube[i1:i2, :, :], axis = 0)
