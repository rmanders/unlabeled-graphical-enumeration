#!/bin/usr/env python

'''Primary script for testing'''

from orderly import *
import sys, argparse

def setupArgs():
    '''Set up command line arguments'''
    parser = argparse.ArgumentParser(description='Program doe enumerating unlabeled graphs')

    parser.add_argument('--vertices', '-n', default=4,
                        type=int, help='Max number of vetices', dest='vertices',
                        metavar='<max vertices>')
    return parser

def main(argv):
    args = setupArgs().parse_args()
    vertices = args.vertices

    g = unlabeledCompliment(vertices)

    for i in g:
        print i

if __name__ == "__main__":
	main(sys.argv)

