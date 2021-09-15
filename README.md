#  Single Dish (GBT/AO) Summer School

My codes and data from the 2021 workshop

There is also 
[my version of gbtgridder](https://github.com/teuben/gbtgridder)
in the python3 branch that you will need to grid the SDFITS file.

Something like

      gbtgridder/src/gbtgridder --clobber Skynet_59471_messier_31_62079_10919.cyb.fits
	  
should do the job.  Not tested yet!  This should be version 0.6 or later, and make sure you see 
the new --dish option!

Although this will produce a cube, line and cont map, the determination of the continuum isn't
always good and you may need to an additional baseline subtraction from either the cube or line.
