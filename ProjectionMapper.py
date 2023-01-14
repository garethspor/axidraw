import cv2
import math
import matplotlib.pyplot as plt
import numpy as np
import time


def GetSlopeIntercept(pointA, pointB):
    rise = pointB[1] - pointA[1]
    run  = pointB[0] - pointA[0]
    if run == 0:
        return 1e100, pointB[0]
    slope = rise / run
    if slope == 0:
        return 0, 0
    intercept = pointA[0] - pointA[1] / slope
    # plt.plot([intercept, pointA[0]], [0, pointA[1]])
    return slope, intercept

def IntersectLines(slopeA, interceptA, slopeB, interceptB):
    y = -(interceptB - interceptA) / ((1 / slopeB) - (1 / slopeA))
    x = y / slopeA + interceptA
    return x,y

def GetIntersection(segmentA, segmentB):
    slopeA, interceptA = GetSlopeIntercept(segmentA[0], segmentA[1])
    slopeB, interceptB = GetSlopeIntercept(segmentB[0], segmentB[1])
    y = -(interceptB - interceptA) / ((1 / slopeB) - (1 / slopeA))
    x = y / slopeA + interceptA
    return x,y


def ReverseProjectionMap(xvals, yvals, points):
    point00 = (xvals[0], yvals[0])
    point10 = (xvals[1], yvals[1])
    point11 = (xvals[2], yvals[2])
    point01 = (xvals[3], yvals[3])
    segmentA = (point00, point10)
    segmentB = (point01, point11)
    vanish_x_inf = GetIntersection(segmentA, segmentB)
    segmentC = (point00, point01)
    segmentD = (point10, point11)
    vanish_y_inf = GetIntersection(segmentC, segmentD)
    slopeA, interceptA = GetSlopeIntercept(segmentA[0], segmentA[1])
    slopeB, interceptB = GetSlopeIntercept(segmentB[0], segmentB[1])
    slopeC, interceptC = GetSlopeIntercept(segmentC[0], segmentC[1])
    slopeD, interceptD = GetSlopeIntercept(segmentD[0], segmentD[1])
    projected_points = []
    for point in points:
        slope_pvx, intercept_y_axis = GetSlopeIntercept(vanish_x_inf, point)
        slope_pvy, intercept_x_axis = GetSlopeIntercept(vanish_y_inf, point)
        px = (intercept_x_axis - interceptC) / (interceptD - interceptC)
        py = (intercept_y_axis - interceptA) / (interceptB - interceptA)
        projected_points.append((px,py))
    return projected_points

def PlotPoints(points, style):
    return plt.plot([p[0] for p in points], [p[1] for p in points], style)

def ProjectionMap(xvals, yvals, points):
    point00 = (xvals[0], yvals[0])
    point10 = (xvals[1], yvals[1])
    point11 = (xvals[2], yvals[2])
    point01 = (xvals[3], yvals[3])
    segmentA = (point00, point10)
    segmentB = (point01, point11)
    vanish_x_inf = GetIntersection(segmentA, segmentB)
    PlotPoints([point00, vanish_x_inf, point01], 'b.-')
    segmentC = (point00, point01)
    segmentD = (point10, point11)
    vanish_y_inf = GetIntersection(segmentC, segmentD)
    PlotPoints([point00, vanish_y_inf, point10], 'g.-')

    vanish_z_inf = (point00[0], point00[1] + 10000) # a guess!
    slopeA, interceptA = GetSlopeIntercept(segmentA[0], segmentA[1])
    slopeB, interceptB = GetSlopeIntercept(segmentB[0], segmentB[1])
    slopeC, interceptC = GetSlopeIntercept(segmentC[0], segmentC[1])
    slopeD, interceptD = GetSlopeIntercept(segmentD[0], segmentD[1])

    z_factor = -1000  # a guess!
    projected_points = []
    for x, y, z in points:
        start_point = point00
        z_point = (start_point[0], start_point[1] + z_factor * z )

        intForX = x * (interceptD - interceptC) + interceptC
        intForY = y * (interceptB - interceptA) + interceptA

        # point with correct y-pos, x & z = 0
        y_point = GetIntersection(segmentC, (vanish_x_inf, (intForY, 0)))
        y_point_up = vanish_z_inf #(y_point[0], y_point[1]-1)

        # point with correct y+z-pos, x = 0
        yz_point = GetIntersection((y_point, y_point_up), (z_point, vanish_y_inf))

        xy_point = GetIntersection((vanish_y_inf, (intForX, 0)), (vanish_x_inf, (intForY, 0)))
        xy_point_up = vanish_z_inf #(xy_point[0], xy_point[1]-1)

        xyz_point = GetIntersection((xy_point, xy_point_up), (vanish_x_inf, yz_point))

        projected_points.append(xyz_point)
    return projected_points

