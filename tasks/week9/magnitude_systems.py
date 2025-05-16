#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#import astropy
import os
from astropy.table import Table 
import glob
from astropy import units
from astropy.coordinates import SkyCoord, search_around_sky
import numpy as np
import warnings
warnings.filterwarnings("ignore")

'''
ASTRO5160 Week 9 Class 17: Magnitude Systems
-----------------
-Calculates ugriz magnitudes for a given Landolt standard star, based on
   UBVRI colors/magnitudes
-Finds matching source in the Legacy Survey sweeps files
-Converts Legacy Survey flux in maggies to appropriate magnitude
-----------------
*Note: must have access to /d/scratch to access sweep files
'''


def convert_Colors_to_Mags( Colors ):
    # Convert list of V, B-V, U-B, V-R, R-I into list of individual U,B,V,R,I mags
    # Expects a list with 5 values (as shown above)
    if len(Colors) != 5:
        raise Exception( "Must input all five U, B-V, U-B, V-R, R-I magnitudes/colors "\
                        +"as list to convert to individual mags" )    
    (V, BmV, UmB, VmR, RmI) = Colors

    # Convert from colors to individual magnitudes    
    B =  BmV + V
    U =  UmB + B
    R = -VmR + V
    I = -RmI + R

    # Return magnitudes as list
    Mags = [U,B,V,R,I]
    return Mags


def convert_Mags_to_mags( Mags ):
    # Convert list of UBVRI Mags into list of ugriz mags
    # Expects a list with 5 values (U,B,V,R,I)
    if len(Mags) != 5:
        raise Exception( "Must input all five UBVRI magnitudes as list to convert "\
                        +"to ugriz mags" )    
    (U,B,V,R,I) = Mags

    # Use Jester 2005 for stars with R-I<1.15 for conversion
    r = V - 0.42*(B-V) + 0.11
    g = V + 0.60*(B-V) - 0.12
    z = r - 1.72*(R-I) + 0.41
    i = r - 0.91*(R-I) + 0.20
    u = g - 1.28*(U-B) - 1.13

    # Output converted magnitudes as list
    mags = [u,g,r,i,z]
    return mags



def decode_sweep_name(sweepname):
    # Given a Legacy Survey sweeps filename, output the bounding RA/Dec values
    # for the file

    # Extract just the file part of the name
    sweepname = os.path.basename(sweepname)
    # The RA/Dec edges
    ramin,  ramax  = float(sweepname[6:9]), float(sweepname[14:17])
    decmin, decmax = float(sweepname[10:13]), float(sweepname[18:21])
    # Flip the signs on the DECs, if needed.
    if sweepname[9] == 'm':
        decmin *= -1
    if sweepname[17] == 'm':
        decmax *= -1
    return [ramin, ramax, decmin, decmax]


def is_in_box(Ra, Dec, radecbox):
    # Accepts Ra and Dec (in decimal/float form) and a given RA/Dec box
    # (also decimal form) and outputs true/false if location is within box    
    ramin, ramax, decmin, decmax = radecbox

    if decmin < -90. or decmax > 90. or decmax <= decmin or ramax <= ramin:
        msg = "Strange input: [ramin, ramax, decmin, decmax] = {}".format(radecbox)
        raise ValueError(msg)
    is_inside = ((Ra >= ramin) & (Ra < ramax)
             & (Dec >= decmin) & (Dec < decmax))
    
    return is_inside


def convert_maggie( f ):
    # Converts a flux in maggies and outputs the magnitude
    # f: float
    m = 22.5 - 2.5*np.log10( f )
    return m


