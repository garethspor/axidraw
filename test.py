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

originx = 10
originy = 10

ad.pendown()
ad.penup()

ad.moveto(originx, originy)              # Absolute pen-up move, to (1 inch, 1 inch)

for i in range(360 * 15):
    theta = 5 * i * math.pi / 180 * 2;
    rad = i / 100.0
    x = math.cos(theta) * rad
    y = math.sin(theta) * rad
    ad.lineto(originx + x, originy + y)



ad.penup()
ad.goto(0, 0)                # Return home
ad.disconnect()             # Close serial port to AxiDraw
