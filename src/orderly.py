'''
An implementation of the orderly method of unlabeled graph enumeration

This algorthim was described in the paper "Everyone a Winner"
'''

__author__ = "Ryan Anderson"
__status__ = "development"

from copy import deepcopy
import math
import combin, graph, draw

# =============================================================================
def augmenter(g):
    """Performs a sequence of augmenting operations on the graph parameter, g.
    In this case, it adds a single edge in all possible ways."""

    vertices = g.keys()
    for pair in combin.kCombinations(vertices, 2):
        if not graph.isAdj(g, pair[0], pair[1]):
            new_graph = deepcopy(g)
            new_graph[pair[0]].append( pair[1] )
            new_graph[pair[1]].append( pair[0] )
            yield new_graph
					
# =============================================================================
def code(g, permutation=None):
    """
    The code function returns a numerical value associated with a graph. 
    The	graph's "code" is used to impose the list ordering on all graphs in an
    isomorphism class. The code is also used to determine the graph's
    "canonicity." In this case, the code is simply the integer value of the
    graph's upper triangle adjacency matrix.

    This function has the additional capability of applying a permution to 
    the	vertices. This will yield a different code for each dictinct permutation 
    that is applied.
    """

    if( permutation == None ):
        permutation = g.keys()

    bits = ""
    for i in range( len( permutation ) ):
        for j in range( len( permutation ) ):
            if( j > i ):
                if graph.isAdj(g, permutation[i], permutation[j]):
                    bits += "1"
                else:
                    bits += "0"
    return int(bits,2)
			
# =============================================================================
def iscanonical(g):
    """
    This is where improvements will probably have the greatest effect. 
    Checks to see whether or not the graph's code represents the canonical 
    labelling for its isomorphism class. It does this by finding the 
    maximum code over all permutations of the vertices.
    """	
    startlist = g.keys()
    testcode = code(g)

    max = 0
    for perm in combin.allPermutations(startlist):
        curcode = code(g, perm)
        if( curcode > max ):
            max = curcode
    #print "Max: (canonical): " + str(max)
    if( testcode == max ):
        return True
    else:
        return False

# =============================================================================
def unlabeled(vertices):
    """
    This is the main implementation of the "Orderly" algorithm. It 
    generates one graph per invocation"
    """
    g0 = {}
    complete = vertices*(vertices-1)/2

    for i in range(1,vertices+1,1):
        g0[i] = []
    yield g0
    Lm = [g0]
    while  graph.edgecount(Lm[0]) < complete :
        L = []
        for g in Lm:
            for trial in augmenter( g ):
                if len(L)  > 0:
                    if code(trial) < code(L[-1]) and iscanonical(trial) == True:				
                        L.append(trial)
                        yield(L[-1])
                elif iscanonical(trial) == True:				
                    L.append(trial)
                    yield(L[-1])
        Lm = L
        L = []

# =============================================================================
def unlabeled_by_edge_count(vertices):
    g0 = {}
    complete = vertices*(vertices-1)/2

    for i in range(1,vertices+1,1):
        g0[i] = []
    Lm = [g0]
    yield Lm
    while graph.edgecount(Lm[0]) < complete:
        L = []
        for g in Lm:
            for trial in augmenter(g):			
                if len(L)  > 0:
                    #print "code trial(" + str(code(trial)) + "), code L[-1] (" + str(code( (L[-1])))
                    if code(trial) < code(L[-1]) and iscanonical(trial) == True :					
                        L.append(trial)
                elif iscanonical(trial) == True:				
                    L.append(trial)
        Lm = L
        yield Lm
				
# =============================================================================
def unlabeledCompliment(vertices):
    """
    This uses a novel 'complement' method for enumerating. Which is a slight 
    optimization that should increase performance by a factor of 2.
    """

    g0 = {}

    edgeclasses = vertices*(vertices-1)/2 + 1
    firsthalf = edgeclasses / 2
    odd = edgeclasses % 2
    print "unlabeled compilemnt: odd=",odd,"max edges: ",edgeclasses-1

    # initialize the first graph with the number of vertices but no edges
    for i in range(1,vertices+1,1):
        g0[i] = []

    # yield the first graph, then yield it's compliment
    yield g0
    yield graph.compliment( g0 )

    # Start with a list on m (in this case 0) edges.
    Lm = [g0]


    while graph.edgecount(Lm[0]) < firsthalf-1:

        # start with an empty list (L) on m+1 edges
        L = []

        # for each unlabeled graph on m edges, add an edge in all possible ways 
        for g in Lm:
            # for each graph generated by adding a single edge
            for trial in augmenter(g):
                if len(L)  > 0 :
                    if code(trial) < code(L[-1]) and iscanonical(trial) == True:					
                        L.append(trial)
                        yield(L[-1])
                        yield(graph.compliment(L[-1]))
                elif iscanonical(trial) == True:				
                    L.append(trial)
                    yield(L[-1])
                    yield(graph.compliment(L[-1]))
        print "Generating: graphs on",Graph.edgecount(Lm[0])+1,"edges("+str(len(L))+")"

        Lm = L
        L = []

    if odd == 1 :
        L = []
        for g in Lm:						
            for trial in augmenter(g):	
                if len(L)  > 0 :
                    if code(trial) < code(L[-1]) and iscanonical(trial) == True:					
                        L.append(trial)
                        yield(L[-1])
                elif iscanonical(trial) == True:				
                    L.append(trial)
                    yield(L[-1])
        Lm = L
        L =[]
		
