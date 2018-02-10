class Graph:
    """A class representing a graph"""
    def __init__(self):
        """Create an empty graph"""
        self.adjList = {}

    def addVertex(self, vertex):
        """Add a vertex to the graph, associated with the given key (vertex)"""
        if vertex not in self.adjList:
            self.adjList[vertex] = []

    def addEdge(self, vertex1, vertex2):
        """Add an edge from vertex1 to vertex2. If vertex1 or vertex2 is not in the graph, adds it."""
        self.addVertex(vertex1)      
        self.addVertex(vertex2)

        if vertex2 not in self.adjList[vertex1]:
            self.adjList[vertex1].append(vertex2)

    def isAdjacent(self, vertex1, vertex2):
        """Returns True if there is an edge leading from vertex1 to vertex2"""
        return vertex2 in self.adjList[vertex1]

    def getAdjacentVertices(self, vertex):
        """Returns a list of vertices adjacent to the given vertex"""
        return self.adjList[vertex]

    def getVertices(self):
        """Returns a list of the vertices in the graph"""
        return list(self.adjList.keys())

    def getEdges(self):
        """Returns a list of tuples representing edges in the graph. In each tuple the first element is the "from" vertex, the second is the "to" vertex"""
        edgeList = []
        for v in self.adjList:
            for i in range(len(self.adjList[v])):
                edgeList.append((v, self.adjList[v][i]))
        return edgeList

    
        