if __name__ == '__main__':

    # Q1: Convert the UBVRI magnitudes for given Landolt standard star to ugriz mags
    # Note: throughout use Capital variables to indicate UBVRI and lowercase var's for ugriz

    # Values taken from https://james.as.arizona.edu/~psmith/61inch/ATLAS/charts/c109.html
    # Note: 'm' means minus (so BmV is B-V)
    star = 'PG1633+099A'
    RA  = 248.8583  # deg
    Dec = 9.7981    # deg
    V   = 15.256
    BmV = 0.873
    UmB = 0.320
    VmR = 0.505
    RmI = 0.511    
    Colors = [V, BmV, UmB, VmR, RmI]
    
    # Convert Colors to Magnitudes
    Mags = convert_Colors_to_Mags( Colors )
    (U,B,V,R,I) = Mags

    # Convert UBVRI Magnitudes to ugriz magnitudes    
    mags = convert_Mags_to_mags( Mags )
    (u,g,r,i,z) = mags

    # Expected/measured values by SDSS (from SDSS Navigator)
    uexp = 17.30
    gexp = 15.70
    rexp = 15.19
    iexp = 14.71
    zexp = 14.55

    # Display output    
    print( "\n\nStar:  " +star )
    print( "   RA:  {:10f}".format(RA) )
    print( "   Dec: {:10f}".format(Dec) )
    print( "   u:  Conv: {:5.2f}   SDSS: {:5.2f}".format( u, uexp ) )
    print( "   g:  Conv: {:5.2f}   SDSS: {:5.2f}".format( g, gexp ) )
    print( "   r:  Conv: {:5.2f}   SDSS: {:5.2f}".format( r, rexp ) )
    print( "   i:  Conv: {:5.2f}   SDSS: {:5.2f}".format( i, iexp ) )
    print( "   z:  Conv: {:5.2f}   SDSS: {:5.2f}".format( z, zexp ) )
    print( "The g and z channels agree very closely with the directly "\
          +"measured values by SDSS." ) 
        
        
        
    # Q2: Find matching source from the Legacy Survey Sweeps files, convert flux
    #     to magnitudes, compare to above
        
    # Find appropriate sweep file for the given standard source
    sweeps_path = '/d/scratch/ASTR5160/data/legacysurvey/dr9/south/sweep/9.0/*.fits'
    sweep_files = glob.glob( sweeps_path )
    file_needed = []
    
    for f in sweep_files:
        # Return the ra_min/max and dec_min/max bounds for given sweep file
        radecbox = decode_sweep_name(f)
        # Return True/False list for FIRST sources which fall inside this RA/Dec box
        match = is_in_box( RA, Dec, radecbox )
        # Append the filename if any sources fall within this RA/Dec box
        if match:
            file_needed.append( f )
    
    # Check that only one sweep file found
    if len(file_needed) != 1 :
        if len(file_needed) > 1 :
            raise Exception( "More than one sweeps file found, for some reason.")
        else:
            raise Exception( "No sweeps files found for given RA/Dec")
    print( "\nSweep file needed: \n" +file_needed[0] )
        
    # Make a SkyCoord array with only the RA/Dec for the standard star
    loc = SkyCoord( ra=[RA]*units.degree, dec=[Dec]*units.degree, frame='icrs' )
    sweep_data = Table.read( file_needed[0] )
    sweep_ras  = sweep_data['RA']
    sweep_decs = sweep_data['DEC']
    sweep_locs = SkyCoord( ra=sweep_ras, dec=sweep_decs )

    # Find match to standard star, check that only 1 match found, print separation
    (_, idx2, sep2d, _) = search_around_sky( loc, sweep_locs, seplimit=1*units.arcsec )
    if len(sep2d) == 1:
        print( "\nMatch found:\n  Separation = {:6f}".format(sep2d.to(units.arcsec)[0] ) )
    elif len(sep2d) > 1:
        raise Exception( "More than one match found for " +star )
    else:        
        raise Exception( "No matches found for " +star )
        
    # Convert the matched fluxes to magnitudes
    match = sweep_data[idx2]
    g_LS  = convert_maggie( match['FLUX_G'][0]  )
    r_LS  = convert_maggie( match['FLUX_R'][0]  )
    z_LS  = convert_maggie( match['FLUX_Z'][0]  )
    w1_LS = convert_maggie( match['FLUX_W1'][0] )
    w2_LS = convert_maggie( match['FLUX_W2'][0] )
    w3_LS = convert_maggie( match['FLUX_W3'][0] )
    w4_LS = convert_maggie( match['FLUX_W4'][0] )
    
    # Compare results
    print( "Band   SDSS  LegSurv ")
    print( "  g:  {:5.2f}   {:5.2f}".format( g, g_LS ) )
    print( "  r:  {:5.2f}   {:5.2f}".format( r, r_LS ) )
    print( "  z:  {:5.2f}   {:5.2f}".format( z, z_LS ) )
    print( " W1:  -----   {:5.2f}".format( w1_LS ) )
    print( " W2:  -----   {:5.2f}".format( w2_LS ) )
    print( " W3:  -----   {:5.2f}".format( w3_LS ) )
    print( " W4:  -----   {:5.2f}".format( w4_LS ) )

    print( "\nThe grz bands from the Legacy Survey agree well with "\
          +"those measured by SDSS, and there is no detection in the WISE-4 channel")