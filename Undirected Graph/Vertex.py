class Vertex:
    def __init__(self, key):
        self.key = key  # represents the vertex identifier
        self.neighbours = []
        self.weight = []

    def getKey(self):
        return self.key

    def getNeighbours(self):
        return self.neighbours

    def getWeight(self):
        return self.weight

    def addEdge(self,x,weight):
        self.neighbours.append(x)
        self.weight.append(weight)

    def __str__(self):
        return "Vertex "+str(self.key)