def ProjectionMapTest(xvals, yvals):
    xvalstr = ' '.join([str(x) for x in xvals])
    yvalstr = ' '.join([str(y) for y in yvals])
    print(f'Using these values:   --xvals {xvalstr} --yvals {yvalstr}')
    points = []
    x0 = 0.25
    x1 = 0.75
    y0 = 0.25
    y1 = 0.75
    z0 = 0.000
    z1 = 0.2
    box = [(x0,y0,z0), (x1,y0,z0), (x1,y1,z0), (x0,y1,z0), (x0,y0,z1), (x1,y0,z1), (x1,y1,z1), (x0,y1,z1)]
    p = ProjectionMap(xvals, yvals, box)
    plot_style = 'k.-'
    PlotPoints([p[0], p[1], p[2], p[3], p[0]], plot_style)
    PlotPoints([p[4], p[5], p[6], p[7], p[4]], plot_style)
    PlotPoints([p[0], p[4]], plot_style)
    PlotPoints([p[1], p[5]], plot_style)
    PlotPoints([p[2], p[6]], plot_style)
    PlotPoints([p[3], p[7]], plot_style)

    fig.canvas.draw()

    rp = ReverseProjectionMap(xvals, yvals, p)
    plt.figure()
    PlotPoints([rp[0], rp[1], rp[2], rp[3], rp[0]], plot_style)
    PlotPoints([rp[4], rp[5], rp[6], rp[7], rp[4]], plot_style)
    PlotPoints([rp[0], rp[4]], plot_style)
    PlotPoints([rp[1], rp[5]], plot_style)
    PlotPoints([rp[2], rp[6]], plot_style)
    PlotPoints([rp[3], rp[7]], plot_style)
    plt.gca().invert_yaxis()
    plt.show(block=False)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--imagepath', '-i', help='path of image to test')
    parser.add_argument('--xvals', '-x', type=float, nargs=4, help='')
    parser.add_argument('--yvals', '-y', type=float, nargs=4, help='')
    args = parser.parse_args()
    # print (args)

    im = cv2.imread(args.imagepath)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.imshow(im)

    xvals = args.xvals if args.xvals else []
    yvals = args.yvals if args.yvals else []
    # xvals = [2028.902597, 2982.668831, 979.097403, 664.487013]
    # yvals = [687.668831, 1499.032468, 2131.564935, 939.357143]
    if len(xvals):
        x = xvals.copy()
        x.append(x[0])
        y = yvals.copy()
        y.append(y[0])
        plt.plot(x, y, 'r-x')


    def onclick(event):
        print('button=%d, x=%d, y=%d, xdata=%f, ydata=%f' % (event.button, event.x, event.y, event.xdata, event.ydata))
        if len(xvals) == 4:
            ProjectionMapTest(xvals, yvals)
        else:
            xvals.append(event.xdata)
            yvals.append(event.ydata)
            ax.cla()
            plt.imshow(im)
            x = xvals.copy()
            x.append(x[0])
            y = yvals.copy()
            y.append(y[0])
            plt.plot(x, y, 'r-x')
            fig.canvas.draw()

    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show(block=False)
    try:
        while True:
            plt.pause(0.01)
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
    finally:
        print('bye')

