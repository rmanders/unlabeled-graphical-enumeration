__author__ = 'rmanders'

from PIL import Image
from graphs.draw import drawGraph
from graphs.orderly import unlabeled

def main():

    ul = unlabeled(3)
    graphs = []
    for g in ul:
        graphs.append(g)
    image = Image.new("RGB", (50,50), "white")
    drawGraph(graphs[-1], (0,0,50), image)
    image.save('./image.jpg')

if __name__ == "__main__":
    main()