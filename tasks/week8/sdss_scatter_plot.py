#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'''
ASTRO5160 Week 8 Class 15: SDSS SQL Query
-----------------
-Use SDSS SQL Query (via https://skyserver.sdss.org/dr9/en/help/howto/search/simplequery.asp)
-Exact query:
    SELECT p.ra, p.dec, p.g
    FROM photoObj p, dbo.fGetNearbyObjEq(300,-1,2) n
    WHERE p.objID = n.objID
-Plot all sources matching above query
-Plot all sources with size proportional to brightness
-----------------
*Note: must have pandas module installed to handle data frames
'''

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as tk
import numpy as np
import math


def plot_within_bounds( df, col, lower_bound=-np.inf, upper_bound=np.inf, size=36 ):
    # Function to plot all objects from 'df' data frame whose column values
    #   lie within a specified range

    # Select only objects with magnitude within range    
    mask = (df[col] > lower_bound) & (df[col] < upper_bound)
    selected = df[mask]
    # The RA's and Dec's of selected objects
    ras  = selected['ra']
    decs = selected['dec']

    # Plot selected RA/Dec pairs on scatter plot
    plt.scatter( ras, decs, s=size, c='b', alpha=0.5 )

    # Format scatter plot
    plt.gca().invert_xaxis()
    plt.gca().set_aspect('equal')
    plt.grid(True)
    plt.xlabel( 'RA' )
    plt.ylabel( 'Dec' )
    # This is just to ensure format of major ticks is normal person numbers
    plt.gca().xaxis.set_major_formatter(tk.StrMethodFormatter('{x:.2f}'))
    plt.gca().yaxis.set_major_formatter(tk.StrMethodFormatter('{x:.2f}'))
    
    return



if __name__ == '__main__':
    # Assuming we've already done the appropriate SQL query (see header above),
    #   read results of SQL search, put into Pandas data frame
    fname = 'sql_results.csv'
    df = pd.read_csv( fname )
 
    # Plot ALL objects using constant size
    plot_within_bounds( df, 'g', size=9 )
    plt.show()

    # Set plotting parameters in order to plot brighter objects in larger size
    min_g = math.floor( min(df['g']) )
    max_g = math.ceil(  max(df['g']) )
    range_g = (max_g - min_g)
    max_size = 100
    min_size = 2
    range_s = (max_size - min_size)

    for i in range( min_g, max_g ):
        # Set size decreasing quadratically from max_size to min_size
        size = max_size - np.sqrt( ( (i-min_g) / (range_g-1) ) ) * range_s
        # Plot objects within 1-magnitude bins, using decreasing size
        plot_within_bounds( df, 'g', lower_bound=i, upper_bound=i+1, size=size )
    plt.show()
