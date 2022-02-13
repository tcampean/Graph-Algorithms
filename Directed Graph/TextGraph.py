from Graph import *

class TextGraph(Graph):

    def __init__(self, file_name,output):
        self._file_name = file_name
        self._output = output
        f = open(self._file_name,'rt')
        num = f.readline()
        f.close()
        num = num.split(' ')
        super().__init__(int(num[0]),0)
        self._load()

    def addVertex(self,key):
        result = super().addVertex(key)
        self._save()
        return result

    def addEdge(self,source,destination,weight):
        result = super().addEdge(source,destination,weight)
        self._save()
        return result

    def removeEdge(self,source,destination):
        result = super().removeEdge(source,destination)
        self._save()
        return result

    def removeVertex(self,x):
        result = super().removeVertex(x)
        self._save()
        return result

    def _save(self):
        f = open(self._output, 'wt')
        line = str(self.nrVertices) +" "+str(self.nrEdges)
        f.write(line)
        f.write('\n')
        for key in sorted(self.vertices):
            for i in range(len(self.vertices[key].outbound)):
                line = str(key)+ " " + str(self.vertices[key].outbound[i]) + " " + str(self.vertices[key].weightOut[i])
                f.write(line)
                f.write('\n')
        f.close()

    def _load(self):
        """
        Load data from file
        We assume file-saved data is valid
        """
        f = open(self._file_name, 'rt')  # read text
        lines = f.readlines()
        f.close()
        for line in lines:
            line = line.split(' ')
            if len(line) >2:
                super().addEdge(int(line[0]),int(line[1]),int(line[2]))