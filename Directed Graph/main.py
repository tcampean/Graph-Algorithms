from UI import *
from TextGraph import *
from Graph import *
import copy
import random


def ReadGraph(file_name):
    """
    Load data from file
    We assume file-saved data is valid
    """
    f = open(file_name, 'rt')  # read text
    param = f.readline()
    param = param.split(' ')
    graph = Graph(int(param[0]),0)
    lines = f.readlines()
    f.close()
    for line in lines:
        line = line.split(' ')
        if len(line) > 2:
            graph.addEdge(int(line[0]), int(line[1]), int(line[2]))
    return graph

def WriteGraph(graph,file_name):
    f = open(file_name, 'wt')
    line = str(graph.nrVertices) + " " + str(graph.nrEdges)
    f.write(line)
    f.write('\n')
    for key in sorted(graph.vertices):
        for i in range(len(graph.vertices[key].outbound)):
            line = str(key) + " " + str(graph.vertices[key].outbound[i]) + " " + str(graph.vertices[key].weightOut[i])
            f.write(line)
            f.write('\n')
    f.close()

def RandomGraph(vertices,edges):
    graph = Graph(vertices,0)
    i = 0
    while i<edges and i<vertices*vertices:
        source = random.randint(0,vertices-1)
        destination = random.randint(0,vertices-1)
        weight = random.randint(1,10000)
        if graph.addEdge(source,destination,weight) != -1:
            i+=1
    return graph


if __name__ == '__main__':
    selected = False
    while not selected:
        print("1: Graph from file")
        print("2: Randomly generated graph")
        command = input("Enter command: ")
        if command == '1':
            inputfile = input("Enter input file: ")
            outputfile = input("Enter output file: ")
            graph = TextGraph(inputfile,outputfile)
            #graph = ReadGraph(inputfile)
            selected=True
        else:
            outputfile = input("Enter output file: ")
            vertices = input("Enter the number of vertices: ")
            try:
                vertices = int(vertices)
            except ValueError:
                print("The vertex count must be an integer!")
                continue

            edges = input("Enter the amount of edges: ")
            try:
                edges = int(edges)
            except ValueError:
                print("The edge count must be an integer!")
                continue
            if edges>vertices*vertices:
                print("The given amount of edges exceeds the maximum number possible for the amount of vertices given!")
                print("The graph will have the maximum amount of edges instead!")
            graph = RandomGraph(vertices,edges)
            selected = True
    copy = copy.deepcopy(graph)
    ui = UI(graph,outputfile)
    ui.run()
    selected = False
    while not selected:
        print("Do you wish to save?")
        print("0: Yes")
        print("1: No")
        command = input("Enter command: ")
        if command == '0':
            WriteGraph(graph,outputfile)
            selected = True
        elif command == '1':
            WriteGraph(copy,outputfile)
            selected = True
        else:
            print("Invalid command!")