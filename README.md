#  Single Dish (GBT/AO) Summer School

My codes and data from the 2021 workshop

There is also 
[my version of gbtgridder](https://github.com/teuben/gbtgridder)
in the python3 branch that you will need to grid the SDFITS file.

Something like

      gbtgridder/src/gbtgridder --clobber Skynet_59471_messier_31_62079_10919.cyb.fits
	  
should do the job.  This should be version 0.6pjt or later, and make
sure you see the new --dish option!

Although this will produce a cube, line and cont map, the
determination of the continuum isn't always good and you may need to
an additional baseline subtraction from either the cube or line.

## Files in this repository

* archive/ - some sample archive data from M31
* cont_sub.py - manual continuum subtraction (from group1)
* convert_lsrk.py -  convert a topocentric cube to VLSR (from group1)
* GBO20m_SSDS_group2_Data.*  - spreadsheet with our data and derived quantaties
* group2/   - our data (M31, N628, N1530, N3976, N4565, N4559)
* plotsp1.py - analysis of noise with baseline subtraction, option to smooth and XX+YY average
* presentation.pdf - our 10 minute final presentation
