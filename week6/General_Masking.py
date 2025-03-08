#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tony Weinbeck
Astro 5160
Class 12: General_Masking
"""

from astropy.coordinates import SkyCoord
from astropy import units as U
import numpy as np
import pymangle as pm
import matplotlib.pyplot as plt
import re  # To replace characters in a string
import warnings
warnings.filterwarnings('ignore')

pi = np.pi



def return_cap_vector( ra, dec, rad ):
    # Takes RA, Dec, and cap_radius as inputs, and outputs 4-vector associated with spherical cap
    #   Note: expects the RA and Dec to be the central point of the cap, NOT
    #   the RA bound for a great circle    
    coord = SkyCoord( ra, dec, frame='icrs' )
    coord.representation_type="cartesian"
    vector = np.array( [coord.x.value, coord.y.value, coord.z.value, (1-np.sin( (90*U.degree - rad)).value ) ] )
    return vector



def write_to_mangle_file( *vs, fname='', sters=0 ):
    # Prints polygons with specific formatting to a Mangle file
    #   Accepts a variable number of polygons, and a variable number of spherical
    #   caps within each polygon
    # If have a list of areas for each polygon, can include in arguments
    #   ( len(sters) must match len(vs) )

    # The number of ordered arguments (=num of polygons)
    n_polys = len(vs)

    with open(fname, "w") as f:
        i = 1  # To keep track of which polygon we're printing
        print( str(n_polys) +' polygons', file=f )
        for v in vs:
            n_caps = len(v)       # Number of caps for current polygon

            # If being fed the areas for each polygon, set appropriately
            if len(sters) != 0:
                ster = sters[i-1]  # b/c zero-ordering
            else: ster = 0

            # Print output to file
            print( 'polygon ' +str(i) +' ( ' +str(n_caps) +' caps, 1 weight, ' \
                  +'0 pixel, ' +str(ster) +' str):', file=f )
            np.set_printoptions(formatter={'float': '{:12.9f}'.format})
            print( ' ' +re.sub( r"[\[\]]", "", str(v)  ), file=f )
            # This is ugly but it just prints the formatted list without the brackets
            i += 1
    return



def calc_area( ra_min, ra_max, dec_min, dec_max ):
    # Calculate area of lat-long rectangle using formula derived in notes
    ster = pi/180 * (ra_max-ra_min) \
           * (np.sin( dec_max ) - np.sin( dec_min ) )
    return np.abs( ster )





if __name__ == '__main__':


    # Part 1)  Create lat-long rectangle
    sters = []  # Use this to keep track of area for each polygon
    ra_min  =  5 *U.hourangle
    ra_max  =  6 *U.hourangle
    dec_min = 30 *U.degree
    dec_max = 40 *U.degree

    # Create vector for each of four associated spherical caps
    v1 = return_cap_vector(  ra = ra_min +6*U.hourangle, dec=0 *U.degree, rad=90 *U.degree)
    v2 = return_cap_vector(  ra = ra_max +6*U.hourangle, dec=0 *U.degree, rad=90 *U.degree)
    v3 = return_cap_vector(  ra = 0*U.hourangle, dec=dec_min, rad=(90*U.degree - dec_min) )
    v4 = return_cap_vector(  ra = 0*U.hourangle, dec=dec_max, rad=(90*U.degree - dec_max) )

    # Calculate area of lat-long rectangle    
    ster  = calc_area( ra_min, ra_max, dec_min, dec_max )
    sters.append(ster)
    
    # Combine vectors into array in format needed to create Mangle file
    mask1 = np.array( [v1, v2, v3, v4] )



    # Part 2) Create another lat-long rectangle, write both to Mangle file
    ra_min  = 11 *U.hourangle
    ra_max  = 12 *U.hourangle
    dec_min = 60 *U.degree
    dec_max = 70 *U.degree

    # Create vector for each of four associated spherical caps
    w1 = return_cap_vector(  ra = ra_min +6*U.hourangle, dec=0 *U.degree, rad=90 *U.degree)
    w2 = return_cap_vector(  ra = ra_max +6*U.hourangle, dec=0 *U.degree, rad=90 *U.degree)
    w3 = return_cap_vector(  ra = 0*U.hourangle, dec=dec_min, rad=(90*U.degree - dec_min) )
    w4 = return_cap_vector(  ra = 0*U.hourangle, dec=dec_max, rad=(90*U.degree - dec_max) )

    # Calculate area of lat-long rectangle    
    ster  = calc_area( ra_min, ra_max, dec_min, dec_max )
    sters.append(ster)

    # Combine vectors into array in format needed to create Mangle file
    mask2 = np.array( [w1, w2, w3, w4])

    # Write both lat-long rectangles to Mangle file to produce two polygons    
    write_to_mangle_file( mask1, mask2, fname="lat_long_rect.ply", sters=sters )
