import random
import math
import sys
import time
from pyaxidraw import axidraw
import numpy as np

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

def washBrushOld():
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
    color_height = 0.2
    color_width = color_height
    ad.penup()
    ad.moveto(x, y)
    ad.pendown()
    ad.line(0,-color_width)
    # time.sleep(0.05)
    for i in range(1):
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
    ad.options.pen_pos_up = 70
    ad.options.pen_pos_down = 35
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

def dabDot(colorA,xA,yA,delay=1):
    pickUpColor(colorA)
    pickUpColor(colorA)
    pickUpColor(colorA)
    ad.moveto(xA,yA)
    ad.pendown()
    time.sleep(delay)
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

def ovalPos(xo,yo,rx,ry,deg0):
    theta_rad = math.pi * deg0 / 180.0
    x = math.cos(theta_rad) * rx + xo
    y = math.sin(theta_rad) * ry + yo
    return (x,y)

def ovalSegment(xo,yo,rx,ry,deg0,deg1, straight=False):
    degStep = deg1-deg0 if straight else (5 if deg1 > deg else -5)
    started = False
    for theta_deg in [deg0] if deg0==deg1 else np.arange(deg0,deg1+degStep,degStep):
        theta_rad = math.pi * theta_deg / 180.0
        x = math.cos(theta_rad) * rx + xo
        y = math.sin(theta_rad) * ry + yo
        if not started:
            ad.moveto(x,y)
            ad.pendown()
            started = True
        else:
            ad.lineto(x,y)
    ad.penup()


HOT_PINK = (4,4)
RED = (4,7)
YELLOW = (1,10)
GREEN = (7,10)
ORANGE = (4,13)
DARK_BLUE=(10,13)
LIGHT_BLUE=(10,17)
PURPLE=(10,7)
LIGHT_GREEN=(7,13)
TURQUOISE=(7,16)
WHITE=(1,16)
BLACK=(10,1.5)

NICE_BLUE = (10,10)
NICE_YELLOW = (1.5,13)

ALL_COLORFUL = [RED,ORANGE,YELLOW,LIGHT_GREEN,TURQUOISE,NICE_BLUE,DARK_BLUE,PURPLE,HOT_PINK,]#,WHITE,BLACK]
def randColorGen():
    colors_to_dispense = ALL_COLORFUL
    while True:
        i  = random.randint(0,len(colors_to_dispense)-1)
        yield colors_to_dispense[i]
def allColorGen():
    color_index = 0
    colors_to_dispense = ALL_COLORFUL
    while True:
        i  = color_index % len(colors_to_dispense)
        yield colors_to_dispense[i]
        color_index += 1

def getColor():
    colors_to_dispense = [RED,ORANGE,YELLOW,GREEN,DARK_BLUE,PURPLE,HOT_PINK]
    # colors_to_dispense = [CLAY,GREEN,YELLOW,ORANGE,RED,BLUE,DARK_BLUE,DARK_GREEN]
    color_index = 0
    while True:
        # i  = random.randint(0,len(colors_to_dispense)-1)
        i = color_index % len(colors_to_dispense)
        yield colors_to_dispense[i]
        color_index += 1

def getSeaColors():
    colors_to_dispense = [GREEN,DARK_BLUE,PURPLE,HOT_PINK]
    color_index = 0
    while True:
        i = color_index % len(colors_to_dispense)
        yield colors_to_dispense[i]
        color_index += 1
def getOddColors():
    colors_to_dispense = [HOT_PINK,DARK_BLUE,PURPLE]
    color_index = 0
    while True:
        i = color_index % len(colors_to_dispense)
        yield colors_to_dispense[i]
        color_index += 1
def getEvenColors():
    colors_to_dispense = [RED, ORANGE, YELLOW ]
    color_index = 0
    while True:
        i = color_index % len(colors_to_dispense)
        yield colors_to_dispense[i]
        color_index += 1


