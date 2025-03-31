#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 12:15:36 2025
@author: Tony weinbeck@alum.mit.edu
"""

from astropy.coordinates import SkyCoord
import astropy.units as U
import numpy as np
from numpy.random import random
import matplotlib.pyplot as plt

pi=np.pi



# Convert to Cartesian coords using built-in converter
def convert_to_cartesian( coords ):    

    coords.representation_type="cartesian"
    print( 'Location in Cartesian (built-in conversion):' )
    print( '  x: {:.4f}'.format( coords.x ) )
    print( '  y: {:.4f}'.format( coords.y ) )
    print( '  z: {:.4f}\n'.format( coords.z ) )

    return [ coords.x, coords.y, coords.z ]


# Generate random list within specified limits
def gen_random_w_bounds( lower_lim, upper_lim, num ):

    distrib = (upper_lim - lower_lim)/2 * ( 1 - random( num )*2 )  \
            + (upper_lim + lower_lim)/2
    return distrib
   


# Find the angle between two sky coordinates, and check if agrees w/ built-in routine    
def part_1( loc1, loc2 ):
    
    # Part 1
    print( '\n\n Part 1 \n\n')
    
    xyz1 = convert_to_cartesian( loc1 )
    xyz2 = convert_to_cartesian( loc2 )

    # Calculate dot product using cartesian coords    
    dot_prod   = xyz1[0]*xyz2[0] + xyz1[1]*xyz2[1] + xyz1[2]*xyz2[2]
    # Use def of dot product to find angle between points
    angle_man  = np.arccos( dot_prod )
    # Use built-in method to calculate the same
    angle_auto = loc1.separation( loc2 )
    
    # Compare calculated and built-in results
    print( "Dot product:    {:7.5f}".format( dot_prod ) )
    print( "Angle_manual:   {:7.4f}".format( angle_man.to(U.deg) ) )
    print( "Angle_built-in: {:7.4f}".format( angle_auto.deg ) +" deg" )
    
    return

    

# Create two sets of SkyCoords within a given RA/Dec range, and plot together
def part_2( num, ra_max, ra_min, dec_max, dec_min, fig, ax ):    

    # Part 2
    print( '\n\n Part 2 \n\n')
    

    # Create set of RAs/Decs    
    ras1 = gen_random_w_bounds(   ra_min,  ra_max, num )
    decs1 = gen_random_w_bounds( dec_min, dec_max, num )
    set1 = SkyCoord( ras1, decs1, frame="icrs" )
    
    # Create another set of RAs/Decs
    ras2 = gen_random_w_bounds(   ra_min,  ra_max, num )
    decs2 = gen_random_w_bounds( dec_min, dec_max, num )
    set2 = SkyCoord( ras2, decs2, frame="icrs" )
    
    # Plot on cartesian grid
    plt.scatter( ras1, decs1, c='b', marker='+', label='Set 1' )
    plt.scatter( ras2, decs2, c='r', marker='x', label='Set 2' )
    
    ax.set_xlabel( 'RA (hours)')
    ax.set_ylabel( 'Dec (deg)')
    ax.invert_xaxis()
    ax.grid( color='gray', linestyle='dashed', linewidth=0.5 )
 
    # Return the two sets of SkyCoord lists
    return set1, set2



# Find matching points between two sets within given separation angle, and plot up
def part_3( set1, set2, sep_in_arcmin, fig, ax ):

    # Part 3
    print( '\n\n Part 3 \n\n')
    
    # Find elements of set2 which lie within given dist of a point in set1
    matches2 = np.full( len(set2), False, dtype=bool )
    for s in set1:
        mask = s.separation( set2 ) < sep_in_arcmin/60 *U.deg
        # Take running logical mask to keep all points
        matches2 = np.logical_or.reduce( [ matches2, mask ] )
    
    # Find elements of set1 which lie within given dist of a point in set2
    matches1 = np.full( len(set1), False, dtype=bool )
    for s in set2:
        mask = s.separation( set1 ) < sep_in_arcmin/60 *U.deg
        matches1 = np.logical_or.reduce( [ matches1, mask ] )
    
    # Plot in a yellow highlighter-color over the existing plots
    x = set1[matches1].ra.hourangle
    y = set1[matches1].dec.degree
    plt.scatter( x, y, c='y', s=25, marker='o', label='Matches within 10\'', alpha=.65 )

    # Same for set2 matches
    x = set2[matches2].ra.hourangle
    y = set2[matches2].dec.degree
    plt.scatter( x, y, c='y', s=25, marker='o', alpha=.65 )
    
    ax.legend( loc='center', ncol=3, bbox_to_anchor=(0.5, 1.05) )
    fig.show()

    return



if __name__ == '__main__':
    
    # Part 1
    # Find the angle between these two
    loc1 = SkyCoord("263.75 -17.9", unit="deg", frame="icrs")
    loc2 = SkyCoord("20h24m59.9s +10d6m0s", frame="icrs")
    
    part_1( loc1, loc2 )

    
    # Part 2    
    # Plot on same graph two separate sets of SkyCoords
    num=100    
    ra_max = 3 *U.hourangle
    ra_min = 2 *U.hourangle
    dec_max =  2 *U.deg
    dec_min = -2 *U.deg

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="rectilinear")

    set1, set2 = part_2( num, ra_max, ra_min, dec_max, dec_min, fig, ax )
    
    
    # Part 3
    # Now find matches to within 10' between the two sets
    sep_in_arcmin = 10
    
    part_3( set1, set2, sep_in_arcmin, fig, ax )
