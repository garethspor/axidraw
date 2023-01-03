import argparse
import math
import numpy as np

HEADER_NO_RECT = """<svg id="svg_css_ex1" viewBox="0 0 10 10" 
   height="7cm"
   width="7cm"
   xmlns="http://www.w3.org/2000/svg">
"""
CIRCLE = """  <circle
    fill="none"
    stroke="black"
    stroke-width="0.05"
		cx="5" cy="5" r="4" />
"""

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

G = 1.61803399

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

def pythag_dist(x0,y0,x1,y1):
	return math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)

def MakeSVG22(scale):
	origin_x = 5
	origin_y = 5
	max_radius = 4
	min_size_to_draw = .02
	numSteps = 20

	spiralArcs = ''
	
	x = origin_x
	y = origin_y
	s = .001 * scale
	vx = 0
	vy = 1
	spiral_started = False
	spiralArcs += 'M {} {}\n'.format(x,y)
	lines = ''
	for i in range(numSteps):
		
		radius = s
		dx0 = s * vx
		dy0 = s * vy
		dx1 = s * vy
		dy1 = s * vx * -1
		dx = dx0 + dx1
		dy = dy0 + dy1
		arc_center_x = x + dx1
		arc_center_y = y + dy1
		safe_dx = 0
		safe_dy = 0
		theta1 = math.atan2(vy,vx)
		for d in range(901):
			th = theta1 + 0.1 * d * math.pi / 180
			potential_x = arc_center_x + radius * math.cos(th)
			potential_y = arc_center_y + radius * math.sin(th)
			potential_rad = math.sqrt((potential_x - origin_x) ** 2 + (potential_y - origin_y) ** 2)
			# potential_rad = max(abs(potential_x - origin_x), abs(potential_y - origin_y))
			if potential_rad < max_radius:
				actual_dx = potential_x - x
				actual_dy = potential_y - y
				if s > min_size_to_draw:
					if not spiral_started:
							spiralArcs += 'M {} {}\n'.format(x,y)
							spiral_started = True
					spiralArcs += 'a {rx} {ry} {angle} {large_arc_flag} {sweep_flag} {dx} {dy}\n'.format(rx=radius, ry=radius, angle=0, large_arc_flag=0, sweep_flag=0, dx=actual_dx, dy=actual_dy)
				break


		x += dx
		y += dy
		s *= G

		linex1 = x
		liney1 = y
		linex2 = linex1 - s * vx
		liney2 = liney1 - s * vy
		perp_dist = abs(vy*(x-origin_x) + vx*(y-origin_y))
		if perp_dist <= max_radius:
			max_parallel_dist = math.sqrt(max_radius**2 - perp_dist**2)
			p1_legal = pythag_dist(origin_x, origin_y, linex1, liney1) <= max_radius
			p2_legal = pythag_dist(origin_x, origin_y, linex2, liney2) <= max_radius
			completely_outside = not p1_legal and not p2_legal and (linex1 > origin_x) == (linex2 > origin_x) and (liney1 > origin_y) == (liney2 > origin_y)
			if not completely_outside:
				if not p1_legal:
					linex1 = linex1 * abs(vy) + abs(vx) * (origin_x + vx * max_parallel_dist)
					liney1 = liney1 * abs(vx) + abs(vy) * (origin_y + vy * max_parallel_dist)
				if not p2_legal:
					linex2 = linex2 * abs(vy) + abs(vx) * (origin_x - vx * max_parallel_dist)
					liney2 = liney2 * abs(vx) + abs(vy) * (origin_y - vy * max_parallel_dist)
				if s > min_size_to_draw:
					lines += '  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="black" stroke-width="0.05" />\n'.format(x1=linex1, y1=liney1, x2=linex2, y2=liney2)

		nvx = vy
		nvy = -vx
		vx = nvx
		vy = nvy

	# lines = ''
	return HEADER_NO_RECT + lines + SPIRALHEADER + spiralArcs + FOOTER



parser = argparse.ArgumentParser(description='make a spiral svg image')
parser.add_argument('out', help='path to save to')
args = parser.parse_args()

num_frames = 16
scale0 = 1
scale1 = 1/((2-G)**2)
scale_step = (scale1/scale0) ** (1/num_frames)
for f in range(num_frames):
	scale = scale0 * scale_step**f
	filename = '{}_{:04d}.svg'.format(args.out, f)
	with open(filename, 'w') as fileobj:
		fileobj.write(MakeSVG22(scale))
