import math
import sys
import time
from pyaxidraw import axidraw

SVGHEADER = """<svg id="svg_css_ex1" viewBox="0 0 100 100" 
   height="20cm"
   width="20cm"
   xmlns="http://www.w3.org/2000/svg">
"""

PATHHEADER = """  <path
    fill="none"
    stroke="black"
    stroke-width=".2"
    d="
"""
PATHFOOTER = '"/>\n'

SVGFOOTER = '</svg>'

def dip():
    water_x = 5
    water_y = 6
    ad.penup()
    ad.moveto(water_x,water_y)
    ad.pendown()
    ad.penup()

def washBrush():
    water_x = 5
    water_y0 = 2
    water_y1 = 11

    ad.penup()
    ad.moveto(water_x,water_y0)
    
    old_speed_down = ad.options.speed_pendown
    update_ad(100)

    for i in range(3):
        ad.lineto(water_x,water_y1)
        ad.lineto(water_x,water_y0)

    update_ad(old_speed_down)

    time.sleep(0.5)
    ad.penup()
    ad.pendown()
    ad.penup()
    time.sleep(0.5)

def pickUpColor(coords):
    x,y = coords
    color_height = 0.6
    color_width = color_height
    ad.penup()
    ad.moveto(x, y)
    ad.pendown()
    ad.line(0,-color_width)
    # time.sleep(0.05)
    for i in range(2):
        ad.line( color_width,  color_height)
        ad.line(-color_width,  color_height)
        ad.line(-color_width, -color_height)
        ad.line( color_width, -color_height)
        # time.sleep(0.1)
    ad.penup()

def drawBow(origin_x, origin_y, rad):
    numSteps = 24
    for i in range(numSteps + 1):
        theta = math.pi * i / numSteps
        x = origin_x + math.cos(theta) * rad
        y = origin_y - math.sin(theta) * rad
        if i == 0:
            ad.moveto(x,y)
        else:
            ad.lineto(x,y)
    time.sleep(0.5)
    ad.penup()


def update_ad(speed_pendown=30):
    ad.options.units = 1
    ad.options.speed_penup = 100
    ad.options.speed_pendown = speed_pendown
    ad.options.pen_pos_up = 80
    ad.options.pen_pos_down = 55
    ad.update()

def plot_svg(svg,origin_x=0,origin_y=0):
    ad.moveto(origin_x,origin_y)
    ad.plot_setup(svg)
    ad.plot_run()
    ad.connect()
    update_ad()
    ad.f_curr_x = origin_x*0.393701
    ad.f_curr_y = origin_y*0.393701

def interact():
    import pdb; pdb.set_trace()

CLAY   = (3.25, 5.5)
GREEN  = (1.75, 5.5)
YELLOW = (1.75, 7.0)
ORANGE = (1.75, 9)
RED    = (1.75, 10.25)
BLUE   = (3.25, 10.25)
DARK_BLUE = (3.25, 2.5)
DARK_GREEN = (3.25, 9)

RAINBOW = [RED, ORANGE, YELLOW, GREEN, DARK_BLUE]

ad = axidraw.AxiDraw() # Initialize class
ad.interactive()            # Enter interactive mode
connected = ad.connect()    # Open serial port to AxiDraw
if not connected:
    sys.exit() # end script

update_ad()
ad.penup()
ad.pendown()



bow_x = 13.75
bow_y = 10

# washBrush()
# pickUpColor(RED)
# drawBow(bow_x, bow_y, 7)

# washBrush()
# pickUpColor(ORANGE)
# drawBow(bow_x, bow_y, 6.5)

# washBrush()
# pickUpColor(YELLOW)
# drawBow(bow_x, bow_y, 6)

# washBrush()
# pickUpColor(GREEN)
# drawBow(bow_x, bow_y, 5.5)

# washBrush()
# pickUpColor(BLUE)
# drawBow(bow_x, bow_y, 5.0)

# washBrush()
# pickUpColor(DARK_BLUE)
# drawBow(bow_x, bow_y, 4.5)

