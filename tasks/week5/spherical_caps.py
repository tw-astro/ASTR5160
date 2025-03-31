#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tony Weinbeck
Astro 5160
Class 10: Spherical Caps
"""

from astropy.coordinates import SkyCoord
from astropy import units as U
import numpy as np
import re  # To replace characters in a string



def return_cap_vector( ra, dec, radius ):
    # Takes RA, Dec, and cap_radius as inputs, and outputs 4-vector associated with spherical cap
    
    coord = SkyCoord( ra + 6*U.hourangle, dec, frame='icrs' )
    coord.representation_type="cartesian"
    vector = np.array( [coord.x.value, coord.y.value, coord.z.value, (1-np.sin( (90*U.degree - radius)).value ) ] )
    # Note that for fourth vector element, the 'size' of the spherical cap, 
    #   I'm inputting everything in terms of the radius of cap, hence the 
    #   '(90 - radius)' within the sine function. Agrees with expected.

    # Print vector with formatting    
    np.set_printoptions(formatter={'float': '{: 8.6f}'.format})
    print( vector )
    return vector



def print_formatted_vectors( v ):
    # Prints multiple spherical cap vectors with specific formatting
    # Accepts either either a single vector or an array of vectors

    # Determine whether v is a single vector or array of vectors
    if 'numpy.ndarray' in str( type(v[0]) ):
        length = len(v)
    else: 
        length = 1

    # Print output
    print( '1 polygons' )
    print( 'polygon 1 ( ' +str(length) +' caps, 1 weight, 0 pixel, 0 str):' )
    np.set_printoptions(formatter={'float': '{: 11.9f}'.format})
    print( '  ' +re.sub( r"[\[\]]", "", str(v)  ) )
    # This is ugly but it just prints the formatted list without the brackets
    return




if __name__ == '__main__':
     
    # Part 1:
    print( '\nPart 1: ')
    ra  = 5 * U.hourangle
    dec = 0 * U.degree
    cap_radius = 90 * U.degree
    
    v1 = return_cap_vector( ra, dec, cap_radius )
    # Result agrees with your answer

    
    # Part 2:    
    print( '\nPart 2: ')
    ra  = 0 * U.hourangle
    dec = 90 * U.degree
    cap_radius = (90-36) * U.degree
    
    v2 = return_cap_vector( ra, dec, cap_radius )
    # Result agrees with your answer
    

    # Part 3:    
    print( '\nPart 3: ')
    ra  = 5 * U.hourangle
    dec = 36 * U.degree
    cap_radius = 1 * U.degree
    
    v3 = return_cap_vector( ra, dec, cap_radius )
    # Result does NOT agree with your answer — mine is rotated by pi/2 in the x-y plane
    #   relative to your answer. This is consistent with Part 1 — specifically,
    #   if your answer for Part 1 is correct, you can continuously deform the dec and
    #   cap_radius inputs to match my answer for Part 3. If I'm wrong here, please
    #   let me know what I'm missing!


    # Part 4:    
    print( '\nPart 4: ')
    print_formatted_vectors( np.array([v1, v2, v3]) )
    # Formatting is basically the same, except I'm outputting everything as floats    
