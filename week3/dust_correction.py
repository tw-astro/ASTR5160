Conversation opened. 2 messages. 1 message unread.

Skip to content
Using Gmail with screen readers
1 of 7,215
Fw: Program
Inbox

Tony Weinbeck
Attachments5:31 PM (2 hours ago)
From: Tony Weinbeck <aweinbec@uwyo.edu> Sent: Friday, February 7, 2025 5:31 PM To: Tony Weinbeck <aweinbec@uwyo.edu> Subject: Program

Tony Weinbeck <weinbeck@alum.mit.edu>
Attachments
7:54 PM (0 minutes ago)
to Tony


 One attachment
  •  Scanned by Gmail
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from astropy.coordinates import SkyCoord
from astropy import units as U
import dustmaps
from dustmaps.sfd import SFDQuery
from dustmaps.config import config
import numpy as np
import matplotlib.pyplot as plt
import os
import warnings
warnings.filterwarnings("ignore")



def setup_sfd():
    # Set up the SFD dust query
    home = os.getenv("HOME")
    dust_dir = os.path.join( home, 'Documents', 'Classes', 'Techniques_II', 'dust_maps' )
    config["data_dir"] = dust_dir
    sfd = SFDQuery()
    
    return sfd


def find_reddening( ra, dec ):    
    # Obtain reddening
    c = SkyCoord( ra*U.degree, dec*U.degree )
    sfd = setup_sfd() 
    ebv = sfd(c)

    return ebv


def find_extinction( ebv ):
    # Find extinction
    ugriz_dust = np.array( [4.239, 3.303, 2.285, 1.698, 1.263] )
    A = ebv * ugriz_dust

    return A


def make_color_color_plot( mag, label ):
    # Compute colors
    g_min_r = mag[1]-mag[2]
    r_min_i = mag[2]-mag[3] 
        
    # Plot g-r (x-axis) vs r-i (y-axis)
    plt.scatter( g_min_r, r_min_i, label=label )
    
    return plt


if __name__ == '__main__':

    # Part 1: Make color-color diagrams and correct for dust extinction
    
    # Magnitudes (ugriz) taken from SDSS Object Finder,
    # https://skyserver.sdss.org/dr12/en/tools/explore/
    mags = [ np.array( [ 18.82, 18.81, 18.73, 18.82, 18.90 ] ), \
             np.array( [ 19.37, 19.10, 18.79, 18.73, 18.63 ] ) ]
    
    ras = [ 246.933, 236.562 ]
    decs = [ 40.795, 2.440 ]
    sources = ['Source 1', 'Source 2']
    
    
    # Plot color-color diagram for both quasars
    for i in range(2):
        plt = make_color_color_plot( mags[i], sources[i] )
    plt.xlabel( 'g - r' )
    plt.ylabel( 'r - i' )
    plt.xlim(0,0.35)
    plt.ylim(-0.10,0.07)
    plt.legend( loc="lower right")
    plt.show()

    print( '\nBefore dust-correcting, there is some variation in the colors '\
           'of the quasars, though it is not extreme\n')


    # Calculate dust reddening for both sources
    mags_corr = []
    for i in range(2):
        ebv = find_reddening( ras[i], decs[i] )
        A = find_extinction( ebv )
        mags_corr.append( mags[i] - A )
        print( '\nSource ' +str(i+1) +':')
        print( '  mag: ' +str(mags[i]) )
        print( '  ebv value: ' +str(ebv) )
        print( '  A: ' +str(A) )
        print( '  mag_corr: ' +str(mags_corr[i]) )
        

    # Plot dust-corrected color-color diagram    
    for i in range(2):
        plt = make_color_color_plot( mags_corr[i], sources[i] )
    plt.xlabel( 'g - r, corrected' )
    plt.ylabel( 'r - i, corrected' )
    plt.xlim(0,0.35)
    plt.ylim(-0.10,0.07)
    plt.legend( loc="lower right")
    plt.show()
    
    print( '\nAfter correcting for the dust extinction, the colors are in '\
           'closer agreement, though still are not precisely the same\n')
    
        
    # Parts 2-4: Create map of dust in vicinity of each quasar
    for i in range(2):
        
        # Set grid size for meshgrid
        if i==0:  bins = [0.10, 0.10]
        else:     bins = [0.13, 0.10]
        
        # Create meshgrid centered at RA, Dec of given source    
        ra_range  = np.linspace( ras[i]  - bins[0]*50,  ras[i] + bins[0]*51, 101 )
        dec_range = np.linspace( decs[i] - bins[1]*50, decs[i] + bins[1]*51, 101 )
        (xgrid, ygrid) = np.meshgrid( ra_range, dec_range )
        
        # Calculate dust reddening for all points in meshgrid
        ebv = find_reddening( xgrid, ygrid )
        
        # Plot dust reddening around source, and denote source with white '+'
        plt.contourf( ra_range, dec_range, ebv)
        plt.xlabel( 'Right Ascension (deg)' )
        plt.ylabel( 'Declination (deg)' )
        plt.title( 'Dust reddening for ' +sources[i] )
        plt.colorbar()
        plt.plot( ras[i], decs[i], marker='+', c='w', markersize=10)
        plt.show()

dust_correction.py
Displaying dust_correction.py.
