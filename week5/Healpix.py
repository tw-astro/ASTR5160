#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tony Weinbeck
Astro 5160
Class 9: HEALPix
"""

import numpy as np
from numpy.random import random as rand
import healpy as hp
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

pi = np.pi



def create_points( num_points, Nside ):
# Creates a bunch of RA/Dec points, and determines which pixel of a HEALPix
# hierarchy they belong to

    # Generate an equal number of random RA's and Decs
    ras  = 360. * rand( num_points )
    decs = 180./pi * np.arcsin( 1.-rand( num_points )*2. )    
    
    # Place points into a HEALPix projection
    pix = hp.ang2pix( Nside, ras, decs, lonlat=True )
    
    # Determine how many points are in each HEALPix pixel
    Nbins   = hp.nside2npix( Nside )
    pixarea = hp.nside2pixarea( Nside )    
    counts  = np.array( np.unique( pix, return_counts=True ) )
    fracts  = counts[1] / num_points

    # Print results
    print()
    print( '{:8d}: num_points'.format(num_points) )
    print( '{:8d}: Nside'.format(Nside) )
    print( '{:8.6f}: pix_area (rads^2)'.format(pixarea) )
    print()
    for i in range( Nbins ):
        print( "Bin: {:4d}    Counts: {:8d}".format( i, counts[1,i] ) ) 

    # Calculate counts per pixel as fractions of total counts
    expected_fract  = 1. / hp.nside2npix( Nside )
    expected_count  = num_points * expected_fract    
    std_counts = np.std( counts[1] )
    std_fract  = np.std( fracts )
    # This was kinda a tangent I went on, specifically seeing how the STD of the counts
    # per pixel scales as either the number of pixels or the number of points increases
    snr = expected_fract / std_fract
    

    print( '\n' )
    print( '{:8.2f}: Expected counts'.format(expected_count) )
    print( '{:8.2f}: Std dev counts'.format(std_counts) )
    print()
    print( '{:8.6f}: Expected fraction'.format(expected_fract) )
    print( '{:8.6f}: Std dev fract'.format(std_fract) )
    print()
    print( '{:8.4f}: SNR (kinda)'.format(snr) )
    
    return pix, ras, decs




def plot_points( ras, decs, color, ax, label='' ):
    # Print given points onto a map
    ax.scatter( ras-pi, decs, marker='o', color=color, s=.5, alpha=0.01, label=label )
    return



def plot_specific_pixel( ras, decs, pix, which_pixel, color, ax ):
    # Plot only points within a specific HEALPix pixel    
    mask = (pix == which_pixel)
    plot_points( ras[mask]*pi/180, decs[mask]*pi/180, color, ax, label='Pixel ' +str(which_pixel) )
    return
    

    
def pixels_inside( pix_to_match, N_lower, N_higher ):
    # Determine which HEALPix pixels of higher-resolution projection lie within
    #   a given lower-resolution HEALPix pixel
    num  = 100 * hp.nside2npix( N_higher )  # This simply must be high enough 
    #   so that the points are surjective to the HEALPix pixels at given resolution
    ras  = 360. * rand( num )
    decs = 180./pi * np.arcsin( 1.-rand( num )*2. )    

    pix1 = hp.ang2pix( N_lower,  ras, decs, lonlat=True )
    pix2 = hp.ang2pix( N_higher, ras, decs, lonlat=True )
    
    mask =  ( pix1 == pix_to_match )
    pixels_inside = np.unique( pix2[mask] )
    print( '\nHEALPix pixels at Nside=' +str(N_higher) +' contained within pixel ' \
           +str(pix_to_match) +' at Nside=' +str(N_lower) +': \n' \
           +str(pixels_inside) )     
    return



if __name__ == "__main__":

    # Parts 1-3)
    # Create a bunch of points, distribute into a given HEALPix projection,
    #   and show/quantify distribution of points across all pixels
    num_points = 1000000
    Nside = 1
    ( pix, ras, decs ) = create_points( num_points, Nside )
    # This clearly shows that the pixels are roughly equal areas
    # To show more concretely, one would repeat this process a whole bunch of
    #   times, then find the average # of pix in each bin across all trials,
    #   which should be extremely close to the same number for each


    # Part 4)
    # Plot data points using an Aitoff projection
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="aitoff")
    xlab = ['14h','16h','18h','20h','22h','0h','2h','4h','6h','8h','10h']
    ax.set_xticklabels( xlab, weight=60, color='k' )
    ax.grid( color='k', linestyle='dashed', linewidth=.5 )
    
    # Plot all points in gray, and then specific pixels in various colors
    plot_points( ras, decs, 'gray', ax )
    plot_specific_pixel( ras, decs, pix, 2, 'b', ax )
    plot_specific_pixel( ras, decs, pix, 5, 'g', ax )
    plot_specific_pixel( ras, decs, pix, 8, 'r', ax )

    # Set up legend
    lh = ax.get_legend_handles_labels()    
    for label in lh[0]:    
        label.set_alpha(1)
    fig.legend( markerscale=5 )
    fig.show()
    
    
    
    # Part 5)
    # Determine which HEALPix pixels at Nside=2 are contained within
    #   pixel 5 of Nside=1 projection
    pix_to_match = 5
    pixels_inside( pix_to_match, N_lower=1, N_higher=2 )
    
    
    '''
    At this point I got curious about how quickly the actual distribution across 
    HEALPix pixels approaches a uniform distribution, as both num_points and Nbins increases.
    Since this is superfluous I didn't code everything out, but I'm skecthing out
    the process I'd use to quantify it below. Sometime when I get bored I'm gonna 
    come back to this cause I think it's a rather interesting quesiton.    

    Rough outline:
        for Nside in range(1,10):
            create_points( num_points=(some constant #), Nside )
              -find std dev of the counts per bin at each Nside, relative to the
               expected number per bin (or what I'm calling SNR in the code)

        for num_points in [10, 10^2, 10^3, 10^4, 10^5, 10^6, 10^7]:
            create_points( num_points, Nside=(some constant #) )
              -find 'SNR' for each run as above, as function of num_points
            
        Then in a lin-log plot, determine the slope of SNR vs Nbins, and similarly
            slope of SNR vs num_points --- essentially what is the functional form
            of the dependence of SNR on these variables
            
        Prediction: SNR increases as sqrt(num_points), and drops as 1/sqrt(Nbins)

    '''
