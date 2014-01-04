from PySide import QtGui
from PySide import QtCore

class GraphicNode(QtGui.QGraphicsEllipseItem):
    def __init__(self, id, x, y):
        self.radius = 24
        self.id = id
        self.x = x
        self.y = y
        super(GraphicNode, self).__init__(x - self.radius / 2, y - self.radius / 2, self.radius, self.radius)
        self.setBrush(QtGui.QColor(0,0,160,255))

    def scenePos(self):
        return QtCore.QPointF(self.x, self.y)