#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import task from previous week    
from week2.sky_coord_converter import get_coords


if __name__ == '__main__':
    # Just checking that we can successfully import modules from other directories
    name = 'M57'
    get_coords( name )

