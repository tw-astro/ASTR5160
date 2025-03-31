#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Import matplotlib plotting library
import matplotlib.pyplot as plt


# Output the result of x^2 + 3x + 8 when supplied argument x
def quad_funct( x ):
        y = x**2 +  3*x + 8
        return y


# Calculate the above quadratic function for each value from 0->100, and plot the result
def plot_quad_funct():
        # Create array of x values from 0-100, and calculate function at each whole number
        x_vals = range(100)
        y_vals = []
        for x in x_vals:
                y_vals.append( quad_funct( x ) )
 
        plt.plot( x_vals, y_vals )
        plt.xlabel('x (units of x)')
        plt.ylabel('y (units of y)')
        plt.show()


# Run above function(s)
if __name__ == "__main__":
        plot_quad_funct()
