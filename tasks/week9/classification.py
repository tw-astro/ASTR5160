#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#import astropy
import os
from astropy.table import Table, vstack
import glob
from astropy import units
from astropy.coordinates import SkyCoord, search_around_sky
import matplotlib.pyplot as plt
import numpy as np
import warnings
warnings.filterwarnings("ignore")

'''
ASTRO5160 Week 9 Class 18: Classification
-----------------
-Read in data for positions of spectroscopically confirmed stars and qsos
-Match positions for each type of object with SDSS Sweep Files
-Convert flux for each object to dust-corrected magnitudes
-Plot on color-color diagrams
-Determine if we can distinguish between objects using a color cut
-Saves plots with color cut to png files
-----------------
*Note: must have access to /d/scratch to download object data and sweep files
'''


# First two functions copied from Adam, and also from my Week 8/Class 16 file
def decode_sweep_name(sweepname):
    """Retrieve RA/Dec edges from a full directory path to a sweep file
    Parameters
    ----------
    sweepname : :class:`str`
        Full path to a sweep file, e.g., /a/b/c/sweep-350m005-360p005.fits
    Returns
    -------
    :class:`list`
        A 4-entry list of the edges of the region covered by the sweeps file
        in the form [RAmin, RAmax, DECmin, DECmax]
        For the above example this would be [350., 360., -5., 5.]
    """
    # ADM extract just the file part of the name.
    sweepname = os.path.basename(sweepname)
    # ADM the RA/Dec edges.
    ramin,  ramax  = float(sweepname[6:9]), float(sweepname[14:17])
    decmin, decmax = float(sweepname[10:13]), float(sweepname[18:21])
    # ADM flip the signs on the DECs, if needed.
    if sweepname[9] == 'm':
        decmin *= -1
    if sweepname[17] == 'm':
        decmax *= -1
    return [ramin, ramax, decmin, decmax]


def is_in_box(objs, radecbox):
    """Determine which of an array of objects are inside an RA, Dec box.
    Parameters
    ----------
    objs : :class:`~numpy.ndarray`
        An array of objects. Must include at least the columns "RA" and "DEC".
    radecbox : :class:`list`
        4-entry list of coordinates [ramin, ramax, decmin, decmax] forming the
        edges of a box in RA/Dec (degrees).
    Returns
    -------
    :class:`~numpy.ndarray`
        ``True`` for objects in the box, ``False`` for objects outside of the box.
    Notes
    -----
        - Tests the minimum RA/Dec with >= and the maximum with <
    """
    ramin, ramax, decmin, decmax = radecbox
    # ADM check for some common mistakes.
    if decmin < -90. or decmax > 90. or decmax <= decmin or ramax <= ramin:
        msg = "Strange input: [ramin, ramax, decmin, decmax] = {}".format(radecbox)
        raise ValueError(msg)
    ii =   ((objs["RA"] >= ramin) & (objs["RA"] < ramax)
          & (objs["DEC"] >= decmin) & (objs["DEC"] < decmax))
    return ii


def plot_color_color( x1, x2, y1, y2, m, b ):
    # Plot color (x1-x2) vs (y1-y2) for the given data and bands,
    # along with a linear function given by y=mx+b
    plt.figure()
    # Plot color-color for stars
    x_ax1 = mags_stars[x1]-mags_stars[x2]
    y_ax1 = mags_stars[y1]-mags_stars[y2]    
    plt.scatter( x_ax1, y_ax1, label='stars',
                 marker='o', color='b', s=1, alpha=.5  )    

    # Plot for qso's
    x_ax2 = mags_qsos[x1]-mags_qsos[x2]
    y_ax2 = mags_qsos[y1]-mags_qsos[y2]
    plt.scatter( x_ax2, y_ax2, label='qsos',
                 marker='o', color='g', s=1, alpha=.5  )  

    # Add the linear function for the color cut
    plt.plot( x_ax1, m*x_ax1 + b, '-', color='r', linewidth=0.5, \
              label='{:4.2f}*x +{:4.2f}'.format(m, b) )
    plt.xlabel( x1 +' - ' +x2 )
    plt.ylabel( y1 +' - ' +y2 )
    plt.legend()
    plt.savefig( os.path.join( cwd, x1 +'_minus_' +x2 +'-vs-'\
                                   +y1 +'_minus_' +y2 +'.png' ) )



