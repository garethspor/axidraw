#!/usr/bin/env python3

import argparse
import math
from pyaxidraw import axidraw

G = 1.61803399

FRAME_WIDTH = 14.1
FRAME_HEIGHT = 9

SVG_FILE_HEADER = """<svg id="svg_css_ex1" viewBox="0 0 20 20" 
   height="20cm"
   width="20cm"
   xmlns="http://www.w3.org/2000/svg">
"""
SVG_FILE_FOOTER = """</svg>
"""

SVG_PATH_HEADER = """<path
    fill="none"
    stroke="black"
    stroke-width="0.05"
    d="
"""
SVG_PATH_FOOTER = """    " />
"""

def PythagoreanDistance(x0,y0,x1,y1):
	return math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)

def AbsManhattanDistance(x0,y0,x1,y1):
	return max(abs(x0 - x1), abs(y0 - y1))

def MakeRegistrationMarks(x,y, width, ystep, value, num_bits):
	num_bits += 2
	value <<= 1
	value += 1
	value += 2 << (num_bits - 1)
	svg = ''
	while value:
		if value % 2:
			svg += f'  <line x1="{x - width}" y1="{y}" x2="{x + width}" y2="{y}" stroke="black" stroke-width="0.05" />\n'
		value >>= 1
		y += ystep
	return svg

class BorderRect:
	def __init__(self, loop_length):
		pass
	def GenerateSVG(self, index):
		rect_svg = f'''  <rect x='0' y='0' width='{FRAME_WIDTH}' height='{FRAME_HEIGHT}' stroke="black" stroke-width="0.05" fill="none" />\n'''
		registration_svg = MakeRegistrationMarks(FRAME_WIDTH,1, 0.1, 0.25, index, 8)
		svg = SVG_FILE_HEADER + rect_svg + registration_svg + SVG_FILE_FOOTER
		return svg

class GoldenSpiral:

	def __init__(self, loop_length):
		self.loop_length = loop_length

		self.origin_x = FRAME_HEIGHT / 2
		self.origin_y = self.origin_x
		self.max_radius = self.origin_x * 0.9

		self.min_size_to_draw = .02
		self.numSteps = 20

		self.scale0 = 1e-3
		self.scale1 = self.scale0 / ((2 - G) ** 2)
		self.scale_step = (self.scale1/self.scale0) ** (1/self.loop_length)


	def GenerateSVG(self, index):
		reversed_index = (self.loop_length - 1) - index
		scale = self.scale0 * self.scale_step ** reversed_index

		curve_svg = self._MakeFibbonacciCurve(scale)
		lines_svg = self._MakeFibbonacciLines(scale)
		registration_svg = MakeRegistrationMarks(FRAME_WIDTH,1, 0.1, 0.25, index, 8)
		
		# svg = SVG_FILE_HEADER + lines_svg + registration_svg + SVG_FILE_FOOTER
		svg = SVG_FILE_HEADER + curve_svg + SVG_FILE_FOOTER
		# svg = SVG_FILE_HEADER + curve_svg + lines_svg + registration_svg + SVG_FILE_FOOTER
		return svg

	def _MakeFibbonacciCurve(self, scale):
		spiralArcs = ''
		x = self.origin_x
		y = self.origin_y
		vx = 0
		vy = 1
		spiral_started = False
		spiralArcs += 'M {} {}\n'.format(x,y)
		lines = ''
		for i in range(self.numSteps):
			radius = scale
			dx0 = scale * vx
			dy0 = scale * vy
			dx1 = scale * vy
			dy1 = scale * vx * -1
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
				potential_rad = math.sqrt((potential_x - self.origin_x) ** 2 + (potential_y - self.origin_y) ** 2)
				# potential_rad = max(abs(potential_x - self.origin_x), abs(potential_y - self.origin_y))
				if potential_rad < self.max_radius:
					actual_dx = potential_x - x
					actual_dy = potential_y - y
					if scale > self.min_size_to_draw:
						if not spiral_started:
								spiralArcs += 'M {} {}\n'.format(x,y)
								spiral_started = True
						spiralArcs += 'a {rx} {ry} {angle} {large_arc_flag} {sweep_flag} {dx} {dy}\n'.format(rx=radius, ry=radius, angle=0, large_arc_flag=0, sweep_flag=0, dx=actual_dx, dy=actual_dy)
					break
			x += dx
			y += dy
			scale *= G

			nvx = vy
			nvy = -vx
			vx = nvx
			vy = nvy

		svg = SVG_PATH_HEADER + spiralArcs + SVG_PATH_FOOTER
		return svg

	def _MakeFibbonacciLines(self, scale):
		x = self.origin_x
		y = self.origin_y
		vx = 0
		vy = 1
		svg = ''
		for i in range(self.numSteps):
			dx0 = scale * vx
			dy0 = scale * vy
			dx1 = scale * vy
			dy1 = scale * vx * -1
			dx = dx0 + dx1
			dy = dy0 + dy1
			x += dx
			y += dy
			scale *= G

			linex1 = x
			liney1 = y
			linex2 = linex1 - scale * vx
			liney2 = liney1 - scale * vy
			perpendicular_dist = abs(vy*(x-self.origin_x) + vx*(y-self.origin_y))
			if perpendicular_dist <= self.max_radius:
				max_parallel_dist = math.sqrt(self.max_radius**2 - perpendicular_dist**2)
				p1_legal = PythagoreanDistance(self.origin_x, self.origin_y, linex1, liney1) <= self.max_radius
				p2_legal = PythagoreanDistance(self.origin_x, self.origin_y, linex2, liney2) <= self.max_radius
				completely_outside = not p1_legal and not p2_legal and (linex1 > self.origin_x) == (linex2 > self.origin_x) and (liney1 > self.origin_y) == (liney2 > self.origin_y)
				if not completely_outside:
					if not p1_legal:
						linex1 = linex1 * abs(vy) + abs(vx) * (self.origin_x + vx * max_parallel_dist)
						liney1 = liney1 * abs(vx) + abs(vy) * (self.origin_y + vy * max_parallel_dist)
					if not p2_legal:
						linex2 = linex2 * abs(vy) + abs(vx) * (self.origin_x - vx * max_parallel_dist)
						liney2 = liney2 * abs(vx) + abs(vy) * (self.origin_y - vy * max_parallel_dist)
					if scale > self.min_size_to_draw:
						svg += '  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="black" stroke-width="0.05" />\n'.format(x1=linex1, y1=liney1, x2=linex2, y2=liney2)
			nvx = vy
			nvy = -vx
			vx = nvx
			vy = nvy

		return svg


