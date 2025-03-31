#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from astropy.table import Table
import matplotlib.pyplot as plt

# Set up path and file structure
home = os.getenv("HOME")
class_path  = home +'/Documents/Classes/TechniquesII/'



# Read in table 
def read_table():
    
    # Read in file as a Table
    table_fname = class_path +'struc.fits' 
    objs = Table.read( table_fname )
    # Print the column names
    print( objs.colnames )
    
    # Plot RA vs Dec for all sources
    plt.scatter( objs['RA'], objs['DEC'], marker ='+', c='b', alpha=0.5, \
                 label='All sources' )
    plt.xlabel('Right Ascension (degs)')
    plt.ylabel('Declination (degs)')


    # Boolean indexing: identify only sources with higher extinction    
    reddened = objs['EXTINCTION'][:,0] > 0.22
    
    # Overplot these sources in red
    plt.scatter( objs[reddened]['RA'], objs[reddened]['DEC'], \
                 marker ='+', c='r', alpha=0.5, label='High extinction' )
    plt.legend()
    # Save figure as PNG
    plt.savefig( class_path +'struc-RA-dec.png', dpi=300 )
    plt.show()

    
if __name__ == '__main__':
    read_table()
    
