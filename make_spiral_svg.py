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
    stroke-width="0.05"
    d="
"""

FOOTER = """    " />
</svg>
"""

def MakeSVG():
	commands = ''
	theta0 = 0.0
	theta1 = 360.0 * 30
	thetaStep = 30.0
	r0 = 0.0
	r1 = 5.0
	originX = 5.0
	originY = 5.0
	prevx = 0
	prevy = 0
	prevradius = 0
	for theta in np.arange(theta0, theta1, thetaStep):
		thetaRad = math.pi * theta / 180.0
		frac = (theta - theta0) / (theta1 - theta0)
		radius = frac * (r1 - r0) + r0
		x = originX + math.cos(thetaRad) * radius
		y = originY - math.sin(thetaRad) * radius
		if theta == theta0:
			commands += 'M {x} {y}\n'.format(x=x, y=y)
		else:
			dx = x - prevx
			dy = y - prevy
			midradius = (prevradius + radius) / 2
			commands += 'a {rx} {ry} {angle} {large_arc_flag} {sweep_flag} {dx} {dy}\n'.format(rx=midradius, ry=radius, angle=0, large_arc_flag=0, sweep_flag=0, dx=dx, dy=dy)
		prevx = x
		prevy = y
		prevradius = radius
	return HEADER + commands + FOOTER




parser = argparse.ArgumentParser(description='make a spiral svg image')
parser.add_argument('out', help='path to save to')
args = parser.parse_args()

with open(args.out, 'w') as fileobj:
	fileobj.write(MakeSVG())
