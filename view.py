from PySide import QtGui, QtCore
from layout.main_window import Ui_MainWindow
from graphicNode import GraphicNode
from model import GraphModel


class View(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(View, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init()

    def init(self):
        self.graph = GraphModel()
        self.scene = QtGui.QGraphicsScene()
        self.ui.graphicsView.setScene(self.scene)
        self.scene.mousePressEvent = self.ownMousePressEvent
        self.scene.mouseReleaseEvent = self.ownMouseReleaseEvent
        self.scene.mouseMoveEvent = self.ownMouseMoveEvent
        self.clickedNodeId = None
        self.currentEdge = None
        self.currentEdgeStart = None

    def ownMousePressEvent(self, event):
        if not self.scene.itemAt(event.scenePos()):
            node_id = self.graph.nextId()
            node = GraphicNode(node_id, event.scenePos().x(), event.scenePos().y())
            self.scene.addItem(node)
            self.graph.add_node(node_id)
        else:
            clickedNode = self.scene.itemAt(event.scenePos())
            self.clickedNodeId = clickedNode.id
            self.currentEdgeStart = clickedNode.scenePos()
            self.currentEdge = QtGui.QGraphicsLineItem(clickedNode.scenePos().x(), clickedNode.scenePos().y(), event.scenePos().x(), event.scenePos().y())
            self.currentEdge.setZValue(-1)
            pen = QtGui.QPen(QtGui.QBrush(QtGui.QColor(0,0,0,255)), 4)
            self.currentEdge.setPen(pen)
            self.scene.addItem(self.currentEdge)
    
    def ownMouseReleaseEvent(self, event):
        if self.scene.itemAt(event.scenePos()) and self.currentEdge and isinstance(self.scene.itemAt(event.scenePos()), GraphicNode):
            clickedNode = self.scene.itemAt(event.scenePos())
            self.graph.add_edge(self.clickedNodeId, clickedNode.id)
            self.currentEdge.setLine(self.currentEdgeStart.x(), self.currentEdgeStart.y(), clickedNode.scenePos().x(), clickedNode.scenePos().y())
            self.currentEdge = None
            self.clickedNodeId = None
            self.currentEdgeStart = None
        elif self.currentEdge:
            self.scene.removeItem(self.currentEdge)
            self.currentEdge = None
            self.clickedNodeId = None
            self.currentEdgeStart = None
        
    def ownMouseMoveEvent(self, event):
        if self.currentEdge:
            self.currentEdge.setLine(self.currentEdgeStart.x(), self.currentEdgeStart.y(), event.scenePos().x(), event.scenePos().y())

