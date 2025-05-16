#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#import astropy
import os
from astropy.table import Table
import matplotlib.pyplot as plt
import glob

'''
ASTRO5160 Week 8 Class 16: Cross-Matching Surveys
-----------------
-Reads and plots all sources from local VLA FIRST file
   (must be able to access /d/scratch for relevant file)
-Runs remote SDSS query script to find counterparts within 1.2" of first 100 FIRST sources
   (must have previously downloaded 'sdssDR9query.py' into local directory)
-Lists all Legacy Survey sweep files needed to match first 100 FIRST sources to
   Legacy Survey sources (again must have access to /d/scratch)
-----------------
*Note: the decode_sweep_name() and is_in_box() functions taken from Adam's DESI repository'
'''



def plot_aitoff( ras, decs, output_file ):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="aitoff")
    ax.scatter( ras, decs, marker='o', color='r', s=0.1, alpha=0.05 )
    xlab = ['14h','16h','18h','20h','22h','0h','2h','4h','6h','8h','10h']
    ax.set_xticklabels( xlab, weight=600, color='k' )
    ax.grid( color='k', linestyle='dashed', linewidth=1 )
    fig.savefig( output_file )

    
    
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
    ii = ((objs["RA"] >= ramin) & (objs["RA"] < ramax)
          & (objs["DEC"] >= decmin) & (objs["DEC"] < decmax))
    return ii


if __name__ == '__main__':

    # Q1: Read in VLA FIRST file as table
    cwd = os.getcwd()
    first_file = '/d/scratch/ASTR5160/data/first/first_08jul16.fits'
    first_data = Table.read( first_file )
    ras = first_data['RA']
    decs = first_data['DEC']
    output_file = os.path.join( cwd, 'first_sources_plot.png' )
    # Plot with Aitoff projection, save plot to file
    plot_aitoff( ras, decs, output_file )


    # Q3: Do query to find matching SDSS sources within 1.2" of first 100 FIRST sources
    num_sources = 100  # The number of sources to match
    # Save the list of matches the following output file
    outfile = os.path.join( cwd, 'first_sdss_matches.txt' )
    if os.path.exists( outfile ):  os.remove( outfile )
    for i in range( 0, num_sources ):
        print( 'Querying source {:d} of {:d}, with RA, Dec of {:10f}, {:10f}'.format( \
                i+1, num_sources, ras[i], decs[i] ) )
        command = 'python sdssDR9query.py ' +str(ras[i]) +' ' +str(decs[i]) +' >> ' +outfile
        os.system( command )


    # Q6: List all the Legacy Survey Sweep files needed to find matches for first 100
    #     FIRST sources
    def find_needed_sweep_files( N ):
        # Returns list of all sweep files needed to match for first N FIRST sources
        sweeps_path = '/d/scratch/ASTR5160/data/legacysurvey/dr9/north/sweep/9.0/*.fits'
        sweep_files = glob.glob( sweeps_path )
        files_needed = []
        
        for f in sweep_files:
            # Return the ra_min/max and dec_min/max bounds for given sweep file
            radecbox = decode_sweep_name(f)
            # Return True/False list for FIRST sources which fall inside this RA/Dec box
            match_list = is_in_box( first_data[0:N], radecbox )
            # Append the filename if any sources fall within this RA/Dec box
            if True in match_list:
                files_needed.append( f )
        return files_needed

    # Run the above function
    num_sources = 100            
    files_needed = find_needed_sweep_files( num_sources )
    # Print final list of necessary sweep files
    print( '\n\nSweep files needed for first {:d} FIRST sources:'.format( num_sources ) )
    print( *files_needed, sep='\n' )















