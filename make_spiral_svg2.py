import argparse
import math
import numpy as np

HEADER = """<svg id="svg_css_ex1" viewBox="0 0 10 10" 
   height="10cm"
   width="10cm"
   xmlns="http://www.w3.org/2000/svg">
  <path
    fill="none"
    stroke="black"
    stroke-width="0.01"
    d="
"""

FOOTER = """    " />
</svg>
"""

def loop(originX,originY,r0,r1,theta0,theta1, isfirst=False):
	commands = ''
	thetaStep = (1.0 if theta1 > theta0 else -1) * 90
	sweep_flag = 0 if theta1 > theta0 else 1
	prevx = 0
	prevy = 0
	prevradius = 0
	for theta in np.arange(theta0, theta1+thetaStep, thetaStep):
		thetaRad = math.pi * theta / 180.0
		frac = (theta - theta0) / (theta1 - theta0)
		radius = frac * (r1 - r0) + r0
		x = originX + math.cos(thetaRad) * radius
		y = originY - math.sin(thetaRad) * radius
		# print("frac: {}, radius: {}".format(frac, radius))
		if theta == theta0:
			if isfirst:
				commands += 'M {x} {y}\n'.format(x=x, y=y)
		else:
			dx = x - prevx
			dy = y - prevy
			midradius = (prevradius + radius) / 2
			commands += 'a {rx} {ry} {angle} {large_arc_flag} {sweep_flag} {dx} {dy}\n'.format(rx=midradius, ry=midradius, angle=0, large_arc_flag=0, sweep_flag=sweep_flag, dx=dx, dy=dy)
		prevx = x
		prevy = y
		prevradius = radius
	return commands


def MakeSVG():
	commands = ''
	isfirst = True
	radStep = 0.04
	radMin = 0.4
	radMax = 1.6
	for rad in np.arange(radMin, radMax-radStep, radStep):
		r0 = rad
		r1 = rad + radStep/2
		r2 = 2 - r1
		r3 = r2 - radStep/2
		commands += loop(4,5, r0, r1,   0, 360, isfirst=isfirst)
		commands += loop(6,5, r2, r3, 540, 180)
		isfirst = False
	# commands += loop(4,5, 1.0, 1.5,   0, 360)
	# commands += loop(6,5, 0.5, 0.0, 540, 180)
	# commands += loop(6,5, 1.5, 1.0, 180)
	# commands += loop(4,5, 1.0, 1.5,   0)
	# commands += loop(6,5, 0.5, 0.0, 180)
	return HEADER + commands + FOOTER




parser = argparse.ArgumentParser(description='make a spiral svg image')
parser.add_argument('out', help='path to save to')
args = parser.parse_args()

with open(args.out, 'w') as fileobj:
	fileobj.write(MakeSVG())
