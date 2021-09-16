#! /usr/bin/env python
#
#   GBO 20m spectra plotting - September 2021 during Single Dish Workshop
#
#   Command line options (hardcoded)
#          plotsp1.py spectrum_file [order] [baseline_section(s)]
#
#   Plotting only the XX, since the YY has calibration issues due to a bad channel
#   This scripts assume OH in the first band, and HI in the 2nd
#   There are some horrific options in the script to flip things around
#
#   Examples of use:
#
#   ./plotsp1.py group2/Skynet_59471_M31_group2_62068_10914.A.onoff.cal.txt 4 -770 -600 50 2200
#   ./plotsp1.py group2/Skynet_59472_ngc628_group2_62098_10938.A.onoff.cal.txt  8 1600 3000  100 500 800 1500
#   ./plotsp1.py group2/Skynet_59472_ngc1530_group2_62102_10937.A.onoff.cal.txt 8 2000 2250 2650 3400 3600 5000
#   ./plotsp1.py group2/Skynet_59472_ngc3976_group2_62119_10949.A.onoff.cal.txt 8
#
#   Some archival M31 data with better noise:
#
#   ./plotsp1.py archive/Skynet_58945_M31_10kpc_radius_44912_54515.A.onoff.cal.txt 8 -2100 -800 100 1000
#   ./plotsp1.py archive/Skynet_58945_M31_center_44909_54513.A.onoff.cal.txt 8 -2100 -600 100 1000

import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

if len(sys.argv) == 1:
    print("Usage:  %s [polynomial_order] [baseline_section(s) in km/s]"  % sys.argv[0])
    print("e.g.    %s 3 100 1000   1300  2000" % sys.argv[0])
    sys.exit(0)

tab = sys.argv[1]

if len(sys.argv) > 2:
    p_order = int(sys.argv[2])
else:
    p_order = None

if len(sys.argv) > 3:
    baselines = sys.argv[3:]
    nbl = len(baselines)
    if nbl%2 != 0:
        print("Need even number of baseline sections")
        sys.exit(0)
    bl = []
    nbl = nbl // 2
    for i in range(nbl):
        vmin = float(baselines[2*i])
        vmax = float(baselines[2*i+1])
        bl.append((vmin,vmax))
    print("BASELINE sections: ",bl)
else:
    bl = []
    nbl = 0


keywords = {}    

def get_key(key, tab=None, verbose=False):
    """  get a keyword from the tabular spectrum.
         This needs to be initialized the first call by setting tab=
    """
    if len(keywords) == 0:
        if tab == None:
            print("Cannot setup keys without given the tab= name")
            sys.exit(0)
        lines = open(tab).readlines()
        for line in lines:
            if line[0] == '#':
                words = line[1:].split('=')
                if len(words)>1:
                    keywords[words[0].strip()] = words[1].strip()
        if verbose:
            print(keywords)
    if key in keywords:
        return keywords[key]
    return None

def fit_poly(x, y, p_order=1, bl = []):
    """ from array X between Xmin and Xmax fit a polynomial
    """

    if len(bl) == 0:
        p = np.poly1d(np.polyfit(x,y,p_order))
        t = x
        r = y - p(x)
    else:
        first = True
        for b in bl:
            print('B',b)
            if first:
                m = ((x>b[0]) & (x<b[1]))
                first = False
            else:
                m = m | ((x>b[0]) & (x<b[1]))
                
        p = np.poly1d(np.polyfit(x[m],y[m],p_order))
        t = x[m]
        r = y[m] - p(x[m])
    return (p,t,r)

def diff_rms(y):
    """ take the differences between neighboring signals
    and compute their rms. this should be sqrt(2)*sigma
    if there is no  trend in the input signal, and if
    the input signal is not correlated (e.g. hanning)
    """
    #y1 = y[1:]
    #y2 = y[:-1]
    return (y[1:]-y[:-1]).std() / 1.414

def my_smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

f1ref = 1665.4018        # OH line
f1ref = 1667.3590        # OH line
f2ref = 1420.405751786   # HI line
c = 299792.458

normalize = False
band_1 = False
band_2 = True
do_yy = False
do_smooth = 0
# do_smooth = 5

(f1,xx1,yy1,f2,xx2,yy2) = np.loadtxt(tab).T
get_key("FILENAME",tab)

print("DATE_OBS:  ",get_key("DATE_OBS"))
print("OBSERVER:  ",get_key("OBSERVER"))

# is this now topocentric?
v1 = (1-f1/f1ref)*c
v2 = (1-f2/f2ref)*c

if do_yy:
    xx1 = yy1
    xx2 = yy2

if do_smooth > 0:
    xx1 = my_smooth(xx1,do_smooth)
    xx2 = my_smooth(xx2,do_smooth)

if p_order != None:
    if band_1:
        (p1,t1,r1) = fit_poly(v1,xx1,p_order,bl)
    if band_2:
        (p2,t2,r2) = fit_poly(v2,xx2,p_order,bl)


plt.figure()
if normalize:
    xx1 = (xx1-xx1.min())/(xx1.max()-xx1.min())
    xx2 = (xx2-xx2.min())/(xx2.max()-xx2.min())
    yy1 = (yy1-yy1.min())/(yy1.max()-yy1.min())
    yy2 = (yy2-yy2.min())/(yy2.max()-yy2.min())
    if band_1:
        plt.plot(v1,xx1, label='XX %g ?' % f1ref)
        plt.plot(v1,yy1, label='YY %g ?' % f1ref)
    if band_2:
        plt.plot(v2,xx2, label='XX %g' % f2ref)
        plt.plot(v2,yy2, label='YY %g' % f2ref)
    plt.ylabel('Normalized Power')
else:
    if band_1:
        plt.plot(v1,xx1, label='%g ?' % f1ref)
    if band_2:
        plt.plot(v2,xx2, label='%g  %ss' % (f2ref, get_key("EXPOSURE")))
        if p_order != None:
            rms2 = r2.std()
            rms3 = diff_rms(r2)
            #plt.plot(t2, p2(t2), '-', label='POLY %d' % p_order)
            plt.plot(v2, p2(v2), '-', label='POLY %d SMTH %d' % (p_order,do_smooth))
            plt.plot(t2, r2, '-', label='RMS %.3g %.3g' % (rms2, rms3))
            plt.plot([v2[0],v2[-1]], [0.0, 0.0], c='black', linewidth=2, label='baseline')
    plt.ylabel('Power [Kelvin]')
plt.xlabel('Doppler Velocity [km/s]')
plt.title(tab)
plt.legend()
plt.savefig('plotsp1.png')
plt.show()
