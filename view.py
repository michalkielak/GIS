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
        self.ui.actionKruskal.triggered.connect(self.executeAlgorithm)
        
    def ownMousePressEvent(self, event):
        if not self.scene.itemAt(event.scenePos()):
            self.addNode(self.graph.nextId(), event.scenePos().x(), event.scenePos().y())
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
            self.graph.addEdge(self.clickedNodeId, clickedNode.id)
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
    
#    @QtCore.SLOT()
    def executeAlgorithm(self):
        min_tree = self.graph.minTree()
        self.addGraph(min_tree)
#        print "Hello world"
    
    def addNode(self, node_id, x, y):
        #Add node to view and model
        node = GraphicNode(node_id, x, y)
        self.scene.addItem(node)
        self.graph.add_node(node_id)
        self.graph.nodesLocations.append((x,y))

    def addGraph(self, graph):
        #Hiding current graph edges
        for item in self.scene.items():
            if isinstance(item, QtGui.QGraphicsLineItem):
                item.hide()
        for edge in graph.edges():
            edgeItem = QtGui.QGraphicsLineItem(self.graph.nodesLocations[edge[0]][0], self.graph.nodesLocations[edge[0]][1], self.graph.nodesLocations[edge[1]][0], self.graph.nodesLocations[edge[1]][1])
            edgeItem.setZValue(-1)
            pen = QtGui.QPen(QtGui.QBrush(QtGui.QColor(0,0,0,255)), 4)
            edgeItem.setPen(pen)
            self.scene.addItem(edgeItem)
    
#    def redraw(self):
        

