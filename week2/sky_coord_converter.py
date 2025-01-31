#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.time import Time
import numpy as np


# Retrieve and print coordinates for a given object
def get_coords( name ):
    # Look up by name
    coords = SkyCoord.from_name("M57")  
    # Print in degs
    print( '\nRing Nebula RA/Dec\n\n   in degrees: \n  ' \
            +coords.to_string( 'decimal' ) )
    # Print in hms, d-am-as
    print( '   in hours-mins-sec, deg-arcmin-arcsec: \n  ' 
            +coords.to_string( 'hmsdms'  ) )

    # Convert hms, d-am-as to degs to confirm they match    
    print( '\nConfirming that these are the same: \n ' )
    
    ra_in_deg  = 15 * (18 + 53/60 + 35.0967648/3600 )
    dec_in_deg = 33 + 1/60 + 44.8833/3600
    
    print( '  RA: '  +str(ra_in_deg ) +' deg')
    print( ' Dec:  ' +str(dec_in_deg) +' deg')



# Look up time and print in different systems
def get_time( ):

    t = Time.now()
    
    # Print in different styles/units
    print( '\n\nCurrent time: \n' +str(t) )
    print( '  JD: ' +str(t.jd) )
    print( ' MJD: ' +str(t.mjd) )
    print( ' Difference: ' +str( t.jd - t.mjd ) )
    
    print( '\n\n  Some MJD\'s for the next two weeks: \n' )

    # Print next two weeks' dates in MJD
    for a in np.arange(14):
        print( str( int( t.mjd +a  ) ) )
  
    
  
if __name__ == '__main__':
    name = 'M51'
    get_coords( name )
