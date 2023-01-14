#!/usr/bin/env python3

import argparse
import math
from pyaxidraw import axidraw
import socket
import time
import ProjectionMapper
import random

CAM_CONTROL_HOST = "127.0.0.1"  # The server's hostname or IP address
CAM_CONTROL_PORT = 65432  # The port used by the server

G = 1.61803399

# FRAME_WIDTH = 14.1
# FRAME_HEIGHT = 9
FRAME_WIDTH = 8
FRAME_HEIGHT = 5

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

def SvgThinLine(p1,p2, scale=1, x_offset=0, y_offset=0, width=0.05):
   x1 = p1[0] * scale + x_offset
   y1 = p1[1] * scale + y_offset
   x2 = p2[0] * scale + x_offset
   y2 = p2[1] * scale + y_offset
   return f' <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="black" stroke-width="{width}" />\n'

def MakeRegistrationMarks(x,y, width, ystep, value, num_bits):
   num_bits += 2
   value <<= 1
   value += 1
   value += 2 << (num_bits - 1)
   svg = ''
   while value:
      if value % 2:
         svg += SvgThinLine((x - width, y), (x + width, y))
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



CAL_RECT_SCALE = 10
CAL_RECT_OFFSET = 5
class CalibrationRect:
   def __init__(self, loop_length):
      pass
   def GenerateSVG(self, index):
      rect_svg = f'''  <rect x='{CAL_RECT_OFFSET}' y='{CAL_RECT_OFFSET}' width='{CAL_RECT_SCALE}' height='{CAL_RECT_SCALE}' stroke="black" stroke-width="0.05" fill="none" />\n'''
      svg = SVG_FILE_HEADER + rect_svg + SVG_FILE_FOOTER
      return svg



class ProjectionMappedPlay:
   def __init__(self, loop_length):
      self.loop_length = loop_length
      import json
      fileobj = open('projectionMappingCal.json')
      self.cal_data = json.load(fileobj)
      fileobj.close()

   def GenerateSVG(self, index):
      x0 = 0.5
      x1 = 0.75
      y0 = 0.5
      y1 = 0.75
      z0 = 0.000
      z1 = 0.2
      cx = (x0+x1)/2
      cy = (y0+y1)/2
      rad = 1.414*(x1-cx)
      theta = (math.pi / 2) * (float(index) / self.loop_length)
      rsp = []
      for i in range(4):
         x = cx + rad * math.cos(theta)
         y = cy + rad * math.sin(theta)
         rsp.append((x,y))
         theta += math.pi / 2
      p0 = (cx + math.cos(theta))
      cube_points = []
      for z in [z0, z1]:
         for i in range(4):
            cube_points.append((rsp[i][0], rsp[i][1], z))
      # cube_points = [(rsp[0][0],rsp[0][1],z0), (rsp[1][0],rsp[1][1],z0), (x1,y1,z0), (x0,y1,z0), (x0,y0,z1), (x1,y0,z1), (x1,y1,z1), (x0,y1,z1)]
      p = ProjectionMapper.ProjectionMap(self.cal_data['xvals'], self.cal_data['yvals'], cube_points)
      rp = ProjectionMapper.ReverseProjectionMap(self.cal_data['xvals'], self.cal_data['yvals'], p)
      rp = [(p[0]*CAL_RECT_SCALE+CAL_RECT_OFFSET, p[1]*CAL_RECT_SCALE+CAL_RECT_OFFSET) for p in rp]
      cube_svg = ''
      for i in range(4):
          cube_svg += SvgThinLine(rp[i], rp[(i+1)%4])
          cube_svg += SvgThinLine(rp[i+4], rp[(i+1)%4+4])
          cube_svg += SvgThinLine(rp[i], rp[i+4])
      svg = SVG_FILE_HEADER + cube_svg + SVG_FILE_FOOTER
      return svg



