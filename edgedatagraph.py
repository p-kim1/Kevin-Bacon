###Implements a subclass of graph that allows data to be associated with edges.
from graph import *
class EdgeDataGraph(Graph):
    """Subclass of Graph that associates data with edges."""
    def __init__(self):
        """Adds new instance variable edgeList, which has tuples as keys and data as values."""
        super().__init__()
        self.edgeList={}

    def getEdgeData(self,vertex1,vertex2):
        """Returns the data associated with the given vertices, or None if the edge does not exist."""
        if (vertex1,vertex2) in self.edgeList:
            return self.edgeList[(vertex1,vertex2)]
        return None
        
    def addEdge(self,vertex1,vertex2,data):
        """Adds an edge to graph associated with the given data."""
        super().addEdge(vertex1,vertex2)
        self.edgeList[(vertex1,vertex2)]=data
