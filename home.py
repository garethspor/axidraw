import sys
import time

from pyaxidraw import axidraw

ad = axidraw.AxiDraw() # Initialize class

ad.interactive()            # Enter interactive mode
connected = ad.connect()    # Open serial port to AxiDraw

if not connected:
    sys.exit() # end script

ad.options.units = 1
ad.options.speed_penup = 100
ad.options.pen_pos_up = 50
ad.options.pen_pos_down = 20
ad.update()

# ad.penup()
# ad.pendown()
# ad.penup()
# time.sleep(1)
# ad.pendown()
ad.penup()

ad.disconnect()             # Close serial port to AxiDraw
