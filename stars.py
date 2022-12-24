import math
import sys

from pyaxidraw import axidraw

ad = axidraw.AxiDraw() # Initialize class

ad.interactive()            # Enter interactive mode
connected = ad.connect()    # Open serial port to AxiDraw

if not connected:
    sys.exit() # end script

# Draw square, using "moveto/lineto" (absolute move) syntax:
ad.options.units = 1              # set working units to cm.
ad.options.speed_pendown = 50     # set pen-down speed to slow
ad.options.pen_pos_up = 90        # select a large range for the pen up/down swing
ad.options.pen_pos_down = 10

ad.update()                 # Process changes to options

originx = 5
originy = 5

import random

theta = random.randint(0,628)

# ad.moveto(originx, originy)              # Absolute pen-up move, to (1 inch, 1 inch)
ad.pendown()
ad.penup()

order = random.randint(2,6)*2+1
rad = 5.0
thetastep = ((order - 1) / 2) * 2.0 * math.pi / order
i = 0
while rad >= 3:
# for i in range(10 * order + 1):
    theta += thetastep;
    x = math.cos(theta) * rad + originx
    y = math.sin(theta) * rad + originy
    x *= 2
    y *= 2
    if i == 0:
        ad.moveto(x, y)
    else:
        ad.lineto(x, y)
    rad -= 0.11
    i += 1



ad.penup()
ad.goto(0, 0)                # Return home
ad.disconnect()             # Close serial port to AxiDraw
