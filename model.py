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

    def minTree(self):
        return nx.minimum_spanning_tree(self)