class Icosahedron:
   def __init__(self, loop_length):
      self.loop_length = loop_length
      import json
      fileobj = open('projectionMappingCal.json')
      self.cal_data = json.load(fileobj)
      fileobj.close()
      angle_per_loop = 2 * math.pi / 3
      self.theta_step = angle_per_loop / self.loop_length

   def IcosahedronPoints(self, theta):
      points = []
      a = math.sqrt(5./16.)
      h = math.sqrt(G**2 - 0.25)
      th0 = math.atan(h / (2 * a))
      th1 = math.atan(G)
      thx = (th0+th1-math.pi/2)
      wpx = math.sin(thx)
      wpy = math.cos(thx)
      points_pre_rotate = [(-a,0,0), (-a-wpx,0,wpy), (a,0,h), (a+wpx,0,h-wpy)]
      for i in range(3):
         for p in points_pre_rotate:
            x = math.cos(theta) * p[0]
            y = math.sin(theta) * p[0]
            z = p[2]
            x *= 0.22
            y *= 0.22
            z *= 0.22
            x += 0.75
            y += 0.5
            points.append((x,y,z))
         theta += 2 * math.pi / 3
      return points

   def GenerateSVG(self, index):
      theta = self.theta_step * index
      points = self.IcosahedronPoints(theta)
      p = ProjectionMapper.ProjectionMap(self.cal_data['xvals'], self.cal_data['yvals'], points)
      rp = ProjectionMapper.ReverseProjectionMap(self.cal_data['xvals'], self.cal_data['yvals'], p)
      rp = [(p[0]*CAL_RECT_SCALE+CAL_RECT_OFFSET, p[1]*CAL_RECT_SCALE+CAL_RECT_OFFSET) for p in rp]
      icosahedron_svg = ''
      paths = [[0, 4, 8, 0, 11, 4, 3, 8, 7, 0, 1, 6, 2, 10, 6, 9, 2, 5, 10, 1], [10, 11], [4, 5], [2, 3], [8, 9], [6, 7], [1, 11, 5, 3, 9, 7, 1]]
      for path in paths:
         for i in range(len(path)-1):
            icosahedron_svg += SvgThinLine(rp[path[i]], rp[path[i+1]])
      svg = SVG_FILE_HEADER + icosahedron_svg + SVG_FILE_FOOTER
      return svg

class OpaquePolyhedron:
   def __init__(self, loop_length):
      self.loop_length = loop_length
      import json
      fileobj = open('projectionMappingCal.json')
      self.cal_data = json.load(fileobj)
      fileobj.close()

      angle_per_loop = 2 * math.pi / 3
      self.theta_step = angle_per_loop / self.loop_length

   def IcosahedronPoints(self, theta):
      points = []
      a = math.sqrt(5./16.)
      h = math.sqrt(G**2 - 0.25)
      th0 = math.atan(h / (2 * a))
      th1 = math.atan(G)
      thx = (th0+th1-math.pi/2)
      wpx = math.sin(thx)
      wpy = math.cos(thx)
      points_pre_rotate = [(-a,0,0), (-a-wpx,0,wpy), (a,0,h), (a+wpx,0,h-wpy)]
      for i in range(3):
         for p in points_pre_rotate:
            x = math.cos(theta) * p[0]
            y = math.sin(theta) * p[0]
            z = p[2]
            x *= 0.22
            y *= 0.22
            z *= 0.22
            x += 0.75
            y += 0.5
            points.append((x,y,z))
         theta += 2 * math.pi / 3
      return points

   def Icosahedron(self, theta):
      ip = self.IcosahedronPoints(theta)
      tris = [[4, 4, 8]]
      edge_indicies = []

   def GenerateSVG(self, index):
      theta = self.theta_step * index
      points = self.IcosahedronPoints(theta)
      p = ProjectionMapper.ProjectionMap(self.cal_data['xvals'], self.cal_data['yvals'], points)
      rp = ProjectionMapper.ReverseProjectionMap(self.cal_data['xvals'], self.cal_data['yvals'], p)
      rp = [(p[0]*CAL_RECT_SCALE+CAL_RECT_OFFSET, p[1]*CAL_RECT_SCALE+CAL_RECT_OFFSET) for p in rp]
      icosahedron_svg = ''
      paths = [[0, 4, 8, 0, 11, 4, 3, 8, 7, 0, 1, 6, 2, 10, 6, 9, 2, 5, 10, 1], [10, 11], [4, 5], [2, 3], [8, 9], [6, 7], [1, 11, 5, 3, 9, 7, 1]]
      for path in paths:
         for i in range(len(path)-1):
            icosahedron_svg += SvgThinLine(rp[path[i]], rp[path[i+1]])
      svg = SVG_FILE_HEADER + icosahedron_svg + SVG_FILE_FOOTER
      return svg


