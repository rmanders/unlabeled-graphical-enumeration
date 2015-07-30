'''Module for visualization'''

__author__ = "Ryan Anderson"

from graph import *

hasPIL = True

try:
    from PIL import Image, ImageDraw
except:
    hasPIL = False


def drawGraph( graph, xy, image ):
    """Draws a graph where the vertices are distributed on a 
    circle that is bounded by the 3-tuple xy=(x,y,length) which
    is a square whose upper left corner is x,y, and whose
    width & height is 'length' """

    if not hasPIL:
        print("Python image library not installed. Please install to use this function")
        return False

    draw = ImageDraw.Draw(image)
    radius = (float(xy[2]) / 2.0) - 10.0
    x = float(xy[0]+(xy[2] / 2)) 
    y = float(xy[1]+(xy[2] / 2)) 
    n = float(len(graph))
    theta = 0.0
    delta = 2*math.pi / n

    #assign coordinates to the vertices
    coords = {}
    for v in graph.keys():
        px = radius*math.cos(theta) + x
        py = radius*math.sin(theta) + y
        theta += delta	
        coords[v] = (px,py)

    # now draw all edges
    for v1 in graph.keys():
        for v2 in graph[v1]:
            draw.line( coords[v1] + coords[v2], fill=(0,0,0))

    for v in graph.keys():
        px,py = coords[v]
        draw.ellipse((px-5,py-5,px+5,py+5),fill=128)

    draw.rectangle([(xy[0],xy[1]),(xy[0]+xy[2],xy[1]+xy[2])],outline=(0,0,0))
    del draw
    return True
    