def ovalExp():
    xo=20
    yo=8
    for i in range(4,12):
        color_gen = getOddColors() if (i % 2) else getEvenColors()
        segments = i

        washBrush(ditch_excess=False)
        for s in range(72):
            seg_span = 5

            rx = (i-2) * 0.6
            ry = rx * 1
            deg0 = s * seg_span
            deg1 = deg0 + seg_span

            if s == 0:
                x0, y0 = ovalPos(xo,yo, rx,ry, deg0)
                ad.moveto(x0,y0)
            x1, y1 = ovalPos(xo,yo, rx,ry, deg1)
            ad.lineto(x1,y1)
        ad.penup()

        for s in range(segments):
            seg_span = 360.0/segments

            rx = (i-2) * 0.6
            ry = rx * 1
            deg0 = s * seg_span
            washBrush()
            pickUpColor(next(color_gen))
            x, y = ovalPos(xo,yo, rx,ry, deg0)
            ad.moveto(x,y)
            ad.pendown()
            ad.penup()
        continue

        for s in range(segments):
            seg_span = 360.0/segments

            rx = (i-2) * 0.6
            ry = rx * 1
            deg0 = s * seg_span
            deg1 = deg0 + seg_span

            deg0 -= 10
            deg1 += 10
            washBrush(ditch_excess=True)
            ovalSegment(xo,yo,rx,ry,deg0,deg1)
            ovalSegment(xo,yo,rx,ry,     deg1,deg0)
            ovalSegment(xo,yo,rx,ry,deg0,deg1)

            # x0, y0 = ovalPos(xo,yo, rx,ry, deg0)
            # ad.moveto(x0,y0)
            # x1, y1 = ovalPos(xo,yo, rx,ry, deg1)
            # ad.lineto(x1,y1)
            # ad.lineto(x0,y0)
            # ad.lineto(x1,y1)
            # ad.penup()

        washBrush(ditch_excess=False)
        for s in range(72):
            seg_span = 5

            rx = (i-2) * 0.6
            ry = rx * 1
            deg0 = s * seg_span
            deg1 = deg0 + seg_span

            if s == 0:
                x0, y0 = ovalPos(xo,yo, rx,ry, deg0)
                ad.moveto(x0,y0)
            x1, y1 = ovalPos(xo,yo, rx,ry, deg1)
            ad.lineto(x1,y1)
        ad.penup()


def ovalExpWash():
    xo=20
    yo=8
    for i in range(3,11):
        segments = 7
        washBrush(ditch_excess=False)
        for s in range(segments):
            seg_span = 360.0/segments

            rx = (i-2) * 0.75
            ry = rx * 1 # 0.618
            deg0 = s * seg_span
            deg0 += (i-3)*(720.0/81.0)
            deg1 = deg0 + seg_span

            if s == 0:
                x0, y0 = ovalPos(xo,yo, rx,ry, deg0)
                ad.moveto(x0,y0)
            x1, y1 = ovalPos(xo,yo, rx,ry, deg1)
            ad.lineto(x1,y1)
            # for w in range(1):
            #     ovalSegment(xo,yo, rx,ry, deg0,deg1, straight=True)
            #     ovalSegment(xo,yo, rx,ry, deg1,deg0, straight=True)
        ad.penup()



def washDirty():
    ad.moveto(0,20);
    for i in range(2):
        ad.line(1,0)
        ad.line(-1,0)
    ad.line(1,0)
    time.sleep(0.5)
    ad.penup()

def washClean():
    ad.moveto(5,20);
    for i in range(2):
        ad.line(1,0)
        ad.line(-1,0)
    ad.line(1,0)
    time.sleep(0.5)
    ad.penup()

def dabSponge():
    ad.moveto(3,20)
    ad.pendown()
    time.sleep(0.5)
    ad.penup()
def dabSpongeQuick():
    ad.moveto(3,20)
    ad.pendown()
    ad.penup()
    ad.moveto(5,20);
    ad.pendown()
    ad.penup()

def washBrush(ditch_excess=False):
    washDirty()
    # dabSponge()
    washClean()
    if ditch_excess:
        ad.moveto(3,22)
        ad.moveto(3,20)
    # washClean()






# flower()

# for i in range(7):
#     dabLines(i/2.0)

# interact()
# ovalExp()




def cleanPaintCircleRandStart(xo,yo, rx,ry):
    deg_step = 5
    phase = random.randint(0,359)
    for s in range(int((360*2+15)/deg_step)):
        deg0 = s * deg_step + phase
        deg1 = deg0 + deg_step
        if s == 0:
            x, y = ovalPos(xo,yo, rx,ry, deg0)
            ad.moveto(x,y)
        x, y = ovalPos(xo,yo, rx,ry, deg1)
        ad.lineto(x,y)
    ad.penup()

