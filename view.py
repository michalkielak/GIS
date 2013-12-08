from PySide import QtGui
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

    def ownMousePressEvent(self, event):
        node_id = self.graph.nextId()
        node = GraphicNode(node_id, event.scenePos().x(), event.scenePos().y())
        print event.scenePos().x(), event.scenePos().y()
        self.scene.addItem(node)
        self.graph.add_node(node_id)
