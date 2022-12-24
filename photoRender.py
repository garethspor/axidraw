import argparse
import math
import numpy as np
from PIL import Image, ImageFile
import matplotlib.pyplot as plt
from scipy import signal
from scipy import misc
from pyaxidraw import axidraw
import sys
import time

def loadImage(filename):
	with Image.open(filename) as im:
		imlayer = im.split()[0]
		imarray = np.array(imlayer.getdata()).reshape(imlayer.size[1], imlayer.size[0]).astype(float) / 255.0
		ksize = 32
		imarray = signal.convolve2d(imarray, np.ones((ksize,ksize))) / (ksize*ksize)
		return imarray


parser = argparse.ArgumentParser(description='make a spiral svg image')
parser.add_argument('image', help='photo to load')
args = parser.parse_args()

im = loadImage(args.image)
print(im)
print(im.shape)
plt.imshow(im)
plt.show()


ad = axidraw.AxiDraw()
ad.interactive()
connected = ad.connect()
if not connected:
	print("No robot :-(")
	# sys.exit()

ad.options.units = 1
ad.options.speed_penup = 100
ad.options.pen_pos_up = 50
ad.options.pen_pos_down = 20
ad.update()
ad.penup()
ad.moveto(0,0)

max_pause_seconds = 6.0

maxx = 0
maxy = 0
maxv = 0
minx = 1000000
miny = 1000000
minv = 1000000
numdots = 0

def drawDot(x,y,v):
	print("x: {}, y: {}, v: {}".format(x,y,v))
	if connected:
		ad.moveto(x,y)
		ad.pendown()
		pause = ((1.0 - v) ** 2) * max_pause_seconds
		time.sleep(pause)
		ad.penup()


# index = 0
theta = 0
goldenRatio = 1.61803399
sampleMag = im.shape[1] / 120

centerx = 10
centery = 10
shrink = 0.2

numdots = 618 * 4
for findex in range(numdots):
# while index < 618*4:
	index = (numdots-1) - findex
	theta = goldenRatio * 2.0 * math.pi * index
	amp = math.sqrt(index)
	x = math.cos(theta) * amp
	y = math.sin(theta) * amp
	samplex = int(im.shape[1] / 2 + (x * sampleMag))
	sampley = int(im.shape[0] / 2 + (y * sampleMag))

	# theta += goldenRatio * 2.0 * math.pi
	# index += 1
	print("index: {}".format(index))

	if samplex < 0 or samplex >= im.shape[1] or sampley < 0 or sampley >= im.shape[0]:
		continue

	value = im[sampley,samplex]

	# value = 1.0 if x > 0 else 0.0
	# if y > 0:
	# 	value = 0.5

	dotx = centerx + x * shrink
	doty = centery + y * shrink
	drawDot(dotx,doty,value)

	# numdots += 1
	maxx = max(dotx,maxx)
	maxy = max(doty,maxy)
	minx = min(dotx,minx)
	miny = min(doty,miny)
	maxv = max(value,maxv)
	minv = min(value,minv)

ad.moveto(0,0)

print("numdots: {}".format(numdots))
print("x: {} - {}".format(minx,maxx))
print("y: {} - {}".format(miny,maxy))
print("v: {} - {}".format(minv,maxv))