def dabOnCircle(deg, xo,yo, rx,ry):
    x, y = ovalPos(xo,yo, rx,ry, deg)
    ad.moveto(x,y)
    ad.pendown()
    x, y = ovalPos(xo,yo, rx,ry, deg+5)
    ad.moveto(x,y)
    ad.penup()

def randCircle(xo,yo,phase,colors):
    # xo += random.randint(-5,5)
    # yo += random.randint(-7,7)
    secondColor = WHITE# if (x+y)>28 else BLACK
    print("xo: {}, yo: {}".format(xo,yo))
    color_gen = randColorGen()

    rx = 0.8
    ry = 0.8
    washBrush(ditch_excess=False)
    cleanPaintCircleRandStart(xo,yo, rx,ry)

    num_dots = len(colors)
    # phase = 45 if (xo+yo)>28 else 180+45 #random.randint(0,359)
    for s in range(num_dots):
        if s>0: 
            washBrush()
        deg_step = 360.0/num_dots
        deg = s * deg_step + phase
        color = colors[s]
        pickUpColor(color)
        dabOnCircle(deg, xo,yo, rx,ry)

def randCircles():
    xo=21.5
    yo=8
    max_radius = 7
    max_closeness = 2.25
    num_circles = 21
    positions = []
    for i in range(100000):
        theta_rad = random.uniform(0,2*math.pi)
        dist = random.uniform(0,max_radius)
        x = xo + dist * math.cos(theta_rad)
        y = yo + dist * math.sin(theta_rad)
        overlaps = False
        for existing_pos in positions:
            dist_to_existing_pos = math.sqrt((x-existing_pos[0])**2 + (y-existing_pos[1])**2)
            if dist_to_existing_pos < max_closeness:
                print('skipping:')
                print(existing_pos)
                print(dist_to_existing_pos)
                overlaps = True
                break
        if overlaps:
            continue
        theta_deg = 180 * theta_rad / math.pi
        print("saving:")
        print((x,y, theta_deg))
        positions.append((x,y,theta_deg))
        if len(positions) >= num_circles:
            break;
    return positions

def fibCircles(xo,yo,scale=1.3):
    max_radius = 7.7
    max_closeness = 2.0
    num_circles = 21
    positions = []
    for i in range(100000):
        index = i + 0.5
        theta_rad = index * 2 * math.pi * 0.61803399
        dist = math.sqrt(index) * scale
        if dist > max_radius:
            break
        x = xo + dist * math.cos(theta_rad)
        y = yo + dist * math.sin(theta_rad)
        overlaps = False
        for existing_pos in positions:
            dist_to_existing_pos = math.sqrt((x-existing_pos[0])**2 + (y-existing_pos[1])**2)
            if dist_to_existing_pos < max_closeness:
                print('skipping as pos is too close {}'.format(dist_to_existing_pos))
                overlaps = True
                break
        if overlaps:
            return None
        theta_deg = 180 * theta_rad / math.pi
        print("saving:")
        print((x,y, theta_deg))
        positions.append((x,y,theta_deg))
    return positions



def drawCirclePositions(positions,colors):
    print("drawing {} positions:".format(len(positions)))
    print(positions)
    count = 0
    for position in positions:
        count += 1
        print("drawing {} of {}".format(count, len(positions)))
        print(position)
        randCircle(position[0], position[1], position[2] + 180, colors)#[WHITE,HOT_PINK])#[NICE_BLUE, TURQUOISE])


def drawNiceCircleComposition():
    xo=21.5
    yo=8
    positions = fibCircles(xo,yo,1.3)
    positions = [x for x in reversed(positions)]
    # inner_color=HOT_PINK
    # outer_color=NICE_BLUE
    # colors = [outer_color,inner_color]
    colors = [GREEN]
    drawCirclePositions(positions, colors)

drawNiceCircleComposition()

# interact()
# for i in range(20):
#     print (i)
#     randCircle()

washBrush()


ad.moveto(0,0)
ad.disconnect()






























