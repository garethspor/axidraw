import argparse
import math
import numpy as np

SVGHEADER = """<svg id="svg_css_ex1" viewBox="0 0 200 200" 
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

	order = 20
	center_x = 100
	center_y = 61

	svg += PATHHEADER

	north_edge_y = center_y - order
	south_edge_y = center_y + order
	west_edge_x = center_x - order
	east_edge_x = center_x + order
	finish_x = center_x + 0.5
	entrance_x = center_x - 0.5

	# start at bottom edge, aligned with the entrace
	x = entrance_x
	y = 0

	# pointed up
	vx = 0
	vy = 1

	svg += Make1stArcMoveCommand((x,y))

	y = north_edge_y
	svg += MakeLineCommand((0,north_edge_y))

	while True:
		if y == north_edge_y and vy > 0:
			x_dist_to_corner = west_edge_x - x if x < center_x else east_edge_x - x
			dx = x_dist_to_corner
			dy = abs(x_dist_to_corner)
			r = abs(x_dist_to_corner)
			sweep_flag = 1 if dx < 0 else 0
			svg += MakeArcCommand(MakeArc(x,y, rx=r, ry=r, angle=0, large_arc_flag=0, sweep_flag=sweep_flag, dx=dx, dy=dy))
			x += dx
			y += dy
			vx = 1 if dx > 0 else -1
			vy = 0
		elif x == west_edge_x and vx < 0:
			y_dist_to_sw_corner = south_edge_y - y
			dx = -y_dist_to_sw_corner
			dy = y_dist_to_sw_corner
			svg += MakeArcCommand(MakeArc(x,y, rx=y_dist_to_sw_corner, ry=y_dist_to_sw_corner, angle=0, large_arc_flag=0, sweep_flag=0, dx=dx, dy=dy))
			x += dx
			y += dy
			vx = 0
			vy = 1
		elif y == south_edge_y and vy > 0:
			if x == finish_x:
				break
			x_dist_to_finish = finish_x - x
			dx = 2 * x_dist_to_finish
			dy = 0
			sweep_flag = 1 if dx < 0 else 0
			svg += MakeArcCommand(MakeArc(x,y, rx=x_dist_to_finish, ry=x_dist_to_finish, angle=0, large_arc_flag=0, sweep_flag=sweep_flag, dx=dx, dy=dy))
			x += dx
			y += dy
			vx = 0
			vy = -1
		elif y == south_edge_y and vy < 0:
			x_dist_to_corner = west_edge_x - x if x < center_x else east_edge_x - x
			dx = x_dist_to_corner
			dy = -abs(x_dist_to_corner)
			sweep_flag = 1 if dx > 0 else 0
			r = abs(x_dist_to_corner)
			svg += MakeArcCommand(MakeArc(x,y, rx=r, ry=r, angle=0, large_arc_flag=0, sweep_flag=sweep_flag, dx=dx, dy=dy))
			x += dx
			y += dy
			vx = 1 if dx > 0 else -1
			vy = 0
		elif x == east_edge_x and vx < 0:
			y_dist_to_corner = south_edge_y - y if y > center_y else north_edge_y - y
			dx = -abs(y_dist_to_corner)
			dy = y_dist_to_corner
			sweep_flag = 1 if dy < 0 else 0
			r = abs(y_dist_to_corner)
			svg += MakeArcCommand(MakeArc(x,y, rx=r, ry=r, angle=0, large_arc_flag=0, sweep_flag=sweep_flag, dx=dx, dy=dy))
			x += dx
			y += dy
			vx = 0
			vy = 1 if dy > 0 else -1
		elif x == east_edge_x and vx > 0:
			y_dist_to_corner = south_edge_y - y
			dx = abs(y_dist_to_corner)
			dy = abs(y_dist_to_corner)
			sweep_flag = 1
			r = abs(y_dist_to_corner)
			svg += MakeArcCommand(MakeArc(x,y, rx=r, ry=r, angle=0, large_arc_flag=0, sweep_flag=sweep_flag, dx=dx, dy=dy))
			x += dx
			y += dy
			vx = 0
			vy = 1
		elif x == west_edge_x and vx > 0:
			y_dist_to_corner = south_edge_y - y if y > center_y else north_edge_y - y
			dx = abs(y_dist_to_corner)
			dy = y_dist_to_corner
			sweep_flag = 1 if dy > 0 else 0
			r = abs(y_dist_to_corner)
			svg += MakeArcCommand(MakeArc(x,y, rx=r, ry=r, angle=0, large_arc_flag=0, sweep_flag=sweep_flag, dx=dx, dy=dy))
			x += dx
			y += dy
			vx = 0
			vy = 1 if dy > 0 else -1
		elif y == north_edge_y and vy < 0:
			x_dist_to_corner = west_edge_x - x if x < center_x else east_edge_x - x
			dx = x_dist_to_corner
			dy = -abs(x_dist_to_corner)
			r = abs(x_dist_to_corner)
			sweep_flag = 1 if dx > 0 else 0
			svg += MakeArcCommand(MakeArc(x,y, rx=r, ry=r, angle=0, large_arc_flag=0, sweep_flag=sweep_flag, dx=dx, dy=dy))
			x += dx
			y += dy
			vx = 1 if dx > 0 else -1
			vy = 0
		else:
			break


	svg += PATHFOOTER
	svg += SVGFOOTER
	# arcs = [MakeArc(0,0,5,5,0,0,1,5,5), MakeArc(5,5,5,5,0,0,0,5,5)]
	# rarcs = [ReverseArc(a) for a in reversed(arcs)]
	# return SVGHEADER + MakePath(rarcs) + SVGFOOTER
	return svg



parser = argparse.ArgumentParser(description='make a spiral svg image')
parser.add_argument('out', help='path to save to')
args = parser.parse_args()

with open(args.out, 'w') as fileobj:
	fileobj.write(MakeSVG())
