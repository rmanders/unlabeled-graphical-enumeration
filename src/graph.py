'''
Functions for operations on graphs. 

The datatype used for a graph is a dictionary of lists,
where the key is the node number and the list is an
adjacency list of node numbers.
'''

__author__ = "Ryan Anderson"

import math

def isAdj(graph, i, j):
    """returns true if vertices i and j are adjacent (Undirected)"""
    if (j in graph[i] or i in graph[j]):
        return True
    return False

def edgecount(graph):
    """ Returns the number of edges in the graph"""
    count = 0
    for node in graph.keys():
        count += len( graph[node] )
    return count / 2

def getUpperTriangle(graph):
    """Gets the upper triangle of a simple graph's adjacency matrix"""
    bits = []
    for i in graph:
        for j in graph:
            if j<i:
                if isAdj(graph, i, j):
                    bits.append(1)
                else:
                    bits.append(0)
    return bits

def upperTriangleAsString(graph):
    '''Returns the upper triangle of a graph's adjacency matrix as a single string'''
    return ''.join(map(str,getUpperTriangle(graph)))
