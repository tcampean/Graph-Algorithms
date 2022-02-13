class Vertex:
    def __init__(self, key):
        self.key = key  # represents the vertex identifier
        self.outbound = []  # represents the list of outbound vertices
        self.inbound = []  # represents the list of inbound vertices
        self.weightIn = []  # represents a list of inbound edges' weights
        self.weightOut = []  # represents a list of outbound edges' weights

    def getKey(self):
        return self.key

    def getOutbound(self):
        return self.outbound

    def getInbound(self):
        return self.inbound

    def getWeightIn(self):
        return self.weightIn

    def getWeightOut(self):
        return self.weightOut

    def addOutbound(self,x,weight):
        self.outbound.append(x)
        self.weightOut.append(weight)

    def addInbound(self,x,weight):
        self.inbound.append(x)
        self.weightIn.append(weight)

    def __str__(self):
        return "Vertex "+str(self.key)


class OutboundIterator:

    def __init__(self,vertex):
        self._vertex = vertex
        self._index = 0

    def __next__(self):
        if self._index < len(self._vertex.outbound):
            result = self._vertex.outbound[self._index]
            self._index+=1
            return result
        raise StopIteration


class InboundIterator:

    def __init__(self, vertex):
        self._vertex = vertex
        self._index = 0

    def __next__(self):
        if self._index < len(self._vertex.inbound):
            result = self._vertex.inbound[self._index]
            self._index += 1
            return result
        raise StopIteration