if __name__ == '__main__':
    
    # Q1: Read in Star and QSO data as tables, 
    #     match to sources within sweep files

    # Set up path structure, read in data as tables
    cwd = os.getcwd()
    path = '/d/scratch/ASTR5160/week10/'    
    stars_file = os.path.join( path, 'stars-ra180-dec30-rad3.fits' )
    qsos_file  = os.path.join( path,  'qsos-ra180-dec30-rad3.fits' )
    stars_data = Table.read( stars_file )
    qsos_data  = Table.read( qsos_file )


    # Find appropriate sweep files for above two files
    sweeps_path = '/d/scratch/ASTR5160/data/legacysurvey/dr9/south/sweep/9.0/*.fits'
    sweep_files = glob.glob( sweeps_path )
    files_needed = []
    
    # Cycle through each sweep file, determine if needed
    for f in sweep_files:
        # Return the ra_min/max and dec_min/max bounds for given sweep file
        radecbox = decode_sweep_name(f)
        # Return True/False list for FIRST sources which fall inside this RA/Dec box
        match_list1 = is_in_box( stars_data, radecbox )
        match_list2 = is_in_box( qsos_data,  radecbox )
        # Append the filename if any sources fall within this RA/Dec box
        if True in match_list1 or True in match_list2: 
            files_needed.append( f )    
    #print( files_needed )  # Confirmed that it finds four files

    # Combine the needed sweep file tables into one large (!) table
    sweep_data = []
    for f in files_needed:
        data = Table.read( f )
        if len( sweep_data ) == 0:
            sweep_data = data
        else:
            sweep_data = vstack( [sweep_data, data] )            


    # Create SkyCoord arrays for RA/Dec pairs for each file
    # (needed for search_around_sky)
    stars_ras  = stars_data['RA']
    stars_decs = stars_data['DEC']
    stars_locs = SkyCoord( ra=stars_ras *units.degree, 
                          dec=stars_decs*units.degree, frame='icrs' )
    qsos_ras   = qsos_data['RA']
    qsos_decs  = qsos_data['DEC']
    qsos_locs  = SkyCoord( ra=qsos_ras *units.degree, 
                          dec=qsos_decs*units.degree, frame='icrs' )
    sweep_ras  = sweep_data['RA']
    sweep_decs = sweep_data['DEC']
    sweep_locs = SkyCoord( ra=sweep_ras, dec=sweep_decs, frame='icrs' )


    # Find matches for stars within sweep files
    (idx1_stars, idx2_stars, sep2d_stars, _) = search_around_sky( \
                    stars_locs, sweep_locs, seplimit=0.5*units.arcsec )
    # Same for qso's
    (idx1_qsos, idx2_qsos, sep2d_qsos, _) = search_around_sky( \
                    qsos_locs,  sweep_locs, seplimit=0.5*units.arcsec )



    # Q2: For each unique match, convert the flux into a dust-corrected magnitude

    # Check for duplicate matches
    values = []
    duplicates_stars = []
    for i in idx1_stars:
        if i not in values:
            values.append(i)
        else:
            duplicates_stars.append(i)
    # Same for qso's
    values = []
    duplicates_qsos = []
    for i in idx1_qsos:
        if i not in values:
            values.append(i)
        else:
            duplicates_qsos.append(i)


    # Make new tables and populate with converted stellar magnitudes 
    headers = ['RA','Dec','g','r','z','w1','w2']
    mags_stars = Table( names=headers )
    for i in idx1_stars:
        if i not in duplicates_stars:
            ra  = stars_data[i]['RA']
            dec = stars_data[i]['DEC']

            idx1 = list(idx1_stars).index(i)
            idx2 = idx2_stars[idx1]
            G  = sweep_data[idx2]['FLUX_G']  / sweep_data[idx2]['MW_TRANSMISSION_G'] 
            R  = sweep_data[idx2]['FLUX_R']  / sweep_data[idx2]['MW_TRANSMISSION_R']
            Z  = sweep_data[idx2]['FLUX_Z']  / sweep_data[idx2]['MW_TRANSMISSION_Z']
            W1 = sweep_data[idx2]['FLUX_W1'] / sweep_data[idx2]['MW_TRANSMISSION_W1']
            W2 = sweep_data[idx2]['FLUX_W2'] / sweep_data[idx2]['MW_TRANSMISSION_W2']
            g  = 22.5 - 2.5 * np.log10(G) 
            r  = 22.5 - 2.5 * np.log10(R) 
            z  = 22.5 - 2.5 * np.log10(Z) 
            w1 = 22.5 - 2.5 * np.log10(W1)
            w2 = 22.5 - 2.5 * np.log10(W2)
            mags_stars.add_row( [ra, dec, g, r, z, w1, w2] )

    # Same for qso's
    mags_qsos = Table( names=headers )
    for i in idx1_qsos:
        if i not in duplicates_qsos:
            ra  = qsos_data[i]['RA']
            dec = qsos_data[i]['DEC']

            idx1 = list(idx1_qsos).index(i)
            idx2 = idx2_qsos[idx1]
            G  = sweep_data[idx2]['FLUX_G']  / sweep_data[idx2]['MW_TRANSMISSION_G'] 
            R  = sweep_data[idx2]['FLUX_R']  / sweep_data[idx2]['MW_TRANSMISSION_R']
            Z  = sweep_data[idx2]['FLUX_Z']  / sweep_data[idx2]['MW_TRANSMISSION_Z']
            W1 = sweep_data[idx2]['FLUX_W1'] / sweep_data[idx2]['MW_TRANSMISSION_W1']
            W2 = sweep_data[idx2]['FLUX_W2'] / sweep_data[idx2]['MW_TRANSMISSION_W2']
            g  = 22.5 - 2.5 * np.log10(G) 
            r  = 22.5 - 2.5 * np.log10(R) 
            z  = 22.5 - 2.5 * np.log10(Z) 
            w1 = 22.5 - 2.5 * np.log10(W1)
            w2 = 22.5 - 2.5 * np.log10(W2)
            mags_qsos.add_row( [ra, dec, g, r, z, w1, w2] )


    # Q3: Plot various colors vs each other to determine if we can visually
    #     classify the objects via a color cut

    # Plot (g-z) vs (r-W1) for stars and qsos
    x1 = 'g'
    x2 = 'z'
    y1 = 'r'
    y2 = 'w1'
    plot_color_color( x1, x2, y1, y2, 1, -1 )

    # Plot (g-r) vs (z-w2)
    x1 = 'g'
    x2 = 'r'
    y1 = 'z'
    y2 = 'w2'
    plot_color_color( x1, x2, y1, y2, .5, -.75 )

    # Plot (g-r) vs (z-w1)
    x1 = 'g'
    x2 = 'r'
    y1 = 'z'
    y2 = 'w1'
    plot_color_color( x1, x2, y1, y2, .75, -.75 )