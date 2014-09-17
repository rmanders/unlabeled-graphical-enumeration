#!/usr/bin/env python

from unlabeled.orderly import *
from unlabeled.draw import drawGraph
from PIL import Image

g = unlabeledCompliment(3)


size = [200,200]
colors = (256,256,256)

img = Image.new("RGB", size, colors)
drawGraph(g.next(), (10,10,180), img)

with open("./test.jpg", "wb") as FILE:
    img.save(FILE)
