#!/bin/usr/env python

"""Primary script for testing"""

from graphs.orderly import *
import sys
import argparse

def setupArgs():
    """Set up command line arguments"""
    parser = argparse.ArgumentParser(description='Program for generating unlabeled graphs over n vertices')

    parser.add_argument('--vertices', '-n', default=4,
                        type=int, help='Max number of vertices', dest='vertices',
                        metavar='<max vertices>')
    return parser

def main():
    args = setupArgs().parse_args()
    vertices = args.vertices

    g = unlabeled_complement(vertices)

    for i in g:
        print i

if __name__ == "__main__":
    main()

