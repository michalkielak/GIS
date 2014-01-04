from PySide import QtGui, QtCore
from layout.main_window import Ui_MainWindow
from graphicNode import GraphicNode
from model import GraphModel
import networkx as nx
import time


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
        self.originalMousePressEvent = self.scene.mousePressEvent
        self.originalMouseMoveEvent = self.scene.mouseMoveEvent
        self.originalMouseReleaseEvent = self.scene.mouseReleaseEvent
        self.scene.mousePressEvent = self.ownMousePressEvent
        self.scene.mouseReleaseEvent = self.ownMouseReleaseEvent
        self.scene.mouseMoveEvent = self.ownMouseMoveEvent
        self.clickedNodeId = None
        self.currentEdge = None
        self.currentEdgeStart = None
        self.minTreeEdges = []
        self.algorithmSteps = []
        self.ui.actionKruskal.triggered.connect(self.executeKruskalAlgorithm)
        self.ui.actionNext.triggered.connect(self.nextAlgorithmStep)
        self.ui.actionNext.setDisabled(True)
        
        
    def ownMousePressEvent(self, event):
        if not self.scene.itemAt(event.scenePos()):
            self.addNode(self.graph.nextId(), event.scenePos().x(), event.scenePos().y())
        elif isinstance(self.scene.itemAt(event.scenePos()), QtGui.QGraphicsSimpleTextItem):
            self.originalMousePressEvent(event)
        else:
            clickedNode = self.scene.itemAt(event.scenePos())
            self.clickedNodeId = clickedNode.id
            self.currentEdgeStart = clickedNode.scenePos()
            self.currentEdge = QtGui.QGraphicsLineItem(clickedNode.scenePos().x(), clickedNode.scenePos().y(), event.scenePos().x(), event.scenePos().y())
            self.currentEdge.setZValue(-2)
            pen = QtGui.QPen(QtGui.QBrush(QtGui.QColor(0,0,0,255)), 4)
            self.currentEdge.setPen(pen)
            self.scene.addItem(self.currentEdge)

    def ownMouseReleaseEvent(self, event):
        if self.scene.itemAt(event.scenePos()) and self.currentEdge and isinstance(self.scene.itemAt(event.scenePos()), GraphicNode):
            clickedNode = self.scene.itemAt(event.scenePos())
            self.addEdge(self.clickedNodeId, clickedNode.id)
            self.currentEdge = None
            self.clickedNodeId = None
            self.currentEdgeStart = None
        elif isinstance(self.scene.itemAt(event.scenePos()), QtGui.QGraphicsSimpleTextItem):
            self.originalMouseReleaseEvent(event)
        elif self.currentEdge:
            self.scene.removeItem(self.currentEdge)
            self.currentEdge = None
            self.clickedNodeId = None
            self.currentEdgeStart = None

    def ownMouseMoveEvent(self, event):
        if isinstance(self.scene.itemAt(event.scenePos()), QtGui.QGraphicsSimpleTextItem):
            self.originalMouseMoveEvent(event)
        elif self.currentEdge:
            self.currentEdge.setLine(self.currentEdgeStart.x(), self.currentEdgeStart.y(), event.scenePos().x(), event.scenePos().y())

    def addNode(self, node_id, x, y):
        #Add node to view and model
        node = GraphicNode(node_id, x, y)
        self.scene.addItem(node)
        self.graph.add_node(node_id)
        self.graph.nodesLocations.append((x,y))

    def addEdge(self, id_from, id_to):
        pos_from = self.graph.nodesLocations[id_from]
        pos_to = self.graph.nodesLocations[id_to]
        self.currentEdge.setLine(pos_from[0], pos_from[1], pos_to[0], pos_to[1])
        weight = self.graph.addEdge(id_from, id_to)
        middle = ((pos_from[0]+pos_to[0])/2, (pos_from[1]+pos_to[1])/2)
        weightItem = QtGui.QGraphicsSimpleTextItem(str(weight))
        weightItem.setPos(middle[0], middle[1] - 20)
        weightItem.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.scene.addItem(weightItem)


    def addGraph(self, graph):
        for item in self.minTreeEdges:
            self.scene.removeItem(item)
        self.minTreeEdges = []
        for edge in graph.edges():
            edgeItem = QtGui.QGraphicsLineItem(self.graph.nodesLocations[edge[0]][0], self.graph.nodesLocations[edge[0]][1], self.graph.nodesLocations[edge[1]][0], self.graph.nodesLocations[edge[1]][1])
            edgeItem.setZValue(-1)
            pen = QtGui.QPen(QtGui.QBrush(QtGui.QColor(255,0,0,255)), 4)
            edgeItem.setPen(pen)
            self.scene.addItem(edgeItem)
            self.minTreeEdges.append(edgeItem)


    def executeKruskalAlgorithm(self):
        self.algorithmSteps = []
        for step in self.graph.iterativeAlgorithm():
            self.algorithmSteps.append(step.copy())
        self.ui.actionNext.setEnabled(True)

    def nextAlgorithmStep(self):
        if self.algorithmSteps:
            self.addGraph(self.algorithmSteps.pop(0))
            if not self.algorithmSteps:
                self.ui.actionNext.setDisabled(True)

