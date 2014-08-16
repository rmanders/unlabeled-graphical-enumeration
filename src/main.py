#!/bin/usr/env python

from orderly import *


def main():
    edges = 4
    g = unlabeledCompliment(4)

    for i in g:
        print i

if __name__ == "__main__":
	main()

