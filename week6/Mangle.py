#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tony Weinbeck
Astro 5160
Class 11: Mangle
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



def write_to_mangle_file( *vs, fname='' ):
    # Prints polygons with specific formatting to a Mangle file
    #   Accepts a variable number of polygons, and a variable number of spherical
    #   caps within each polygon

    # The number of arguments (=num of polygons)
    n_polys = len(vs)

    with open(fname, "w") as f:
        i = 1  # To keep track of which polygon we're printing
        print( str(n_polys) +' polygons', file=f )
        for v in vs:
            n_caps = len(v)       # Number of caps for current polygon

            # Print output to file
            print( 'polygon ' +str(i) +' ( ' +str(n_caps) +' caps, 1 weight, 0 pixel, 0 str):', file=f )
            np.set_printoptions(formatter={'float': '{:12.9f}'.format})
            print( ' ' +re.sub( r"[\[\]]", "", str(v)  ), file=f )
            # This is ugly but it just prints the formatted list without the brackets
            i += 1
    return



def plot_masks( *args ):
    # Print out a variable number of data sets in different colors
    #   Each argument must be of form [ ras, decs, label ]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid( color='k', linestyle='dashed', linewidth=.5 )

    # Plot each dataset using different color     
    colors = ['b', 'r', 'g', 'y']
    i = 0
    for arg in args:
        ras   = arg[0]
        decs  = arg[1]
        label = arg[2]
        color = colors[ i ]
        i += 1
        ax.scatter( ras, decs, marker='o', color=color, s=.5, alpha=0.01, label=label )
    ax.set_xlabel( 'RA (degs)') 
    ax.set_ylabel( 'Dec (degs)') 
    ax.set_aspect('equal')

    # Set up legend
    lh = ax.get_legend_handles_labels()    
    for label in lh[0]:    
        label.set_alpha(1)
    fig.legend( markerscale=5 )
    fig.show()
    return




if __name__ == '__main__':
     
    # Part 1)  Create two spherical caps
    cap1 = return_cap_vector(  ra = 76 * U.degree, \
                              dec = 36 * U.degree, \
                              rad = 5 * U.degree )

    cap2 = return_cap_vector(  ra = 75 * U.degree, \
                              dec = 35 * U.degree, \
                              rad = 5 * U.degree )

    # Part 2)  Create mangle files based on different combinations of above caps
    mask1 = np.array( [cap1, cap2] )  # Input both caps as one polygon
    mask2a = np.array( [cap1] )       # Input caps separately for two polygons
    mask2b = np.array( [cap2] )
    write_to_mangle_file( mask1, fname="intersection.ply" )
    write_to_mangle_file( mask2a, mask2b, fname="bothcaps.ply" )


    # Part 3)  Read in Mangle files, plot both masks on same plot
    inter = pm.Mangle( "intersection.ply" )
    both  = pm.Mangle( "bothcaps.ply" )

    # Create a bunch of random points inside each mask
    npoints = 10000
    (ra_min,  ra_max)   = (68.5, 82.5)
    (dec_min, dec_max)  = (28.5, 42.5)
    # Use genrand_range() to speed up compared with genrand() 
    #   (restricts random points to rectangle containing the masks)
    (ras_inter, decs_inter)  =  inter.genrand_range( npoints, ra_min,ra_max, dec_min,dec_max )
    (ras_both,  decs_both )  =   both.genrand_range( npoints, ra_min,ra_max, dec_min,dec_max )

    # Create list to feed to the plot_masks function
    plot_inter = [ras_inter, decs_inter, 'Intersection']
    plot_both  = [ras_both,  decs_both,  'Both']
    plot_masks( plot_inter, plot_both )

    print( '\nPart 3: Clearly the first method is equivalent to the Intersection '\
          +'of the two masks, and the second method is the Union of them.')

     
    

    # Part 4)
    # Flip the first spherical cap and then take intersection of that and cap2
    cap1_flip = cap1.copy()
    cap1_flip[-1] = -cap1[-1]

    mask = np.array( [cap1_flip, cap2] )
    fname = "flip1.ply"
    write_to_mangle_file( mask, fname=fname )
    flip1  = pm.Mangle( fname )    
    (ras_flip1, decs_flip1)  =  flip1.genrand_range( npoints, ra_min,ra_max, dec_min,dec_max )

    plot_flip1 = [ras_flip1, decs_flip1, 'Flip1']
    plot_masks( plot_inter, plot_flip1 )

    print( '\nPart 4: In this case the effect of flipping Cap 1 is to select all points '\
          +'inside Cap 2 that are outside Cap 1.')



    # Part 5)
    cap2_flip = cap2.copy()
    cap2_flip[-1] = -cap2[-1]

    mask = np.array( [cap1, cap2_flip] )
    fname = "flip2.ply"
    write_to_mangle_file( mask, fname=fname )
    flip2  = pm.Mangle( fname )
    (ras_flip2, decs_flip2)  =  flip2.genrand_range( npoints, ra_min,ra_max, dec_min,dec_max )

    plot_flip2 = [ras_flip2, decs_flip2, 'Flip2']
    plot_masks( plot_inter, plot_flip1, plot_flip2 )
    
    print( '\nFor following two summaries, the symbol & indicates the logical AND '
          +'(or Intersection) while + indicates logical OR (or Union).' )
    print( '\nPart 5: This visually shows that the Union of (1 & not(2)) + (2 & not(1)) '
          +'+ (1 & 2) is simply the Union of 1 + 2 -- essentially the distributive property.' )


    
    
    # Part 6)
    mask = np.array( [cap1_flip, cap2_flip] )
    fname = "flipboth.ply"
    write_to_mangle_file( mask, fname=fname )
    flip_both  = pm.Mangle( fname )
    npoints = 1000000
    (ras_flip_both, decs_flip_both)  =  flip_both.genrand( npoints )

    plot_flip_both = [ras_flip_both, decs_flip_both, 'Flip_both']
    plot_masks( plot_flip_both )

    print( '\nPart 6: This is simply the conjugate of (1 + 2). In logic terms, '\
          +'this confirms that not(1) & not(2) = not(1 + 2).')
