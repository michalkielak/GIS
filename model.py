import networkx as nx


def euclideanDistance(p1, p2):
    return round(((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**0.5)


class GraphModel(nx.Graph):
    def __init__(self, parent=None):
        self.next_id = 0
        self.nodesLocations = []
        super(GraphModel, self).__init__(parent)
        
    def nextId(self):
        self.next_id += 1
        return self.next_id - 1
    
    def addEdge(self, id_from, id_to):
        weight = euclideanDistance(self.nodesLocations[id_from], self.nodesLocations[id_to])
        self.add_edge(id_from, id_to, weight=weight)
        return weight

    def minTree(self):
        return nx.minimum_spanning_tree(self)
    
    def iterativeAlgorithm(self):
        T = nx.Graph()
        for n in T:
            T.node[n]=self.node[n].copy()
        T.graph=self.graph.copy()
        for u, v, d in nx.minimum_spanning_edges(self, data=True):
            T.add_edge(u,v,d)
            yield T
    
    def serialize(self):
        output = ""
        for node_from in self.nodes(data=False):
            for node_to in self.nodes(data=False):
                if self.has_edge(node_from, node_to):
                    output+= str(self.get_edge_data(node_from, node_to)['weight'])+" "
                else:
                    output+= "0 "
            output+= "\n"
        output+= "\n"
        for node in self.nodesLocations:
            output+= str(node[0]) + " " + str(node[1]) + " 0 \n"
        return output
    
    def deserialize_nodes(self, input):
        for line in input:
            line = line.replace('  ', ' ')

        coordinates = False
        dimension = len(input)
        self.nodesLocations = []
        for line in input:
            if not coordinates and line != '\n':
                self.nodesLocations.append(map(float, line.strip().rstrip().split(' ')))
        self.clear()
        self.next_id = dimension
        for idx in range(dimension):
            self.add_node(idx)

    def deserialize_weights(self, input, weight = False):
        for line in input:
            line = line.replace('  ', ' ')
        adjMatrix = []

        for line in input:
            adjMatrix.append(map(float, line.strip().rstrip().split(' ')))

        if weight is not False:
            #Check matrix validitiy
            dimension = len(adjMatrix)
            for row in adjMatrix:
                if len(row) != dimension:
                    print "Error!!! Input matrix is invalid!"

            self.next_id = dimension
            for idx in range(dimension):
                for idy in range(dimension):
                    if adjMatrix[idx][idy] != 0:
                        self.add_edge(idx, idy, weight=adjMatrix[idx][idy])
