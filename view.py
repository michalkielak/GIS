from PySide import QtGui, QtCore
from layout.main_window import Ui_MainWindow
from graphicNode import GraphicNode
from model import GraphModel
from weightWindow import Form
import networkx as nx


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
        self.originalcontextMenuEvent = self.scene.contextMenuEvent
        self.scene.mousePressEvent = self.ownMousePressEvent
        self.scene.mouseReleaseEvent = self.ownMouseReleaseEvent
        self.scene.mouseMoveEvent = self.ownMouseMoveEvent
        self.scene.contextMenuEvent = self.ownContextMenuEvent
        self.clickedNodeId = None
        self.weights = []
        self.currentEdge = None
        self.currentEdgeStart = None
        self.clickedMoveNodeId = None
        self.clickedMoveNode = None
        self.lineWidth = 4
        self.lineColor = QtGui.QColor("black")
        self.nodeWidth = 24
        self.nodeColor = QtGui.QColor("blue")
        self.minTreeEdges = []
        self.algorithmSteps = []
        self.edgesStartList = None
        self.currentNode = None
        self.weightWindowVariable = None
        self.ui.actionKruskal.triggered.connect(self.executeKruskalAlgorithm)
        self.ui.actionNext.triggered.connect(self.nextAlgorithmStep)
        self.ui.actionNext.setDisabled(True)
        self.ui.actionOpen_from_file.triggered.connect(self.openFileNodes)
        self.ui.actionOpen_from_file_weight.triggered.connect(self.openFileWeight)
        self.ui.actionSave_graph.triggered.connect(self.saveGraph)
        self.ui.actionExport.triggered.connect(self.actionExport)
        self.ui.actionPRIMA.triggered.connect(self.executePrimaAlgorithm)
        self.ui.actionExport_weights.triggered.connect(self.actionExport_weights)
        self.ui.nodeColorCb.currentIndexChanged['QString'].connect(self.setNodeColor)
        self.ui.lineColorCb.currentIndexChanged['QString'].connect(self.setLineColor)
        self.ui.lineWidthCb.currentIndexChanged['QString'].connect(self.setLineWidth)
        self.ui.nodeWidthCb.currentIndexChanged['QString'].connect(self.setNodeWidth)
        self.ui.labelSizeCb.currentIndexChanged['QString'].connect(self.setLabelSize)
        self.ui.actionNext_Prima.setEnabled(False)
        self.lineColor = QtGui.QColor(QtGui.QColor("blue"))
        self.lineWidth = 1
        self.labelSize = 8

    def setLineColor(self):
        self.lineColor = QtGui.QColor(str(self.ui.lineColorCb.currentText()))
        self.refreshScene()

    def setLineWidth(self):
        self.lineWidth = int(self.ui.lineWidthCb.currentText())
        self.refreshScene()

    def setNodeColor(self):
        self.nodeColor = QtGui.QColor(str(self.ui.nodeColorCb.currentText()))
        self.refreshScene()

    def setNodeWidth(self):
        self.nodeWidth = int(self.ui.nodeWidthCb.currentText())
        self.refreshScene()
        
    def setLabelSize(self):
        self.labelSize = int(self.ui.labelSizeCb.currentText())
        self.refreshScene()

    def ownContextMenuEvent(self, event):

        menu = QtGui.QMenu()
        ag = QtGui.QActionGroup(menu, exclusive=True)
        delete = menu.addAction("Delete")

        point = QtCore.QPoint(event.scenePos().x(), event.scenePos().y())
        action = menu.exec_(self.mapToGlobal(point))
        #if action == delete:
            #self.deleteItem(event)

    def deleteItem(self, event):
        item = self.scene.itemAt(event.scenePos())
        if item and isinstance(self.scene.itemAt(event.scenePos()), GraphicNode):
            deletedNode = self.scene.itemAt(event.scenePos())
            self.graph.remove_node(deletedNode.id)
            self.graph.nodesLocations.pop(deletedNode.id)
            self.redraw()

    def chageItemColor(self, item, color):
        return None


    def ownMousePressEvent(self, event):
        if event.button() is not QtCore.Qt.RightButton:
            if not self.scene.itemAt(event.scenePos()):
                self.addNode(self.graph.nextId(), event.scenePos().x(), event.scenePos().y())
            elif isinstance(self.scene.itemAt(event.scenePos()), QtGui.QGraphicsSimpleTextItem):
                self.originalMousePressEvent(event)
            elif event.button() is not QtCore.Qt.MiddleButton:
                clickedNode = self.scene.itemAt(event.scenePos())
                self.clickedNodeId = clickedNode.id
                self.currentEdgeStart = clickedNode.scenePos()
                self.currentEdge = QtGui.QGraphicsLineItem(clickedNode.scenePos().x(), clickedNode.scenePos().y(), event.scenePos().x(), event.scenePos().y())
                self.currentEdge.setZValue(-2)
                pen = QtGui.QPen(QtGui.QBrush(self.lineColor), self.lineWidth)
                self.currentEdge.setPen(pen)
                self.scene.addItem(self.currentEdge)
        elif event.button() is QtCore.Qt.MiddleButton and event.button() is not QtCore.Qt.RightButton:
            if self.scene.itemAt(event.scenePos()):
                clickedMoveNode = self.scene.itemAt(event.scenePos())
                self.clickedMoveNodeId = clickedMoveNode.id
                neighborsList = []
                neighborsList = self.graph.neighbors(self.clickedMoveNodeId)
                self.edgesStartList = []
                self.scene.removeItem(self.scene.itemAt(event.scenePos()))
                self.currentNode = self.addNode(self.clickedMoveNodeId, event.scenePos().x(),  event.scenePos().y(), addToModel = False)
                if neighborsList is not None:
                    for i in neighborsList:
                        middlex = (clickedMoveNode.x + self.graph.nodesLocations[self.clickedMoveNodeId][0])/2
                        middley = (clickedMoveNode.y + self.graph.nodesLocations[self.clickedMoveNodeId][1])/2
                        point = QtCore.QPoint(middlex, middley)
                        self.edgesStartList.append(self.graph.nodesLocations[self.clickedMoveNodeId][0], self.graph.nodesLocations[self.clickedMoveNodeId][1])
                        self.scene.removeItem(point)
                if self.edgesStartList is not None:
                    for k in self.edgesStartList:
                        self.currentEdge = QtGui.QGraphicsLineItem(self.edgesStartList[k][0], self.edgesStartList[1], event.scenePos().x(), event.scenePos().y())
                        pen = QtGui.QPen(QtGui.QBrush(self.lineColor), self.lineWidth)
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
        if event.button() is not QtCore.Qt.MiddleButton:
            if isinstance(self.scene.itemAt(event.scenePos()), QtGui.QGraphicsSimpleTextItem) or isinstance(self.scene.itemAt(event.scenePos()), GraphicNode):
                self.originalMouseMoveEvent(event)
            elif self.currentEdge:
                self.currentEdge.setLine(self.currentEdgeStart.x(), self.currentEdgeStart.y(), event.scenePos().x(), event.scenePos().y())
        elif event.button() is QtCore.Qt.MiddleButton:
            if isinstance(self.scene.itemAt(event.scenePos()), GraphicNode):
                self.originalMouseMoveEvent(event)
            if self.edgesStartList is not None:
                for k in self.edgesStartList:
                    self.currentEdge = QtGui.QGraphicsLineItem(self.edgesStartList[k][0], self.edgesStartList[1], event.scenePos().x(), event.scenePos().y())

    def addNode(self, node_id, x, y, addToModel = True):
        #Add node to view and model
        node = GraphicNode(node_id, x, y, self.nodeColor, self.nodeWidth)
        node.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.scene.addItem(node)
        if addToModel:
            self.graph.add_node(node_id)
            self.graph.nodesLocations.append((x,y))

    def addEdge(self, id_from, id_to, addToModel = True):
        pos_from = self.graph.nodesLocations[id_from]
        pos_to = self.graph.nodesLocations[id_to]
        self.currentEdge.setLine(pos_from[0], pos_from[1], pos_to[0], pos_to[1])
        if addToModel:
            weight = self.graph.addEdge(id_from, id_to)
        else:
            weight = self.graph.get_edge_data(id_from, id_to)['weight']
        middle = ((pos_from[0]+pos_to[0])/2, (pos_from[1]+pos_to[1])/2)
        weightItem = QtGui.QGraphicsSimpleTextItem(str(weight))
        font = QtGui.QFont()
        font.setPointSize(self.labelSize)
        weightItem.setFont(font)
        weightItem.setPos(middle[0], middle[1] - 20)
        weightItem.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.scene.addItem(weightItem)


    def addGraph(self, graph):
        for item in self.minTreeEdges:
            self.scene.removeItem(item)
        self.minTreeEdges = []
        for edge in graph.edges():
            edgeItem = QtGui.QGraphicsLineItem(self.graph.nodesLocations[edge[0]][0], self.graph.nodesLocations[edge[0]][1], self.graph.nodesLocations[edge[1]][0], self.graph.nodesLocations[edge[1]][1])
            for j in range(len(self.weights)):
                if self.weights[j][0] == str(self.graph.get_edge_data(edge[0], edge[1])['weight']):
                    self.weights[j][1] = 1
            edgeItem.setZValue(-1)
            pen = QtGui.QPen(QtGui.QBrush(QtGui.QColor("red")), 5)
            edgeItem.setPen(pen)
            self.scene.addItem(edgeItem)
            self.minTreeEdges.append(edgeItem)

    def executeKruskalAlgorithm(self):
        self.algorithmSteps = []
        self.weightWindowVariable = Form()
        self.weightWindowVariable.show()
        self.sortByWeight()
        for step in self.graph.iterativeAlgorithm():
            self.algorithmSteps.append(step.copy())

        self.ui.actionNext.setEnabled(True)
        self.ui.actionPRIMA.setEnabled(False)
        self.ui.actionKruskal.setEnabled(False)

    def executePrimaAlgorithm(self):
        self.algorithmSteps = []
        self.weightWindowVariable = Form()
        self.sortByWeight()
        for step in self.graph.iterativeAlgorithmPrima():
            self.algorithmSteps.append(step.copy())

        self.ui.actionNext.setEnabled(True)
        self.ui.actionPRIMA.setEnabled(False)
        self.ui.actionKruskal.setEnabled(False)


    def sortByWeight(self):
        edges = sorted(self.graph.edges(data=True),key=lambda t: t[2].get('weight',1))
        self.edges = []
        
        for edge in edges:
            self.edges.append({'weight': edge[2]['weight'], 'edge': edge, 'inGraph': False, 'createCycle':False})

    def printWeights(self):
        html = ""
        currentGraph = self.algorithmSteps[0]
        graphEdges = len(currentGraph.edges())
        for edge in self.edges:
            if currentGraph.has_edge(edge['edge'][0], edge['edge'][1]):
                html += str(edge['weight']) + "<br>"
            else:
                currentGraph.add_edge(edge['edge'][0], edge['edge'][1])
                print sum(1 for x in nx.simple_cycles(currentGraph.to_directed()))
                if sum(1 for x in nx.simple_cycles(currentGraph.to_directed()))!=graphEdges+1:
                    html+="<font color='red'>"+str(edge['weight']) + "</font><br>"
                else:
                    html+="<font color='green'>"+str(edge['weight']) + "</font><br>"
                currentGraph.remove_edge(edge['edge'][0], edge['edge'][1])

        self.weightWindowVariable.plainTextEdit.clear()
        self.weightWindowVariable.plainTextEdit.appendHtml(html)

    def nextAlgorithmStep(self):
        if self.algorithmSteps:
            if self.ui.actionNext_Prima.isEnabled() == False:
                self.printWeights()
            self.addGraph(self.algorithmSteps.pop(0))
            if not self.algorithmSteps:
                self.ui.actionNext.setDisabled(True)
                self.ui.actionPRIMA.setEnabled(True)
                self.ui.actionKruskal.setEnabled(True)

    def openFileNodes(self):
        filePath = QtGui.QFileDialog.getOpenFileName()[0]
        fp = open(filePath, 'r')
        inputGraph = fp.readlines()
        self.graph.deserialize_nodes(inputGraph)
        self.redraw_nodes()

    def openFileWeight(self):
        filePath = QtGui.QFileDialog.getOpenFileName()[0]
        fp = open(filePath, 'r')
        inputGraph = fp.readlines()
        self.graph.deserialize_weights(inputGraph, True)
        self.redraw()
        
    def saveGraph(self):
        filePath = QtGui.QFileDialog.getSaveFileName()[0]
        image = QtGui.QImage(int(self.scene.width()), int(self.scene.height()), QtGui.QImage.Format_ARGB32)
        painter = QtGui.QPainter(image)
        painter.setRenderHint(QtGui.QPainter.Antialiasing);
        self.scene.render(painter);
        image.save(filePath)
        painter.end()
        
    def actionExport_weights(self):
        output = self.graph.serialize_edges()
        filePath = QtGui.QFileDialog.getSaveFileName()[0]
        fp = open(filePath, "w")
        fp.write(output)
        fp.close()

    def actionExport(self):
        output = self.graph.serialize_nodes()
        filePath = QtGui.QFileDialog.getSaveFileName()[0]
        fp = open(filePath, "w")
        fp.write(output)
        fp.close()

    def redraw_nodes(self):
        for node in self.graph.nodes():
            self.addNode(node, self.graph.nodesLocations[node][0], self.graph.nodesLocations[node][1], False)

    def redraw(self):
        for node in self.graph.nodes():
            self.addNode(node, self.graph.nodesLocations[node][0], self.graph.nodesLocations[node][1], False)
        for u,v in self.graph.edges():
            self.currentEdge = QtGui.QGraphicsLineItem(0, 0, 0, 0)
            self.currentEdge.setZValue(-2)
            pen = QtGui.QPen(QtGui.QBrush(QtGui.QColor(0,0,0,255)), 4)
            self.currentEdge.setPen(pen)
            self.scene.addItem(self.currentEdge)
            self.addEdge(u, v, False)
        self.currentEdge = None
        
    def refreshScene(self):
        linePen = QtGui.QPen()
        linePen.setWidth(self.lineWidth)
        linePen.setColor(self.lineColor)
        labelFont = QtGui.QFont()
        labelFont.setPointSize(self.labelSize)
        for item in self.scene.items():
            if isinstance(item, QtGui.QGraphicsLineItem):
                item.setPen(linePen)
                self.scene.removeItem(item)
                graphicsLine = self.scene.addLine(item.line(), linePen)
                graphicsLine.setZValue(-1)
            elif isinstance(item, QtGui.QGraphicsSimpleTextItem):
                item.setFont(labelFont)
            elif isinstance(item, GraphicNode):
                nodeId = item.id
                self.scene.removeItem(item)
                self.addNode(nodeId, self.graph.nodesLocations[nodeId][0], self.graph.nodesLocations[nodeId][1], False)
                
                
    
    