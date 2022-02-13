from Graph import *
from main import WriteGraph


class UI:
    def __init__(self, graph,output):
        self._graph = graph
        self._output = output
        self.__commands = {'1': self.add_vertex_ui, '2': self.add_edge_ui, '3': self.remove_vertex_ui,
                           '4': self.remove_edge_ui, '5': self.get_degree,
                           '6': self.is_edge_ui, '7': self.get_weight_ui,
                           '8': self.modify_weight_ui, '9': self.list_vertices, '10': self.list_neighbours,'11': self.get_no_vertices,
                           '12':self.get_connected,'13':self.hamiltonian}

    def print_menu(self):
        print("1: Add a vertex")
        print("2: Add an edge")
        print("3: Remove a vertex")
        print("4: Remove an edge")
        print("5: Get degree of a vertex")
        print("6: Check for an edge between two vertices")
        print("7: Get the weight between two vertices")
        print("8: Modify the weight between two vertices")
        print("9: List all vertices")
        print("10: Display the lists of the outbounds and inbounds of a vertex")
        print("11: Get number of vertices")
        print("12: Display all connected components")
        print("13: Hamiltonian cycle")
        print("0: Exit")


    def hamiltonian(self):
        result = self._graph.Hamiltonian()
        if result == -1:
            print("A Hamiltonian cost with at most double the minimum cost cannot be found within given graph")
            print("or the given graph does not respect the triangle inequality !")
        else:
            print("The following edges represent the hamiltonian cycle:")
            cost = 0
            for elem in result:
                print(elem)
                cost+=elem[2]
            print("This Hamiltonian cycle has a total cost of",cost)



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

    def get_degree(self):
        source = input("Enter the vertex: ")
        try:
            source = int(source)
        except ValueError:
            print("The vertex must be an integer!")
            return
        if self._graph.getDegree(source)==-1:
            print("The vertex does not exist!")
        else:
            print("The Degree of", source,"is",self._graph.getDegree(source))

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

    def list_neighbours(self):
        source = input("Enter the source: ")
        try:
            source = int(source)
        except ValueError:
            print("The source must be an integer!")
            return
        outbounds = "Neighbours: "
        if source not in self._graph.vertices:
            print("There is no such vertex!")
            return
        for i in self._graph.vertices[source].getNeighbours():
            outbounds +=str(i)+' '
        print("For the", source, " vertex:")
        print(outbounds)

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

    def get_connected(self):
        connected_components = self._graph.ConnectedComponentsDFS() # We get the list of graphs
        for i in range(len(connected_components)):
            vertices = "Vertices: "
            edges = "Edges: "
            edges_check = [] # A list used so that we won't get the same edge displayed twice
            print("Connected component Nr.",i+1)
            for key in sorted(connected_components[i].vertices):
                vertices+=str(key)+" " # we add the node to the print
                for neighbour in connected_components[i].vertices[key].getNeighbours():
                    edge1 = [key,neighbour,self._graph.getWeight(key,neighbour)]
                    edge2 = [neighbour,key, self._graph.getWeight(key, neighbour)]
                    if edge1 not in edges_check:
                        edges +=" (" + str(edge1[0])+", "+str(edge1[1])+", "+str(edge1[2])+") " # We add the edge to the print
                        edges_check.append(edge1)
                        edges_check.append(edge2)
            print(vertices)
            print(edges)
            print()

        print("There are",len(connected_components),"connected components in the list!")

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