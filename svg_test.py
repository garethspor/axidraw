#!/usr/bin/env python3
# -*- encoding: utf-8 -#-


import sys
import os.path
from pyaxidraw import axidraw

ad = axidraw.AxiDraw()             # Create class instance

# ad.interactive()            # Enter interactive mode
# connected = ad.connect()    # Open serial port to AxiDraw

# if not connected:
#     sys.exit() # end script

# ad.options.units = 1              # set working units to cm.
# ad.options.speed_pendown = 50     # set pen-down speed to slow
# ad.options.pen_pos_up = 90        # select a large range for the pen up/down swing
# ad.options.pen_pos_down = 10

SVG = """
<svg id="svg_css_ex1" viewBox="0 0 100 100" 
   height="30mm"
   width="100mm"
   xmlns="http://www.w3.org/2000/svg">
  <path
    fill="none"
    stroke="red"
    d="M 10,30
       A 20,20 0,0,1 50,30
       A 20,20 0,0,1 90,30
       Q 90,60 50,90
       Q 10,60 10,30 z
       " />
</svg>
"""

FILE = "AxiDraw_trivial.svg"


ad.plot_setup(SVG)    # Parse the input file
# ad.options.speed_pendown = 50 # Set maximum pen-down speed to 50%
# ad.penup()
# ad.goto(3, 3)                # Return home
# ad.pendown()
ad.plot_run()   # plot the document

ad.penup()
ad.goto(0, 0)                # Return home
ad.disconnect()             # Close serial port to AxiDraw
