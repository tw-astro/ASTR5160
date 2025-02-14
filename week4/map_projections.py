#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 10:14:30 2025
@author: Tony weinbeck@alum.mit.edu
"""

import numpy as np
from numpy.random import random
import matplotlib.pyplot as plt
pi = np.pi


# Creates a series of random RA's and Dec's, and plots them on three different projections
def compare_projections( num_sources ):

    # Generate list of RA's ranging from [-pi, pi) 
    ras = 2*pi* ( random( num_sources ) - 0.5 )
    # Generate list of dec's ranging from (-pi/2, pi/2], but geometrically weighted by arcsin
    decs = np.arcsin( 1 - random( num_sources )*2)
    
    # Plot on cartesian grid
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="rectilinear")
    ax.scatter( ras, decs, marker='o', color='r', s=0.7, alpha=0.3 )
    xlab = ['14h','16h','18h','20h','22h','0h','2h','4h','6h','8h','10h']
    ax.set_xticklabels( xlab, weight=400, color='k' )
    ax.set_xlabel( 'RA ')
    ylab = ['-75°','-60°','-45°','-30°','-15°','0°','15°','30°','45°','60°','75°']
    ax.set_yticklabels( ylab, weight=400, color='k' )    
    ax.set_ylabel( 'Dec ')
    ax.grid( color='b', linestyle='dashed', linewidth=1 )
    fig.show()

    
    # Plot with Aitoff projection
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="aitoff")
    ax.scatter( ras, decs, marker='o', color='r', s=0.7, alpha=0.3 )
    xlab = ['14h','16h','18h','20h','22h','0h','2h','4h','6h','8h','10h']
    ax.set_xticklabels( xlab, weight=600, color='k' )
    ax.grid( color='b', linestyle='dashed', linewidth=1 )
    # This grid looks *awful* on the plot, with blue datapoints
    fig.show()
    
    
    # Plot with Lambert projection
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="lambert")
    ax.scatter( ras, decs, marker='o', color='r', s=0.7, alpha=0.3 )
    xlab = ['14h','16h','18h','20h','22h','0h','2h','4h','6h','8h','10h']
    ax.set_xticklabels( xlab, weight=600 )
    ax.grid( color='b', linestyle='dashed', linewidth=1 )
    fig.show()
    

if __name__ == '__main__':
  
    num_sources = 10000
    compare_projections( num_sources )
  
