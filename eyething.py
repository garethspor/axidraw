import argparse
import math
import numpy as np

SVGHEADER = """<svg id="svg_css_ex1" viewBox="0 0 10 10" 
   height="20cm"
   width="20cm"
   xmlns="http://www.w3.org/2000/svg">
"""

PATHHEADER = """  <path
    fill="none"
    stroke="black"
    stroke-width="0.01"
    d="
"""

SVGFOOTER = """</svg>
"""

def MakeLine(x0,y0,x1,y1):
	return(x0,y0,x1,y1)

def MakeLineCommand(l):
	x0 = l[0]
	y0 = l[1]
	x1 = l[2]
	y1 = l[3]
	return 'l {dx} {dy}\n'.format(dx=x1-x0, dy=y1-y0)

def MakeArc(x0, y0, rx, ry, angle, large_arc_flag, sweep_flag, dx, dy):
	return (x0, y0, rx, ry, angle, large_arc_flag, sweep_flag, dx, dy)

def ReverseArc(arc):
	x1 = arc[0] + arc[8]
	y1 = arc[0] + arc[8]
	return MakeArc(x1, y1, arc[2], arc[3], arc[4], arc[5], 1-arc[6], -arc[7], -arc[8])

def Make1stArcMoveCommand(arc):
	x0 = arc[0] + 5
	y0 = arc[1] + 5
	return 'M {x} {y}\n'.format(x=x0, y=y0)

def MakeArcCommand(arc):
	return 'a {rx} {ry} {angle} {large_arc_flag} {sweep_flag} {dx} {dy}\n'.format(rx=arc[2], ry=arc[3], angle=arc[4], large_arc_flag=arc[5], sweep_flag=arc[6], dx=arc[7], dy=arc[8])

def MakePathFromArcs(arcs):
	return PATHHEADER + Make1stArcMoveCommand(arcs[0]) + ''.join([MakeArcCommand(a) for a in arcs]) + '"/>\n'

def MakePathFromLines(lines):
	return PATHHEADER + Make1stArcMoveCommand(lines[0]) + ''.join([MakeLineCommand(l) for l in lines]) + '"/>\n'

def MakeEyeThingPath(x,y):
	lines = []
	numIters = 8
	for i in range(numIters):
		x0 = x
		y0 = y
		scale = 0.618
		x *= scale
		x1 = x
		y1 = y
		y *= scale
		x2 = x
		y2 = y
		lines.append(MakeLine(x0,y0,x1,y1))
		lines.append(MakeLine(x1,y1,x2,y2))
	return MakePathFromLines(lines)


def MakeSVG():
	svg = SVGHEADER
	# numPoints = 72 * 2
	thetaStep = 2
	for theta in range(0, 360, int(thetaStep)):
		theta += thetaStep / 2
		thetaRad = math.pi * theta / 180
		x = math.cos(thetaRad) * 5
		y = math.sin(thetaRad) * 5
		svg += MakeEyeThingPath(x,y)
	svg += SVGFOOTER
	return svg




parser = argparse.ArgumentParser(description='make a spiral svg image')
parser.add_argument('out', help='path to save to')
args = parser.parse_args()

with open(args.out, 'w') as fileobj:
	fileobj.write(MakeSVG())