def GeneratePlotLoopFrameFiles(plot_obj, begin_frame, end_frame, out_path):
	for i in range(begin_frame, end_frame):
		print(f'GeneratePlotLoopFrameFiles - Frame {i} of [{begin_frame}->{end_frame})')
		svg = plot_obj.GenerateSVG(i)
		filename = f'{out_path}{i:04d}.svg'
		with open(filename, 'w') as fileobj:
			print(f'Writing: {filename}')
			fileobj.write(svg)

def DrawPlotLoopOnAxiDraw(plot_obj, begin_frame, end_frame, ad):
	index = begin_frame
	while index < end_frame:
		user_input = input(f'Hit enter to draw Frame {index} of [{begin_frame}->{end_frame}): ')
		if not user_input:
			pass
		elif user_input == 'q':
			return
		elif user_input == 'n':
			index = int(input('Enter new frame number to draw instead: '))
			continue

		svg = plot_obj.GenerateSVG(index)
		ad.plot_setup(svg)
		ad.plot_run()
		index += 1


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Make a plot loop')
	parser.add_argument('--outpath', '-o', help='path to folder+base name')
	parser.add_argument('--classname', '-c', default='GoldenSpiral', help='classname of plot')
	parser.add_argument('--beginframe', '-b', type=int, default=0, help='index of first frame to plot')
	parser.add_argument('--endframe', '-e', type=int, default=-1, help='index of last frame to plot')
	parser.add_argument('--looplength', '-l', type=int, default=8, help='number of frames in total loop')
	parser.add_argument('--axiplot', '-a', help='plot frames on axiplot', action='store_true')

	args = parser.parse_args()

	plot_obj = {'GoldenSpiral' : GoldenSpiral,
				'BorderRect' : BorderRect,
				}[args.classname](args.looplength)

	endframe = args.looplength if args.endframe == -1 else args.endframe+1

	if args.outpath:
		GeneratePlotLoopFrameFiles(plot_obj, args.beginframe, endframe, args.outpath)

	if args.axiplot:
		ad = axidraw.AxiDraw()
		ad.interactive()
		ad.connect()
		# if ad.options and ad.connect():
		ad.options.units = 1
		ad.options.speed_penup = 100
		ad.options.speed_pendown = 25
		ad.options.pen_pos_up = 70
		ad.options.pen_pos_down = 50
		ad.update()
		DrawPlotLoopOnAxiDraw(plot_obj, args.beginframe, endframe, ad)
		# else:
		# 	print('No axidraw :(')