class MorelletSphereFrame:
   def __init__(self, loop_length):
      self.loop_length = loop_length
      self.theta_step = math.pi * 2 / loop_length
      self.r1 = random.random()
      self.r2 = random.random()

   def _rotate(self, x, y, theta):
      theta += math.atan2(y, x)
      rad = math.sqrt(x**2+y**2)
      x = math.cos(theta) * rad
      y = math.sin(theta) * rad
      return (x, y)

   def _project(self, x, y, z):
      y, z = self._rotate(y, z, math.pi/4)
      theta = self.theta_step * self.index
      tilt = math.pi/128

      theta += self.r1 * 2 * math.pi
      tilt += self.r2 * 2 * math.pi

      x, z = self._rotate(x, z, theta)
      y, z = self._rotate(y, z, tilt)
      
      depth_scale = 1.0 / ((z * 0.01) + 1.0)
      return (depth_scale * x, depth_scale * y)

   def GenerateSVG(self, index):
      self.index = index
      x_offset = 10
      y_offset = 10
      scale = 0.3
      sphere_rad = 28.0
      line_width = 0.001
      sweep = range(-30, 31, 1)
      sphere_svg = ''
      # self.r1 = random.random()
      # self.r2 = random.random()
      for i in range(3):
         for x in sweep:
            if i == 0:
               x += 0.25
            layer_rad_squared = (sphere_rad ** 2) - (x ** 2)
            if layer_rad_squared <= 0:
               continue
            layer_rad = math.sqrt(layer_rad_squared)
            for y in sweep:
               if i == 2:
                  y -= 0.25
               rod_rad_squared = (layer_rad ** 2) - (y ** 2)
               if rod_rad_squared <= 0:
                  continue
               rod_rad = math.sqrt(rod_rad_squared)

               # xo = x; x = y; y = xo
               if i == 0:
                  sphere_svg += SvgThinLine(self._project(x, y, -rod_rad), self._project(x, y, rod_rad), scale=scale, x_offset=x_offset, y_offset=y_offset, width=line_width)
               elif i == 1:
                  sphere_svg += SvgThinLine(self._project(-rod_rad, x, y), self._project(rod_rad, x, y), scale=scale, x_offset=x_offset, y_offset=y_offset, width=line_width)
               elif i == 2:
                  sphere_svg += SvgThinLine(self._project(y, -rod_rad, x), self._project(y, rod_rad, x), scale=scale, x_offset=x_offset, y_offset=y_offset, width=line_width)


      svg = SVG_FILE_HEADER + sphere_svg + SVG_FILE_FOOTER
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
      # svg = SVG_FILE_HEADER + curve_svg + SVG_FILE_FOOTER
      svg = SVG_FILE_HEADER + curve_svg + lines_svg + SVG_FILE_FOOTER
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
                  svg += SvgThinLine((linex1, liney1), (linex2, liney2))
                  # svg += '  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="black" stroke-width="0.05" />\n'.format(x1=linex1, y1=liney1, x2=linex2, y2=liney2)
         nvx = vy
         nvy = -vx
         vx = nvx
         vy = nvy

      return svg


def TriggerCapture():
   with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.connect((CAM_CONTROL_HOST, CAM_CONTROL_PORT))
      s.sendall(b"c")
      response = s.recv(1024).decode("utf-8") 
      print(f"Received: {response} from CameraControl")

def GeneratePlotLoopFrameFiles(plot_obj, begin_frame, end_frame, out_path):
   for i in range(begin_frame, end_frame):
      print(f'GeneratePlotLoopFrameFiles - Frame {i} of [{begin_frame}->{end_frame})')
      svg = plot_obj.GenerateSVG(i)
      filename = f'{out_path}{i:04d}.svg'
      with open(filename, 'w') as fileobj:
         print(f'Writing: {filename}')
         fileobj.write(svg)

def DrawPlotLoopOnAxiDraw(plot_obj, begin_frame, end_frame, ad, controlcamera):
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

      if controlcamera:
         time.sleep(0.5)
         TriggerCapture()

      index += 1


if __name__ == "__main__":
   parser = argparse.ArgumentParser(description='Make a plot loop')
   parser.add_argument('--outpath', '-o', help='path to folder+base name')
   parser.add_argument('--classname', '-c', default='GoldenSpiral', help='classname of plot')
   parser.add_argument('--beginframe', '-b', type=int, default=0, help='index of first frame to plot')
   parser.add_argument('--endframe', '-e', type=int, default=-1, help='index of last frame to plot')
   parser.add_argument('--looplength', '-l', type=int, default=8, help='number of frames in total loop')
   parser.add_argument('--axiplot', '-a', help='plot frames on axiplot', action='store_true')
   parser.add_argument('--controlcamera', help='trigger camera controller to capture frames', action='store_true')

   args = parser.parse_args()

   plot_obj = {
            'GoldenSpiral' : GoldenSpiral,
            'BorderRect' : BorderRect,
            'CalibrationRect' : CalibrationRect,
            'ProjectionMappedPlay' : ProjectionMappedPlay,
            'Icosahedron' : Icosahedron,
            'MorelletSphereFrame' : MorelletSphereFrame,
            'OpaquePolyhedron' : OpaquePolyhedron,
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
      ad.options.pen_pos_up = 75
      ad.options.pen_pos_down = 50
      ad.update()
      DrawPlotLoopOnAxiDraw(plot_obj, args.beginframe, endframe, ad, args.controlcamera)

