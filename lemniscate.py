import argparse
import math
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

def MakeLineCommand(l):
	dx = l[0]
	dy = l[1]
	return 'l {dx} {dy}\n'.format(dx=dx, dy=dy)

def MakeArc(x0, y0, rx, ry, angle, large_arc_flag, sweep_flag, dx, dy):
	return (x0, y0, rx, ry, angle, large_arc_flag, sweep_flag, dx, dy)

def ReverseArc(arc):
	x1 = arc[0] + arc[8]
	y1 = arc[0] + arc[8]
	return MakeArc(x1, y1, arc[2], arc[3], arc[4], arc[5], 1-arc[6], -arc[7], -arc[8])

def Make1stArcMoveCommand(arc):
	return 'M {x} {y}\n'.format(x=arc[0], y=arc[1])

def MakeArcCommand(arc):
	return 'a {rx} {ry} {angle} {large_arc_flag} {sweep_flag} {dx} {dy}\n'.format(rx=arc[2], ry=arc[3], angle=arc[4], large_arc_flag=arc[5], sweep_flag=arc[6], dx=arc[7], dy=arc[8])

def MakePath(arcs):
	return PATHHEADER + Make1stArcMoveCommand(arcs[0]) + ''.join([MakeArcCommand(a) for a in arcs]) + '"/>\n'

def MakeSVG():
	svg = SVGHEADER
	svg += PATHHEADER

	xstep = 0.5
	yoffset = 5
	x = 5
	y = 30
	bmag = 2

	svg += Make1stArcMoveCommand((x,y-yoffset))

	# for i in range(200):
	while x < 90:
		x0 = x
		y0 = y - yoffset
		x1 = x + xstep / 2
		y1 = y + yoffset
		bx0 = x - bmag
		bx1 = x1 + bmag
		svg += 'C {},{} {},{} {},{}'.format(bx0,y0,bx1,y1,x1,y1)
		x2 = x + xstep
		y2 = y - yoffset
		bx1 = x1 - bmag
		bx2 = x2 + bmag
		svg += 'C {},{} {},{} {},{}'.format(bx1,y1,bx2,y2,x2,y2)
		x = x2

	svg += PATHFOOTER
	svg += SVGFOOTER
	return svg

def MakeVeryCoolThing():
	svg = SVGHEADER
	svg += PATHHEADER

	xstep = 0.5
	yoffset = 5
	x = 1
	y = 50
	bmag = 0.5

	yoffset = 50 - abs(50-x)
	svg += Make1stArcMoveCommand((x,y-yoffset))

	while x < 99:
		yoffset = 50 - abs(50-x)
		bmag = yoffset * 0.4

		x0 = x
		x1 = x + xstep / 2
		y0 = y - yoffset
		y1 = y + yoffset
		bx0 = x - bmag
		bx1 = x1 + bmag
		svg += 'C {},{} {},{} {},{}'.format(bx0,y0,bx1,y1,x1,y1)
		x2 = x + xstep
		y2 = y - yoffset
		bx1 = x1 - bmag
		bx2 = x2 + bmag
		svg += 'C {},{} {},{} {},{}'.format(bx1,y1,bx2,y2,x2,y2)
		x = x2

		# yoffset -= 0.3

	svg += PATHFOOTER
	svg += SVGFOOTER
	return svg

def MakeTreeSVG():
	svg = SVGHEADER
	svg += PATHHEADER

	xstep = 7
	yoffset = 5
	x = 1
	y = 50
	bmag = 0.5

	yoffset = 20 if x < 20 else (100 - x)*0.61803399
	svg += Make1stArcMoveCommand((x,y-yoffset))

	while x < 99:
		yoffset = 10 if x < 20 else (100 - x)*0.61803399
		bmag = yoffset * 0.4

		x0 = x
		x1 = x + xstep / 2
		y0 = y - yoffset
		y1 = y + yoffset
		bx0 = x - bmag
		bx1 = x1 + bmag
		svg += 'C {},{} {},{} {},{}'.format(bx0,y0,bx1,y1,x1,y1)
		x2 = x + xstep
		y2 = y - yoffset
		bx1 = x1 - bmag
		bx2 = x2 + bmag
		svg += 'C {},{} {},{} {},{}'.format(bx1,y1,bx2,y2,x2,y2)
		x = x2

		# yoffset -= 0.3

	svg += PATHFOOTER
	svg += SVGFOOTER
	return svg

def ExperimentA():
	svg = SVGHEADER
	svg += PATHHEADER

	points = []
	thetaStep = 5
	for theta in np.arange(0,180.0, thetaStep):
		thetaRad = math.pi * theta / 180.0
		x = math.cos(thetaRad)
		y = math.sin(thetaRad)
		points.append((x,y))

		theta += thetaStep / 2
		theta *= -1

		thetaRad = math.pi * theta / 180.0
		x = math.cos(thetaRad)
		y = math.sin(thetaRad)
		points.append((x,y))

	scale = 5
	xOrigin = 50
	yOrigin = 50

	bezScale = .2

	bezAPoints = [(x+y*bezScale*abs(y),y-x*bezScale*abs(y)) for x,y in points]
	bezBPoints = [(x-y*bezScale*abs(y),y+x*bezScale*abs(y)) for x,y in points]


	ScaledPoints = [(x*scale+xOrigin,y*scale+yOrigin) for x,y in points]
	bezAPoints = [(x*scale+xOrigin,y*scale+yOrigin) for x,y in bezAPoints]
	bezBPoints = [(x*scale+xOrigin,y*scale+yOrigin) for x,y in bezBPoints]

	svg += Make1stArcMoveCommand(ScaledPoints[0])
	for i in range(len(ScaledPoints) - 1):
		x0,y0 = ScaledPoints[i]
		x1,y1 = ScaledPoints[i + 1]
		ox0,oy0 = points[i] 
		ox1,oy1 = points[i + 1] 
		bx0,by0 = bezAPoints[i]     if oy0 > 0 else bezBPoints[i]
		bx1,by1 = bezBPoints[i + 1] if oy1 > 0 else bezAPoints[i + 1]
		svg += 'C {},{} {},{} {},{}\n'.format(bx0,by0,bx1,by1,x1,y1)

	svg += PATHFOOTER
	svg += SVGFOOTER
	return svg



parser = argparse.ArgumentParser(description='make a spiral svg image')
parser.add_argument('out', help='path to save to')
args = parser.parse_args()

with open(args.out, 'w') as fileobj:
	fileobj.write(ExperimentA())
