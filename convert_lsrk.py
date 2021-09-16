#! /usr/bin/env python
#
#   convert a fits cube spectral coordinate to LSRK
#   based pn scripts in https://docs.astropy.org/en/stable/coordinates/spectralcoord.html
#   written by Jane Huang (group1)
#

import sys
import numpy as np
from astropy.coordinates import EarthLocation
from astropy.io import fits
from astropy.time import Time
from astropy.coordinates import SkyCoord, SpectralCoord
import astropy.units as u
import astropy.constants as const

# @todo make this proper command line arguments
ifile = 'dark_cloud_baseline_rmv_new.fits'
ofile = 'dark_cloud_baseline_rmv_lsrk.fits'
ifile = sys.argv[1]
ofile = sys.argv[2]

hdulist = fits.open(ifile)


location = EarthLocation.of_site('gbt')
gbt = location.get_itrs(obstime=Time(hdulist[0].header['DATE-OBS']))
#  @todo  grab RA/DEC from input fits header
cloud = SkyCoord('18h35m08.0s -09d16m01.4', frame='icrs')
restfreq=1420405751.786 # 21 cm line in Hz
sc_cloud = SpectralCoord((hdulist[0].header['CRVAL3']+np.arange(0,hdulist[0].header['NAXIS3'])*hdulist[0].header['CDELT3']) * u.GHz,
                         observer=gbt,
                         target=cloud,
                         doppler_rest=restfreq*u.Hz,
                         doppler_convention='radio')
lsrkfreqs = np.array(sc_cloud.with_observer_stationary_relative_to('lsrk').quantity)
velocities = ((restfreq-lsrkfreqs)/restfreq*const.c).to(u.km/u.s)

hdulist[0].header['CRVAL3'] = lsrkfreqs[0]
hdulist[0].header['CDELT3'] = lsrkfreqs[1]-lsrkfreqs[0]
hdulist[0].header['SPECSYS'] ='lsrk'
newhdul = fits.HDUList(hdulist)
newhdul.writeto(ofile,overwrite=True)
