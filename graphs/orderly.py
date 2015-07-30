"""
Functions for generating unlabeled, undirected graphs.
"""

__author__ = "Ryan Anderson"
__status__ = "development"

from copy import deepcopy
import combin
import graph

# =============================================================================
def augmenter(g):
    """
    A python generator which performs a sequence of augmenting operations on 
    the graph parameter, g. In this case, it adds a single edge in all possible 
    ways.

    :param g: A dict which maps vertex numbers to adjacency lists.
    """

    vertices = g.keys()
    for pair in combin.k_combinations(vertices, 2):
        if not graph.isAdj(g, pair[0], pair[1]):
            new_graph = deepcopy(g)
            new_graph[pair[0]].append(pair[1])
            new_graph[pair[1]].append(pair[0])
            yield new_graph


# =============================================================================
def code(g, permutation=None):
    """
    The code function returns a numerical value associated with a graph.
    The	graph's "code" is used to impose the list ordering on all graphs in an
    isomorphism class. The code is also used to determine the graph's
    "canonicity." In this case, the code is simply the integer value of the
    graph's upper triangle adjacency matrix.

    This function has the additional capability of applying a permutation to
    the	vertices. This will yield a different code for each distinct permutation
    that is applied.

    :param g: A dict which maps vertex numbers to adjacency lists.

    :param permutation: A list containing a specific ordering/permutation of the vertices in g

    :return: A number unique number for this graph.

    """

    if permutation is None:
        permutation = g.keys()

    bits = ""
    for i in range(len(permutation)):
        for j in range(len(permutation)):
            if j > i:
                if graph.isAdj(g, permutation[i], permutation[j]):
                    bits += "1"
                else:
                    bits += "0"
    return int(bits, 2)


# =============================================================================
def is_canonical(g):
    """
    This is where improvements will probably have the greatest effect. 
    Checks to see whether or not the graph's code represents the canonical 
    labelling for its isomorphism class. It does this by finding the 
    maximum code over all permutations of the vertices.

    :param g: A dict which maps vertex numbers to adjacency lists.

    :return: True if the code of g is the maximum over all permutations of g's
    vertices. False otherwise
    """
    start_list = g.keys()
    test_code = code(g)

    max = 0
    for perm in combin.all_permutations(start_list):
        cur_code = code(g, perm)
        if (cur_code > max):
            max = cur_code
    # print "Max: (canonical): " + str(max)
    if (test_code == max):
        return True
    else:
        return False

# =============================================================================
def unlabeled(vertices):
    """
    A generator which generates all unlabeled (structurally different) graphs with a given number of vertices.

    This generator uses an algorithm described in the paper:
    R. C. Read, Everyone a Winner or How to Avoid Isomorphism When Cataloging Combinatorial Configurations, Annals of
    Discrete Mathematics 2 (1978) 107-120

    :param vertices: The number of vertices for which to generate unlabeled graphs over.
    """
    g0 = {}
    complete = vertices * (vertices - 1) / 2

    for i in range(1, vertices + 1, 1):
        g0[i] = []
    yield g0
    Lm = [g0]
    while graph.edgecount(Lm[0]) < complete:
        L = []
        for g in Lm:
            for trial in augmenter(g):
                if len(L) > 0:
                    if code(trial) < code(L[-1]) and is_canonical(trial) == True:
                        L.append(trial)
                        yield (L[-1])
                elif is_canonical(trial) == True:
                    L.append(trial)
                    yield (L[-1])
        Lm = L
        L = []


# =============================================================================
def unlabeled_by_edge_count(vertices):
    g0 = {}
    complete = vertices * (vertices - 1) / 2

    for i in range(1, vertices + 1, 1):
        g0[i] = []
    Lm = [g0]
    yield Lm
    while graph.edgecount(Lm[0]) < complete:
        L = []
        for g in Lm:
            for trial in augmenter(g):
                if len(L) > 0:
                    # print "code trial(" + str(code(trial)) + "), code L[-1] (" + str(code( (L[-1])))
                    if code(trial) < code(L[-1]) and is_canonical(trial) == True:
                        L.append(trial)
                elif is_canonical(trial):
                    L.append(trial)
        Lm = L
        yield Lm


# =============================================================================
def unlabeled_complement(vertices):
    """
    A slightly more efficient generator which generates all unlabeled (structurally different) graphs with a given
    number of vertices.

    This generator is equivalent to the 'unlabeled' generator except that it utilizes small shortcut by only generating
    the first half of the unlabeled graphs using the algorithm in 'unlabeled.' It generates the second half by taking
    the complement of all graphs in the first half. The complement in this case simply meaning: "for every pair of
    vertices with an edge, remove that edge and for every pair of vertices with no edge, add an edge."

    :param vertices: The number of vertices for which to generate unlabeled graphs over.
    """

    g0 = {}

    edgeclasses = vertices * (vertices - 1) / 2 + 1
    firsthalf = edgeclasses / 2
    odd = edgeclasses % 2
    print "graphs complement: odd=", odd, "max edges: ", edgeclasses - 1

    # initialize the first graph with the number of vertices but no edges
    for i in range(1, vertices + 1, 1):
        g0[i] = []

    # yield the first graph, then yield it's compliment
    yield g0
    yield graph.complement(g0)

    # Start with a list on m (in this case 0) edges.
    Lm = [g0]

    while graph.edgecount(Lm[0]) < firsthalf - 1:

        # start with an empty list (L) on m+1 edges
        L = []

        # for each graphs graph on m edges, add an edge in all possible ways
        for g in Lm:
            # for each graph generated by adding a single edge
            for trial in augmenter(g):
                if len(L) > 0:
                    if code(trial) < code(L[-1]) and is_canonical(trial) == True:
                        L.append(trial)
                        yield (L[-1])
                        yield (graph.complement(L[-1]))
                elif is_canonical(trial) == True:
                    L.append(trial)
                    yield (L[-1])
                    yield (graph.complement(L[-1]))
        print "Generating: graphs on", graph.edgecount(Lm[0]) + 1, "edges(" + str(len(L)) + ")"

        Lm = L
        L = []

    if odd == 1:
        L = []
        for g in Lm:
            for trial in augmenter(g):
                if len(L) > 0:
                    if code(trial) < code(L[-1]) and is_canonical(trial) == True:
                        L.append(trial)
                        yield (L[-1])
                elif is_canonical(trial) == True:
                    L.append(trial)
                    yield (L[-1])
        Lm = L
        L = []
