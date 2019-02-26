class Edge: # represent edge as begin, end, length
   
    def __init__(self, begin, end, length):
        self.begin, self.end, self.length = begin, end, length
        
    def __repr__(self):
        return f"{self.begin} {self.end} {self.length}"    


def initDSU(vertices): # create DSU with N members, O(logn) implementation
    global parents, depths, edges
    edges = []
    parents = list(range(vertices))
    depths = [0] * vertices


def getRepresentative(vertex): # get "name" of set to which a vertex belongs
    if parents[vertex] == vertex:
        return vertex
    else:
        return getRepresentative(parents[vertex])
        


def mergeSets(vertex1, vertex2): # combine two sets
    a = getRepresentative(vertex1)
    b = getRepresentative(vertex2)
    if (a != b):
        if (depths[a] > depths[b]):
            a, b = b, a
        parents[a] = b
        if (depths[a] == depths[b]):
            depths[b] += 1

            
def Kruskal(edges):
    spanningTreeLength, addedEdges, vertexCount = 0, 0, len(parents)
    paths = sorted(edges, key=lambda x: x.length, reverse=True) # sort by length in reverse order
    while addedEdges < vertexCount - 1: 
        # a tree with k vertices always has k - 1 edges, therefore we quit after reaching this number
        x = paths.pop()
        if getRepresentative(x.begin) != getRepresentative(x.end):
            addedEdges += 1
            spanningTreeLength += x.length
            mergeSets(x.begin, x.end)
    return spanningTreeLength # return overall tree length