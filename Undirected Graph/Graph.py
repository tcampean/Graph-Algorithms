from Vertex import *


class TreeNode:
    def __init__(self,info):
        self._info = info
        self._left = self._right = None

    def createLevelOrder(self,elements,root,i,n):
        if i < n:
            temp = TreeNode(elements[i])
            root = temp
            root.left = self.createLevelOrder(elements,root.left,2*i+1,n)

            root.right = self.createLevelOrder(elements,root.right,2*i+2,n)
        return root






class Graph:
    def __init__(self,n,m):
        self.nrVertices = n  # the number of vertices
        self.nrEdges = m  # the number of edges
        self.vertices = {}  # a dictionary containing all vertices
        self.Edges = []
        for i in range(self.nrVertices):
            self.vertices[i] = Vertex(i)

    def parseVertices(self):
        return self.vertices

    def parseNeighbours(self,vertex):
        if vertex not in self.vertices:
            return -1
        return self.vertices[vertex].getNeighbours()

    def addVertex(self,key):
        if key in self.vertices:
            return -1
        vertex = Vertex(key)
        for i in range(len(self.vertices),key+1):
            self.vertices[i] = Vertex(i)
            self.nrVertices += 1
        self.vertices[key] = vertex
        return 1

    def addEdge(self,source,destination,weight):
        if source not in self.vertices:
            return -1
        if destination not in self.vertices:
            return -1
        if destination in self.vertices[source].getNeighbours():
            return -1
        if source == destination:
            return -1
        self.vertices[source].addEdge(destination,weight)
        self.vertices[destination].addEdge(source,weight)
        self.Edges.append([source, destination, weight])
        self.nrEdges+=1
        return 1

    def isEdge(self,source,destination):
        if source not in self.vertices:
            return -1
        if destination not in self.vertices:
            return -1
        return destination in self.vertices[source].getNeighbours()


    def getVerticesCount(self):
        return self.nrVertices

    def getEdgesCount(self):
        return self.nrEdges

    def getDegree(self,vertex):
        if vertex not in self.vertices:
            return -1
        return len(self.vertices[vertex].getNeighbours())

    def getWeight(self,source,destination):
        if source not in self.vertices:
            return -1
        if destination not in self.vertices:
            return -1
        for i in range(len(self.vertices[source].getNeighbours())):
            if self.vertices[source].getNeighbours()[i] == destination:
                return self.vertices[source].getWeight()[i]
        return -1


    def updateWeight(self,source,destination,new_weight):
        if source not in self.vertices:
            return -1
        if destination not in self.vertices:
            return -1
        ok_out = 0
        ok_in = 0
        for i in range(len(self.vertices[source].getNeighbours())):
            if self.vertices[source].neighbours[i] == destination:
                self.vertices[source].weight[i] = new_weight
                ok_out = 1
        for i in range(len(self.vertices[destination].getNeighbours())):
            if self.vertices[destination].neighbours[i] == source:
                self.vertices[destination].weight[i] = new_weight
                ok_in = 1
        if ok_out == 1 and ok_in == 1:
            return 1
        else:
            return -1

    def removeEdge(self,source,destination):
        if source not in self.vertices:
            return -1
        if destination not in self.vertices:
            return -1
        if destination not in self.vertices[source].getNeighbours():
            return -1
        for i in range(len(self.vertices[source].getNeighbours())):
            if self.vertices[source].neighbours[i] == destination:
                self.vertices[source].weight.pop(i)
        self.vertices[source].neighbours.remove(destination)
        for i in range(len(self.vertices[destination].getNeighbours())):
            if self.vertices[destination].neighbours[i] == source:
                self.vertices[destination].weight.pop(i)
        self.vertices[destination].neighbours.remove(source)
        self.nrEdges-=1
        return 1

    def removeVertex(self,x):
        if x not in self.vertices:
            return -1
        while(len(self.vertices[x].neighbours)>0):
            self.removeEdge(x,self.vertices[x].neighbours[0])
        del self.vertices[x]
        self.nrVertices-=1
        return 1


    def DFS(self, vertices, vertex, visited):
        visited.append(vertex) # current vertex gets marked as visited
        vertices.append(vertex) # we put it in our queue of vertices
        for neighbour in self.vertices[vertex].getNeighbours():
            if neighbour not in visited:
                vertices = self.DFS(vertices, neighbour, visited) # we will recursively apply the DFS for the neighbour found
        return vertices # we return the list with the vertices parsed


    def DFSConnected(self):
        visited = [] # we initialize a list to mark the visited vertices
        components = [] # a list that will hold all the components found
        for key in self.vertices:
            if key not in visited: # if the key was not visited we start looking for connected components from there
                vertices = [] # we initialize list that will hold the visited nodes during the iteration
                components.append(self.DFS(vertices, key, visited))
        return components # return the list with the connected components


    def ConnectedComponentsDFS(self):
        connected = self.DFSConnected()  # We get a list with all the components
        graphs = []  # Initialise a list of the graphs represented by the connected components
        for i in range(len(connected)):
            graphs.append(Graph(self.nrVertices, 0))  # Create as many graphs as the connected components
        for graph in graphs:
            for i in range(self.nrVertices):
                del graph.vertices[i]  # Since when we create a graph we initialize all the vertices as well, we need to
                # clear the vertices so we can have an accurate graph representation
        i = 0
        for component in connected:  # Iterate on the list of the components
            for node in component:  # Iterate on the nodes of each component
                if node not in graphs[i].vertices:
                    graphs[i].vertices[node] = Vertex(node)  # If there is no such node we add it
                for neighbour in self.vertices[
                    node].getNeighbours():  # Add all the edges between the connected component's nodes
                    # so we can have an accurate representation of the component
                    if neighbour not in graphs[i].vertices:
                        graphs[i].vertices[neighbour] = Vertex(neighbour)  # If there is no such node we add it
                    graphs[i].addEdge(node, neighbour, self.getWeight(node,
                                                                      neighbour))  # We add the edge between the node and it's neighbour
            i += 1
        return graphs  # Return the list of graphs


    def BFSConnected(self):
        visited = [] # No nodes have been visited yet
        for key in self.vertices: # We start the breadth first search from the first vertex of the graph
            if key not in visited:
                visited.append(key) # Mark the node as visited
                component = [] # initialize a new component
                vertices = [key] # a queue for the nodes to be visited
                while vertices:
                    vertex = vertices[0] # Starting from the first element in the queue
                    vertices.pop(0) # Eliminate the first node in the queue
                    component.append(vertex) # Put the first node in the queue in our component
                    for neighbour in self.vertices[vertex].getNeighbours():
                        if neighbour not in visited:
                            visited.append(neighbour) # If the neighbour wasn't visited we mark it
                            vertices.append(neighbour) # Add the unvisited neighbour to the queue
                yield component # After getting all the nodes up to the point there are no more unvisited neighbours we return the component


    def ConnectedComponents(self):
        connected = list(self.BFSConnected()) # We get a list with all the components
        graphs = [] # Initialise a list of the graphs represented by the connected components
        for i in range(len(connected)):
            graphs.append(Graph(self.nrVertices,0)) # Create as many graphs as the connected components
        for graph in graphs:
            for i in range(self.nrVertices):
                del graph.vertices[i] # Since when we create a graph we initialize all the vertices as well, we need to
                # clear the vertices so we can have an accurate graph representation
        i = 0
        for component in connected: # Iterate on the list of the components
            for node in component: # Iterate on the nodes of each component
                if node not in graphs[i].vertices:
                    graphs[i].vertices[node] = Vertex(node) # If there is no such node we add it
                for neighbour in self.vertices[node].getNeighbours(): # Add all the edges between the connected component's nodes
                    # so we can have an accurate representation of the component
                    if neighbour not in graphs[i].vertices:
                        graphs[i].vertices[neighbour] = Vertex(neighbour) # If there is no such node we add it
                    graphs[i].addEdge(node,neighbour,self.getWeight(node,neighbour)) # We add the edge between the node and it's neighbour
            i+=1
        return graphs # Return the list of graphs

    def getSource(self,sources,vertex): # looks for the source of the vertex
        if sources[vertex] == vertex:
            return vertex
        return self.getSource(sources,sources[vertex])

    def Kruskal(self):
        sorted_edges = sorted(self.Edges,key= lambda x: x[2]) # save a sorted version of the edges

        sources = [i for i in range(self.nrVertices)] # set the origin of a vertex to itself
        rank = [0] * self.nrVertices # set the rank to 0
        minimum_spanning_tree = []
        for edge in sorted_edges:
            x = self.getSource(sources, edge[0]) # get the sources of both the source and destination of an adge
            y = self.getSource(sources,edge[1])
            if x != y:
                minimum_spanning_tree.append(edge) # since the origins are different we put the edge in our tree and we do an union by rank
                if rank[x] < rank[y]:
                    sources[x] = y
                    rank[y] += 1
                else:
                    sources[y] = x
                    rank[x] +=1
            if len(minimum_spanning_tree) == self.nrVertices -1:
                break
        return minimum_spanning_tree

    def DFS2(self,graph,vertex,visited): # depth first search of a given graph
        visited.append(vertex)
        for neighbour in graph.vertices[vertex].getNeighbours():
            if neighbour not in visited:
                self.DFS2(graph,neighbour,visited)

    def Hamiltonian(self):
        tree = self.Kruskal() # get the tree resulted from Kruskal's algorithm
        copyGraph = Graph(self.nrVertices,0) # we will model the tree into a graph type
        for vertex in copyGraph.vertices:
            del vertex
        for edge in tree:
            if edge[0] not in copyGraph.vertices:
                copyGraph.addVertex(edge[0])
            if edge[1] not in copyGraph.vertices:
                copyGraph.addVertex(edge[1])
            copyGraph.addEdge(edge[0],edge[1],edge[2])
        # we will do a DFS for the tree obtained from Kruskal's
        # then we traverse the graph in the exact order of DFS to find a cycle
        # if we find a cycle that matches the criteria then that's a Hamiltonian cycle with less than double the minimum cost
        found = True
        order = []
        edges = []
        self.DFS2(copyGraph,0,order)
        if len(order) != self.nrVertices:
            return -1
        i = 0
        while found and i < len(order)-1:
            found = False
            for neighbour in self.vertices[order[i]].getNeighbours():
                if neighbour == order[i+1]: # we look for the next node to walk to
                    found = True
                    edges.append([order[i],order[i+1],self.getWeight(order[i],order[i+1])]) # when we find it we are going to put the edge in our list
                    break
            i+=1
        if found: # checking whether or not we can go from the last node to our origin
            found = False
            for neighbour in self.vertices[order[i]].getNeighbours():
                if neighbour == order[0]:
                    edges.append([order[i], order[0], self.getWeight(order[i], order[0])])
                    found = True
                    break
        if found:
            return edges

        if not found:
            return -1


























