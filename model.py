import networkx as nx

class GraphModel(nx.Graph):
    def __init__(self, parent=None):
        self.next_id = 0
        super(GraphModel, self).__init__(parent)
        
    def nextId(self):
        self.next_id += 1
        return self.next_id - 1