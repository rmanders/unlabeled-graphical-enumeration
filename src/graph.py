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

def getUpperTriangleString(graph):
    '''Returns the upper triangle of a graph's adjacency matrix as a single string'''
    return ''.join(map(str,getUpperTriangle(graph)))

def getLowerTriangle(graph):
    """Gets the lower triangle of a simple graph's adjacency matrix"""
    bits = []
    for i in graph:
        for j in graph:
            if j>i:
                if isAdj(graph, i, j):
                    bits.append(1)
                else:
                    bits.append(0)
    return bits

def getLowerTriangleString(graph):
    '''Returns the lower triangle of a graph's adjacency matrix as a single string'''
    return ''.join(map(str,getLowerTriangle(graph)))

def getCode(graph):
    '''Returns the integer value of the upper triangle of the graph's 
    adjacency matrix. A simple graph is assumed (i.e. not mutliple edges and no 
    self-loops'''

    label = getUpperTriangleString(graph)
    return int(label,2)

def compliment(graph):
    '''Returns the compliment of the graph (exitsing edges become non-edges, non-edges 
    become edges.'''
    comp = {}
    for n in graph.keys():
        comp[n] = []
        for e in graph.keys():
            if n != e and not(e in graph[n]):
                comp[n].append(e)
    return comp

def relabel(graph, v1, v2):
    '''Re-label's v1 as v2. If v2 exists in the graph, v2 is renamed to v1'''
    if v1 not in graph:
        return
    nodes = graph.keys()
    if v2 in graph:
        # TODO: use a better way than looping through three times
        for n in nodes:
            if v2 in graph[n]:
                graph[n][graph[n].index(v2)] = 'x'
        for n in nodes:
            if v1 in graph[n]:
                graph[n][graph[n].index(v1)] = v2
        for n in nodes:
            if 'x' in graph[n]:
                graph[n][graph[n].index('x')] = v1
        v2tmp = graph.pop(v1)
        v1tmp = graph.pop(v2)
        graph[v1] = v1tmp
        graph[v2] = v2tmp
    else:
        for n in nodes:
            if v1 in graph[n]:
                graph[n][graph[n].index(v1)] = v2
        v2tmp = graph.pop(v1)
        graph[v2] = v2tmp

def upperTriangleToGraph(bits):
    '''Creates a graph from an upper triangle of an adjacency matrix'''
    nodes = 1+int(math.sqrt(1+(8*len(bits))) / 2)
    for v in range(1, nodes+1, 1):
        graph = {}
        graph[v] = []
    pos = 0
    # TODO: can probably do this in (nodes^2 / 2)
    for i in range(1, nodes+1, 1):
        s = ""
        for j in range(1, nodes+1, 1):
            if j>1:
                if bits[pos] == 1:
                    graph[i].append(j)
                    graph[j].append(i)
                pos += 1
    return graph