def hearts():
    HEART = 'heart.svg'

    hx = 9
    hy = 3
    for color in RAINBOW:
        washBrush()
        pickUpColor(color)
        plot_svg(HEART,hx,hy)
        hx+=0.5
        hy+=0.5

def sunflower(color, origin_x, origin_y, scale, num_dots, dot_offset=0, stroke_mag=1, phase=0.333, color_refresh_period=11):
    for i in range(num_dots):
        if color is not None and i%color_refresh_period == 0:
            washBrush()
            pickUpColor(color)
        dot = i + dot_offset + phase
        r = math.sqrt(dot) * scale
        theta = math.pi * 2 * 0.61803399 * dot
        vx = math.cos(theta)
        vy = math.sin(theta)
        px = origin_x + r * vx
        py = origin_y + r * vy
        ad.moveto(px,py)
        ad.line(vx*stroke_mag, vy*stroke_mag)
        ad.penup()

# washBrush()
# pickUpColor(ORANGE)
# interact()
# sunflower(GREEN, 14.5, 8, 0.5, 99)
# sunflower(DARK_BLUE,  14.5, 8, 0.25,  288, dot_offset =  0, stroke_mag=0.25, phase=0.66, color_refresh_period=48)
# sunflower(GREEN,      14.5, 8, 0.25,  36, dot_offset = 36, stroke_mag=0.25, phase=0.66, color_refresh_period=1000)
# sunflower(YELLOW,     14.5, 8, 0.50, 144, dot_offset =  0, stroke_mag=1.00, phase=0.33, color_refresh_period=12)
# sunflower(RED,     14.5, 8, 0.50, 48, dot_offset =  0, stroke_mag=2.60, phase=0.5, color_refresh_period=5)
# sunflower(ORANGE,     16.5, 8+3, 0.05, 48, dot_offset =  16, stroke_mag=2.60, phase=0.5, color_refresh_period=5)

def flower():
    flower_x = 14.5
    flower_y = 8

    tot_dots = 200

    dot_count = 0
    dots_per = 7
    while dot_count < tot_dots:
        # for color in [DARK_GREEN]: #, BLUE, BLUE, GREEN, ORANGE, RED, GREEN, GREEN]:
        washBrush()
        pickUpColor(DARK_GREEN)
        # pickUpColor(YELLOW)
        # pickUpColor(BLUE)
        for i in range(7):
            sunflower(None, flower_x, flower_y, 0.75/2,  dots_per, dot_offset=dot_count, stroke_mag=0.25, phase=0.166/2, color_refresh_period=10000)
            dip()
            dot_count += dots_per
        print(dot_count)

def dabDot(colorA,xA,yA):
    pickUpColor(colorA)
    pickUpColor(colorA)
    pickUpColor(colorA)
    ad.moveto(xA,yA)
    ad.pendown()
    time.sleep(1)
    ad.penup()
    ad.pendown()
    ad.penup()
    washBrush()

def dabLine(colorA,xA,yA, colorB,xB,yB):
    dabDot(colorA,xA,yA)
    dabDot(colorB,xB,yB)
    ad.moveto(xA,yA)
    ad.lineto(xB,yB)
    ad.lineto(xA,yA)
    ad.lineto(xB,yB)
    ad.lineto(xA,yA)
    ad.penup()

def dabLines(val):
    dabLine(RED,12-val,12-val, BLUE,12+val,12-val)
    dabLine(BLUE,12+val,12-val, YELLOW,12+val,12+val)
    dabLine(YELLOW,12+val,12+val, DARK_GREEN,12-val,12+val)
    dabLine(DARK_GREEN,12-val,12+val, RED,12-val,12-val)



# flower()
for i in range(7):
    dabLines(i/2.0)
# dabLines(0.5)
# dabLines(1.0)
# dabLines(1.5)
# dabLines(1)
# interact()

# washBrush()


ad.moveto(0,0)
ad.disconnect()             # Close serial port to AxiDraw
