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

# =============================================================================
# Section 2: Graph Classes
# ==============================================================================
# Graph
# ==============================================================================
class Graph:
    "Class representing an undirected graph with colorable vertices"
    def __init__(self,vertices=0,adjList=None):
        self.g = []
        self.labels = []
        self.colors = []
        self.name = ""			

        if( adjList != None and isinstance(adjList,str)):
            line = adjList.split(':')
            if(len(line) != 5):
                raise Exception("Invalid Graph String Format: " + adjList)
            self.name = line[0]
            self.resetVertices( int(line[1]) )
            pos=0
            adj = line[4]
            for i in xrange(self.numVertices()):
                for j in xrange(self.numVertices()):
                    if( i > j ):
                        if( int(adj[pos]) == 0 ):
                            self.g[i][j] = 0
                            self.g[j][i] = 0
                        else:
                            self.g[i][j] = 1
                            self.g[j][i] = 1
                        pos += 1
                    elif( i == j):
                        self.g[i][j] = 0					
        else:
            self.resetVertices( vertices )


    def resetVertices(self, n):
        "Resets the number if vertices in the graph to the value specified by n and clears all edges"
        self.g = []
        self.labels = []		

        for i in xrange( n ):
            self.g.append([])
            self.labels.append("")
            for j in xrange( n ):
                self.g[i].append(0)

    def numVertices(self):
        return len(self.g)

    def numEdges(self):
        count = 0
        for i in xrange(len(self.g)):
            for j in xrange(len(self.g[i])):
                if( i > j and self.g[i][j] == 1):
                    count += 1
        return count

    def setEdge(self, v1, v2 ):
        self.g[v1][v2] = 1
        self.g[v2][v1] = 1

    def resetEdge(self, v1, v2 ):
        self.g[v1][v2] = 0
        self.g[v2][v1] = 0

    def getEdge(self, v1, v2 ):
        return self.g[v1][v2]

    def printLowerDiag(self):		
        result = ""
        for i in range(len(self.g)):
            for j in range(len(self.g[i])):
                if( i > j ):
                    result = result + str(self.g[i][j])
        print result

    def __str__(self):
        result = self.name + ":" + str(self.numVertices()) + ":" + str(self.numEdges()) + ":" + str((self.numVertices() * (self.numVertices()-1)) / 2) + ":"
        for i in xrange(self.numVertices()):
            for j in xrange(self.numVertices()):
                if( i > j ):
                    result = result + str(self.g[i][j])
        return result

    def printDBFormat(self):
        print self

    def printGraph(self):
        line = ""
        for i in range(len(self.g)):
            for j in range(len(self.g[i])):
                 line += str(self.g[i][j]) + " "
            print line
            line = ""

    def dumpEpsEquations(self):
        line = ""
        for i in range(len(self.g)):
            for j in range(len(self.g[i])):
                if( i > j and self.g[i][j] == 1):
                    x1 = "x" + str(i)
                    y1 = "y" + str(i)
                    x2 = "x" + str(j)
                    y2 = "y" + str(j)
                    line += "( " + x2 + " - " + x1 + " )^2 + " + "( " + y2 + " - " + y1 + " )^2 - 1 = 0,\n"
        print line


    def clear(self):
        for i in self.g:
            for j in i:
                j = 0

    def degree(self,v):
        d = 0
        for i in xrange(self.numVertices()):
            if( self.g[v][i] == 1):
                d += 1
        return d

#==============================================================================
# Vertex
#==============================================================================
class Vertex:

    def __init__(self,id=0,color=-1):
        self.id = id
        self.color = color
        self.adj = Set([])

    def __eq__(self,other):
        return self.id == other.id

    def __hash__(self):
        if not self:
            return 0
        value = self.id
        if value == -1:
            value = -2
        return value	

    def Degree(self):
        return len(adj)
		
#==============================================================================
# GraphEx
#==============================================================================
class GraphEx:

    def __init__(self, gObject=None):
        self.vertices = Set([])

    def AddVertex(self,v):
        self.vertices.add(v)

    def RemoveVertex(self,v):
        for i in self.vertices:
            i.adj.discard(v)
        self.vertices.discard(v)

    def AddEdge(self,v1,v2):
        if( ( v1 != v2 ) and (v1 in self.vertices) and (v2 in self.vertices) ):
            v1.adj.add(v2)
            v2.adj.add(v1)

    def RemoveEdge(self,v1,v2):
        v1.adj.discard(v2)
        v2.adj.discard(v1)

    def NumVertices(self):
        return len(self.vertices)

    def NumEdges(self):
        count=0
        for i in self.vertices:
            count += len(i.adj)
        return count/2

    def PrintGraph(self):
        for i in self.vertices:
            line = str(i.id) + "[" + str(i.color) + "]: "
            for j in i.adj:
                line += " -> (" + str(j.id) + ")"
            print line
		
#==============================================================================
# GraphToGraphEx
#==============================================================================
def GraphToGraphEx( g ):
    gex = GraphEx()
    vList = []
    for i in xrange(g.numVertices()):
        v = Vertex(i)
        vList.append(v)

    for i in vList:
        for j in xrange(g.numVertices()):
            if(g.g[i.id][j] == 1):
                i.adj.add(vList[j])
    gex.vertices = Set(vList)
    return gex

	
# For testing	
if __name__ == "__main__":
    tg = { 'A': ['B','D'], 'B': ['A','C'], 'C': ['B','D'], 'D': ['C','A'] }

