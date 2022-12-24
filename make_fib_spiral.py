import argparse
import math
import numpy as np

HEADER = """<svg id="svg_css_ex1" viewBox="0 0 10 10" 
   height="28cm"
   width="28cm"
   xmlns="http://www.w3.org/2000/svg">
  <rect 
    fill="none"
    stroke="black"
    stroke-width="0.05"
		width="9.70820394" height="6" />
"""
SPIRALHEADER = """<path
    fill="none"
    stroke="black"
    stroke-width="0.05"
    d="
"""

FOOTER = """    " />
</svg>
"""

def MakeSVG():
	spiralArcs = ''
	numSteps = 16
	x = 0
	y = 0
	s = 6
	gr = 0.61803399
	vx = 1
	vy = 1
	spiralArcs += 'M 0 0\n'
	lines = ''
	for i in range(numSteps):
		dx = s * vx
		dy = s * vy
		spiralArcs += 'a {rx} {ry} {angle} {large_arc_flag} {sweep_flag} {dx} {dy}\n'.format(rx=s, ry=s, angle=0, large_arc_flag=0, sweep_flag=0, dx=dx, dy=dy)
		linex1 = x
		liney1 = y
		if i % 4 == 0:
			linex1 += s
		elif i % 4 == 1:
			liney1 -= s
		elif i % 4 == 2:
			linex1 -= s
		elif i % 4 == 3:
			liney1 += s
		lines += '  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="black" stroke-width="0.05" />\n'.format(x1=linex1, y1=liney1, x2=x+dx, y2=y+dy)
		x += dx
		y += dy
		s *= gr
		nvx = vy
		nvy = -vx
		vx = nvx
		vy = nvy
	return HEADER + lines + SPIRALHEADER + spiralArcs + FOOTER




parser = argparse.ArgumentParser(description='make a spiral svg image')
parser.add_argument('out', help='path to save to')
args = parser.parse_args()

with open(args.out, 'w') as fileobj:
	fileobj.write(MakeSVG())
