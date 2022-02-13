from Graph import *
from main import WriteGraph
import copy
from queue import PriorityQueue


class UI:
    def __init__(self, graph,output):
        self._graph = graph
        self._output = output
        self.__commands = {'1': self.add_vertex_ui, '2': self.add_edge_ui, '3': self.remove_vertex_ui,
                           '4': self.remove_edge_ui, '5': self.get_degree_in, '6': self.get_degree_out,
                           '7': self.is_edge_ui, '8': self.get_weight_ui,
                           '9': self.modify_weight_ui, '10': self.list_vertices, '11': self.list_outbound_inbound,'12': self.get_no_vertices,
                           '13': self.shortest_path_ford,'14': self.topological_sort,'15': self.longest_path,'16':self.all_longest_paths,
                           '17': self.BFS_ui,'18':self.DFS_ui,'19':self.djikstra_ui}

    def print_menu(self):
        print("1: Add a vertex")
        print("2: Add an edge")
        print("3: Remove a vertex")
        print("4: Remove an edge")
        print("5: Get Inbound Degree of a vertex")
        print("6: Get Outbound Degree of a vertex")
        print("7: Check for an edge between two vertices")
        print("8: Get the weight between two vertices")
        print("9: Modify the weight between two vertices")
        print("10: List all vertices")
        print("11: Display the lists of the outbounds and inbounds of a vertex")
        print("12: Get number of vertices")
        print("13: Get the shortest path using Bellman-Ford")
        print("14: Topological sort using predecessor count")
        print("15: Longest path between two vertices")
        print("16: Longest path between each two vertices")
        print("17: BFS")
        print("18: DFS")
        print("19: Dijkstra")
        print("0: Exit")

    def djikstra_ui(self):
        vertex = int(input("Enter source: "))
        d , prev = self._graph.dijkstra(vertex)
        print(d)
        print(prev)

    def BFS_ui(self):
        vertex = int(input("Enter source: "))
        print(self._graph.BFS(vertex))

    def DFS_ui(self):
        vertex = int(input("Enter source: "))
        visited = []
        vertices = []
        parent = [-1] * self._graph.nrVertices
        self._graph.DFS(vertices,vertex,visited,parent)
        print("Order: ", vertices)
        print("Paren:" , parent)


    def topological_sort(self):
        visited = []
        sorted = []
        count = {}
        for vertex in self._graph.vertices:
            count[vertex] = self._graph.getInDegree(vertex)
        result = []
        self._graph.topological_sort_predecessor(result,sorted,visited,count)
        if result == []:
            print("The graph is not a DAG!")
        else:
            print("The topological sorts for the given graph are:")
            for element in result:
                print(element)

    def longest_path(self):
        source = int(input("Enter the source: "))
        destination = int(input("Enter the destination: "))
        result,edges = self._graph.longest_path(source, destination)
        if result == float("-Inf"):
            print("There is no path from",source,"to",destination)
        elif result == -1:
            print("The given graph is not a DAG!")
        else:
            print()
            print("The path has the total weight of", result)
            print("The path is composed of the following edges:")
            string = ""
            for i in range(len(edges)):
                string += str(edges[i])
                if i != len(edges) - 1:
                    string += ', '
            print(string)
            print()

    def all_longest_paths(self):
        print("For the following sort",self._graph.topological_sort_predecessor_singular())
        for vertex1 in self._graph.vertices:
            print()
            print("==========================================")
            print("PATHS STARTING FROM",vertex1)
            print("==========================================")
            print()
            for vertex2 in self._graph.vertices:
                print()
                print("** FROM",vertex1,"TO",vertex2,"**")
                print()
                result, edges = self._graph.longest_path(vertex1, vertex2)
                if result == float("-Inf"):
                    print("There is no path from", vertex1, "to", vertex2)
                elif result == -1:
                    print("The given graph is not a DAG!")
                    return
                else:
                    print("The path has the total weight of", result)
                    print("The path is composed of the following edges:")
                    string = ""
                    for i in range(len(edges)):
                        string += str(edges[i])
                        if i != len(edges) - 1:
                            string += ', '
                    print(string)



    def shortest_path_ford(self):
        source = int(input("Enter the source: "))
        destination = int(input("Enter the destination: "))
        dist,edges = self._graph.BellmanFord(source,destination)
        if dist == -1 and edges == -1:
            print("There are negative cost cycles!")
        elif dist == -2 and edges == -2:
            print("There is no path between ",source,"and ",destination)
        else:
            print("The path has the total weight of",dist[destination])
            print("The path is composed of the following edges:")
            string =""
            for i in range(len(edges)):
                string+=str(edges[i])
                if i !=len(edges)-1:
                    string+=', '
            print(string)


    def get_no_vertices(self):
        print(len(self._graph.vertices))

    def add_vertex_ui(self):
        key = input("Enter a key: ")
        try:
            key = int(key)
        except ValueError:
            print("The key must be an integer!")
            return
        if self._graph.addVertex(key) == -1:
            print("The vertex already exists!")
        else:
            print("Vertex added successfully!")
            WriteGraph(self._graph,self._output)


    def add_edge_ui(self):
        source = input("Enter the source: ")
        try:
            source = int(source)
        except ValueError:
            print("The source must be an integer!")
            return

        destination = input("Enter the destination: ")
        try:
            destination = int(destination)
        except ValueError:
            print("The destination must be an integer!")
            return

        weight = input("Enter the weight: ")
        try:
            weight = int(weight)
        except ValueError:
            print("The source must be an integer!")
            return

        if self._graph.addEdge(source, destination, weight) == -1:
            print("The edge already exists or there are no such vertices in the graph!")
        else:
            print("Edge added successfully!")
            WriteGraph(self._graph,self._output)

    def remove_vertex_ui(self):
        key = input("Enter a key: ")
        try:
            key = int(key)

        except ValueError:
            print("The key must be an integer!")
            return
        if self._graph.removeVertex(key) == -1:
            print("The key doesn't exist in the graph!")
        else:
            print("The key was removed!")
            WriteGraph(self._graph, self._output)

    def remove_edge_ui(self):
        source = input("Enter the source: ")
        try:
            source = int(source)
        except ValueError:
            print("The source must be an integer!")
            return

        destination = input("Enter the destination: ")
        try:
            destination = int(destination)
        except ValueError:
            print("The destination must be an integer!")
            return

        if self._graph.removeEdge(source, destination) == -1:
            print("The source or destination doesn't belong to the graph!")
        else:
            print("Edge removed successfully!")
            WriteGraph(self._graph, self._output)

    def get_degree_in(self):
        source = input("Enter the vertex: ")
        try:
            source = int(source)
        except ValueError:
            print("The vertex must be an integer!")
            return
        if self._graph.getInDegree(source)==-1:
            print("The vertex does not exist!")
        else:
            print("The Inbound Degree of", source,"is",self._graph.getInDegree(source))

    def get_degree_out(self):
        source = input("Enter the vertex: ")
        try:
            source = int(source)
        except ValueError:
            print("The vertex must be an integer!")
            return
        if self._graph.getOutDegree(source) == -1:
            print("The vertex does not exist!")
        else:
            print("The Outbound Degree of", source,"is",self._graph.getOutDegree(source))

    def is_edge_ui(self):
        source = input("Enter the source: ")
        try:
            source = int(source)
        except ValueError:
            print("The source must be an integer!")
            return

        destination = input("Enter the destination: ")
        try:
            destination = int(destination)
        except ValueError:
            print("The destination must be an integer!")
            return
        if self._graph.isEdge(source, destination) == -1:
            print("The source or destination are not in the graph!")
        elif self._graph.isEdge(source, destination) == 1:
            print("There is an edge between", source, " and", destination)
        else:
            print("There is no edge between", source, " and", destination)

    def list_outbound_inbound(self):
        source = input("Enter the source: ")
        try:
            source = int(source)
        except ValueError:
            print("The source must be an integer!")
            return
        outbounds = "Outbound: "
        inbounds = "Inbound: "
        if source not in self._graph.vertices:
            print("There is no such vertex!")
            return
        iterator = OutboundIterator(self._graph.vertices[source])
        while True:
            try:
                elem = next(iterator)
                outbounds += str(elem) + " "
            except StopIteration:
                break
        iterator = InboundIterator(self._graph.vertices[source])
        while True:
            try:
                elem = next(iterator)
                inbounds += str(elem) + " "
            except StopIteration:
                break

        print("For the", source, " vertex:")
        print(outbounds)
        print(inbounds)

    def get_weight_ui(self):
        source = input("Enter the source: ")
        try:
            source = int(source)
        except ValueError:
            print("The source must be an integer!")
            return

        destination = input("Enter the destination: ")
        try:
            destination = int(destination)
        except ValueError:
            print("The destination must be an integer!")
            return
        if self._graph.getWeight(source, destination) == -1:
            print("The source or destination doesn't exist in the graph or there is no such edge!")
        else:
            print("The weight of the edge (", source, " ,", destination, ") is",
                  self._graph.getWeight(source, destination))

    def modify_weight_ui(self):
        source = input("Enter the source: ")
        try:
            source = int(source)
        except ValueError:
            print("The source must be an integer!")
            return

        destination = input("Enter the destination: ")
        try:
            destination = int(destination)
        except ValueError:
            print("The destination must be an integer!")
            return

        weight = input("Enter the weight: ")
        try:
            weight = int(weight)
        except ValueError:
            print("The source must be an integer!")
            return

        if self._graph.updateWeight(source, destination, weight) == -1:
            print("The source or destination aren't in the graph or there is no edge!")
        else:
            print("Weight updated successfully!")
            WriteGraph(self._graph, self._output)

    def list_vertices(self):
        for key in sorted(self._graph.vertices):
            print(self._graph.vertices[key])

    def run(self):
        done = False
        while not done:
            self.print_menu()
            command = input("Enter command: ")
            if command in self.__commands:
                self.__commands[command]()
            elif command == '0':
                done = True
            else:
                print("Invalid command!")
