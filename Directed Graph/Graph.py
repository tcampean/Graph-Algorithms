from Vertex import *
import copy


class PriorityQueue:
    def __init__(self):
        self.__values = {}

    def isEmpty(self):
        return len(self.__values) == 0

    def pop(self):
        topPriority = None
        topObject = None
        for obj in self.__values:
            objPriority = self.__values[obj]
            if topPriority is None or topPriority > objPriority:
                topPriority = objPriority
                topObject = obj
        del self.__values[topObject]
        return topObject

    def add(self, obj, priority):
        self.__values[obj] = priority

    def contains(self, val):
        return val in self.__values

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

    def parseInbound(self,vertex):
        if vertex not in self.vertices:
            return -1
        return self.vertices[vertex].getInbound()

    def parseOutbound(self,vertex):
        if vertex not in self.vertices:
            return -1
        return self.vertices[vertex].getOutbound()


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
        if destination in self.vertices[source].getOutbound():
            return -1
        self.vertices[source].addOutbound(destination,weight)
        self.vertices[destination].addInbound(source,weight)
        self.Edges.append([source,destination,weight])
        self.nrEdges+=1
        return 1

    def isEdge(self,source,destination):
        if source not in self.vertices:
            return -1
        if destination not in self.vertices:
            return -1
        return destination in self.vertices[source].getOutbound()


    def getVerticesCount(self):
        return self.nrVertices

    def getEdgesCount(self):
        return self.nrEdges

    def getInDegree(self,vertex):
        if vertex not in self.vertices:
            return -1
        return len(self.vertices[vertex].getInbound())

    def getOutDegree(self,vertex):
        if vertex not in self.vertices:
            return -1
        return len(self.vertices[vertex].getOutbound())

    def getWeight(self,source,destination):
        if source not in self.vertices:
            return -1
        if destination not in self.vertices:
            return -1
        for i in range(len(self.vertices[source].outbound)):
            if self.vertices[source].outbound[i] == destination:
                return self.vertices[source].weightOut[i]
        return -1


    def updateWeight(self,source,destination,new_weight):
        if source not in self.vertices:
            return -1
        if destination not in self.vertices:
            return -1
        ok_out = 0
        ok_in = 0
        for i in range(len(self.vertices[source].outbound)):
            if self.vertices[source].outbound[i] == destination:
                self.vertices[source].weightOut[i] = new_weight
                ok_out = 1
        for i in range(len(self.vertices[destination].inbound)):
            if self.vertices[destination].inbound[i] == source:
                self.vertices[destination].weightIn[i] = new_weight
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
        if destination not in self.vertices[source].getOutbound():
            return -1
        for i in range(len(self.vertices[source].outbound)):
            if self.vertices[source].outbound[i] == destination:
                self.vertices[source].weightOut.pop(i)
        self.vertices[source].outbound.remove(destination)
        for i in range(len(self.vertices[destination].inbound)):
            if self.vertices[destination].inbound[i] == source:
                self.vertices[destination].weightIn.pop(i)
        self.vertices[destination].inbound.remove(source)
        self.nrEdges-=1
        return 1

    def removeVertex(self,x):
        if x not in self.vertices:
            return -1
        i = 0
        while(len(self.vertices[x].outbound)>0):
            self.removeEdge(x,self.vertices[x].outbound[0])
        while(i<len(self.vertices[x].inbound)):
            self.removeEdge(self.vertices[x].inbound[0],x)
        del self.vertices[x]
        self.nrVertices-=1
        return 1

    def BellmanFord(self, src,destination):
        dist = [float("Inf")] * self.nrVertices # initialize the list of distance values with infinity for every vertex
        pre = [-1] * self.nrVertices # initialize a list that contains the previous node iterated, has -1 for every vertex by default
        edges = [] # a list where all the edges that are passed during the iteration are stored
        dist[src] = 0 # we mark the distance from the source vector to itself with 0

        # Relaxation
        changed = True
        i = 0
        while changed and i < self.nrVertices:
            changed = False
            for edge in self.Edges:
                if dist[edge[0]] != float("Inf") and dist[edge[0]] + edge[2] < dist[edge[1]]:
                        dist[edge[1]] = dist[edge[0]] + edge[2] # update the the distance value of the adjacent vertices
                        pre[edge[1]] = edge[0] # we save the previous vertex in the list
                        changed = True
            i += 1

        # Check for negative-weight cycles
        for edge in self.Edges:
            if dist[edge[0]] != float("Inf") and dist[edge[0]] + edge[2] < dist[edge[1]]:
                    return -1,-1 # if we find a smaller distance after the relaxation it means that the graph has a negative weight cycle
                        # and the shortest path cannot be determined accurately
        if dist[destination] == float("Inf"):
            return -2,-2 # if the destination is still marked with infinity it means that we cannot reach the node
            # starting from the given source
        else:
            current = destination # we use this variable to go in reverse of our pathing to get all the edges we passed
            path = [] # list will hold all the vertices passed;
            while current!=-1:
                path.append(current)
                current=pre[current]
            for i in range(len(path)-1,0,-1):
                edges.append([path[i],path[i-1],self.getWeight(path[i],path[i-1])]) # we build the edges that were passed during the iteration

        return dist,edges # we return the list with the distances and the list with all the edges passed


    def topological_sort_predecessor(self,result,sorted,visited,count):
        for vertex in self.vertices: # iterate through every vertex
            if count[vertex] == 0 and vertex not in visited: # if the vertex has no inbounds and hasn't been visited
                for neighbour in self.parseOutbound(vertex): # we decrease the inbound degree of each of it's neighbour
                    count[neighbour] -= 1

                sorted.append(vertex) # we put the vertex in our list of sorted vertices
                visited.append(vertex) # mark the vertex as visited
                self.topological_sort_predecessor(result,sorted,visited,count) # recursively call the function
                for neighbour in self.parseOutbound(vertex):
                    count[neighbour] += 1 # we add to the inbound degree of each neighbour we decreased during our iteration
                sorted.pop() # we get the vertex out of the list of sorted vertices
                visited.pop() # mark the vertex as unvisited
        if len(sorted) == self.nrVertices: # if the list contains all the vertices then it means it's a complete sort
            sorted_list = copy.deepcopy(sorted) # make an exact copy of the list so we don't lose the values during backtrack
            result.append(sorted_list) # we save the the result

    def topological_sort_predecessor_singular(self):
        sorted = [] # list where the result will be stored
        queue = [] # list containing the queue of the vertices that have 0 inbound degree
        count = {} # dictionary holding the inbound degree of every vertex
        for vertex in self.vertices:
            count[vertex] = self.getInDegree(vertex) # put the inbound degree of the vertex in the dictionary
            if count[vertex] == 0:
                queue.append(vertex) # if it's 0 then we add it up in our queue
        while len(queue)>0:
            vertex = queue[0]
            queue.pop(0)
            sorted.append(vertex) # we put the first element of our queue in the sorted list
            for neighbour in self.parseOutbound(vertex):
                count[neighbour] -= 1 # for every neighbour we decrease the inbound degree (as if we are removing the vertex)
                if count[neighbour] == 0:
                    queue.append(neighbour) # if the neighbour's degree becomes 0 then we add it to the queue
        if len(sorted) < self.nrVertices: # if the result doesn't contain all the vertices then it means we have a cycle
            return -1
        return sorted # return the result

    def longest_path(self,source,destination):
        dist = [float("-Inf")] * self.nrVertices # distance list initialized with -inf for every vertex
        dist[source] = 0 # set the distance from source to source to 0
        pre = [-1] * self.nrVertices # list where we keep our pathing
        topological_order = self.topological_sort_predecessor_singular() # get the topological order of the graph
        if topological_order == -1:
            return -1,-1 # if it's -1 then the graph has a cycle and the order can't be computed
        for vertex in topological_order: # we iterate through the order of vertices
            if vertex == destination: # if we reach our destination we get out of the loop
                break
            for neighbour in self.parseOutbound(vertex):
                if dist[neighbour] < dist[vertex] + self.getWeight(vertex,neighbour):
                    dist[neighbour] = dist[vertex] + self.getWeight(vertex,neighbour) # update the new distance
                    pre[neighbour] = vertex # save the pathing of the vertex

        current = destination  # we use this variable to go in reverse of our pathing to get all the edges we passed
        path = []  # list will hold all the vertices passed;
        edges = [] # list containing pairs of three numbers representing the edges of our path
        while current != -1:
            path.append(current)
            current = pre[current]
        for i in range(len(path) - 1, 0, -1):
            edges.append([path[i], path[i - 1], self.getWeight(path[i], path[i - 1])])
        return dist[destination],edges # return the requested distance and the pathing from source to the destination

    def BFS(self,source):
        visited = []
        queue = []
        queue.append(source)
        visited.append(source)
        order = []
        parent = [-1] * self.nrVertices
        while queue:
            vertex = queue.pop(0)
            order.append(vertex)
            for i in self.vertices[vertex].getOutbound():
                if i not in visited:
                    queue.append(i)
                    visited.append(i)
                    parent[i] = vertex
        print("BFS ORDER IS: ", order)
        print("PARENTS ARE: ", parent)

    def DFS(self, vertices, vertex, visited,parent):
        visited.append(vertex)  # current vertex gets marked as visited
        vertices.append(vertex)  # we put it in our queue of vertices
        for neighbour in self.vertices[vertex].getOutbound():
            if neighbour not in visited:
                parent[neighbour] = vertex
                self.DFS(vertices, neighbour,
                                    visited,parent)  # we will recursively apply the DFS for the neighbour found
        return vertices  # we return the list with the vertices parsed

    def getChildren(self,x, prev):
        list = []
        for i in prev:
            if prev[i] == x:
                list.append(i)
        return list

    def printDijkstraTree(self,s, q, d, prev, indent):
        if q.contains(s):
            star = ''
        else:
            star = '*'
        print("%s%s [%s]%s" % (indent, s, d[s], star))
        for x in self.getChildren(s, prev):
            self.printDijkstraTree(x, q, d, prev, indent + '    ')

    def printDijkstraStep(self, s,x, q, d, prev):
        print ('----')
        if x is not None:
            print('x=%s [%s]' % (x, d[x]))
        self.printDijkstraTree(s, q, d, prev, '')

    def dijkstra(self,s):
        prev = {}
        q = PriorityQueue()
        q.add(s, 0)
        d = {}
        d[s] = 0
        visited = set()
        visited.add(s)
        self.printDijkstraStep(s, None, q, d, prev)
        while not q.isEmpty():
            x = q.pop()
            for y in self.vertices[x].getOutbound():
                if y not in visited or d[y] > d[x] + self.getWeight(x,y):
                    d[y] = d[x] + self.getWeight(x, y)
                    visited.add(y)
                    q.add(y, d[y])
                    prev[y] = x
            self.printDijkstraStep(s, x, q, d, prev)

        return d, prev


