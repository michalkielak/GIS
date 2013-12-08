from PySide import QtGui

class GraphicNode(QtGui.QGraphicsEllipseItem):
    def __init__(self, id, x, y):
        self.radius = 8
        self.id = id
        super(GraphicNode, self).__init__(x - self.radius / 2, y - self.radius / 2, self.radius, self.radius)
        
    