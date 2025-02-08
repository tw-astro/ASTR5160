#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from astropy.coordinates import SkyCoord, AltAz
from astropy import units as U
from astropy.coordinates import EarthLocation
from astropy.time import Time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates
import warnings
warnings.filterwarnings("ignore")




# Print RA/Dec coords for given object
def print_ra_dec( coords ):

    # Ensure the passed skycoord is in spherical representation
    coords.representation_type="spherical"    
    print( '\nLocation in RA/Dec:' )
    print( '  RA:  {:.4f}'.format( coords.ra.deg) )
    print( '  Dec: {:.4f}'.format( coords.dec.deg ) )

    return    


# Print Cartesian coords using built-in converter
def print_cartesian( coords ):    
    
    # Use built-in conversions to represent in cartesian
    coords.representation_type="cartesian"
    print( '\nLocation in Cartesian (built-in conversion):' )
    print( '  x: {:.4f}'.format( coords.x ) )
    print( '  y: {:.4f}'.format( coords.y ) )
    print( '  z: {:.4f}'.format( coords.z ) )

    return


# Convert to Cartesian coords and output as list
def compare_cartesian( coords ):    

    # Manually convert to cartesian coords
    xyz = convert_to_cartesian( coords )
    print( '\nLocation in Cartesian (manual conversion):' )
    print( '  x: {:.4f}'.format( xyz[0] ) )
    print( '  y: {:.4f}'.format( xyz[1] ) )
    print( '  z: {:.4f}'.format( xyz[2] ) )
    
    # Compare to check if they agree
    coords.representation_type="cartesian"
    diff_x = coords.x - xyz[0]
    diff_y = coords.y - xyz[1]
    diff_z = coords.z - xyz[2]
    print( '\nDifference beteween built-in and manual conversion:' )
    print( '  diff_x: {:.4f}'.format( diff_x ) )
    print( '  diff_y: {:.4f}'.format( diff_y ) )
    print( '  diff_z: {:.4f}'.format( diff_z ) )

    return


def convert_to_cartesian( coords ):
    
    # Ensure the passed skycoord is in spherical representation
    coords.representation_type="spherical"
    
    # Just to save some time
    dec = coords.dec.degree * U.degree
    ra  = coords.ra.degree  * U.degree
    
    # Convert RA, Dec to Cartesian
    x = np.cos( dec ) * np.cos( ra )
    y = np.cos( dec ) * np.sin( ra )
    z = np.sin( dec )

    return [x, y, z]




if __name__ == '__main__':    
    
    # Part 1: Output coordinates of M51 in ICRS and Cartesian
    print( '\n\nPart 1:')
    name = 'M57'
    print( '\n\nObject name: ' +name +':' )
    coords = SkyCoord.from_name( name )
    print( 'Constellation: ' +coords.get_constellation( coords ) )
    print_ra_dec( coords )
    print_cartesian( coords )
    compare_cartesian( coords )
    

    # Part 2: Output galactic center coordinates in ICRS, and locate on sky    
    print( '\n\nPart 2:')
    name = 'Galactic Center'
    print( 'Object name: ' +name +':' )
    coords = SkyCoord( frame='galactic', l=0*U.degree, b=0*U.degree )
    print( 'Constellation: ' +coords.get_constellation( coords ) )
    coords = coords.transform_to('fk5')
    print_ra_dec( coords )
    print( 'This is on the very eastern edge of Sagittarius, '\
            'very nearly falling within Scorpius/Serpens.')
    
        
    # Part 3: Plot Zenith coordinates at Laramie over a year
    print( '\n\nPart 3:' )
    print( '  Please see attached plot' )
    # Get Location object for Laramie
    laramie = EarthLocation.of_address('Laramie, WY')
    t = Time('2025-01-01')
    t.to_value('mjd')
    (times, ras, decs) = ( [], [], [] )
    # Get galactic lat and galactic long at zenith from Laramie
    for i in range(365):
        t2 = t + i
        zenith = AltAz( alt=90*U.degree, az=0*U.degree, location=laramie, obstime=t2 )
        coord=SkyCoord(zenith).transform_to('galactic')
        ras.append( float(coord.l.deg) )
        decs.append( float(coord.b.deg) )
        times.append( t2.to_value('iso') )

    # Make plots of l and b during year    
    plt.scatter(times, ras, label='Galactic Longitude (l)', s=5 )
    plt.scatter(times, decs, label='Galactic Latitude (b)', s=5 )
    plt.legend()
    plt.xlabel( 'Date (2025)' )
    plt.ylabel( 'Position on sky (deg)')
    plt.title( ' Galactic coordinates at zenith from Laramie' )
    ax = plt.gca()
    ax.xaxis.set_major_locator( dates.MonthLocator(bymonthday=15) )
    ax.xaxis.set_major_formatter( dates.DateFormatter('%b') )
    plt.show()
