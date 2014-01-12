# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\GIS\layout\ui\main_window.ui'
#
# Created: Sat Jan 04 12:51:36 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(845, 729)
        self.centralwidget = QtGui.QWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.graphicsView = QtGui.QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout_2.addWidget(self.graphicsView)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 845, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setMinimumSize(QtCore.QSize(0, 30))
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionKruskal = QtGui.QAction(MainWindow)
        self.actionKruskal.setObjectName("actionKruskal")
        self.actionNext = QtGui.QAction(MainWindow)
        self.actionNext.setObjectName("actionNext")
        self.nodeSettings = QtGui.QAction(MainWindow)
        self.actionNext.setObjectName("actionNext")
        self.actionSave_graph = QtGui.QAction(MainWindow)
        self.actionSave_graph.setObjectName("actionSave_graph")
        self.actionOpen_from_file = QtGui.QAction(MainWindow)
        self.actionOpen_from_file.setObjectName("actionOpen_from_file")
        self.actionOpen_from_file_weight = QtGui.QAction(MainWindow)
        self.actionOpen_from_file_weight.setObjectName("actionOpen_from_file_weight")
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionExport = QtGui.QAction(MainWindow)
        self.actionExport.setObjectName("actionExport")
        self.menuFile.addAction(self.actionExport)
        self.menuFile.addAction(self.actionOpen_from_file)
        self.menuFile.addAction(self.actionOpen_from_file_weight)
        self.menuFile.addAction(self.actionSave_graph)
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.toolBar.addAction(self.actionKruskal)
        self.toolBar.addAction(self.actionNext)
        self.toolBar.addAction(self.nodeSettings)
        self.toolBar.addSeparator()

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.actionExit, QtCore.SIGNAL("triggered()"), MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionKruskal.setText(QtGui.QApplication.translate("MainWindow", "Kruskal", None, QtGui.QApplication.UnicodeUTF8))
        self.actionKruskal.setToolTip(QtGui.QApplication.translate("MainWindow", "Kruskall algorithm", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNext.setText(QtGui.QApplication.translate("MainWindow", "Next", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNext.setToolTip(QtGui.QApplication.translate("MainWindow", "Next step", None, QtGui.QApplication.UnicodeUTF8))
        self.nodeSettings.setToolTip(QtGui.QApplication.translate("MainWindow", "Ustawienia punktów", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_graph.setText(QtGui.QApplication.translate("MainWindow", "Save to image file", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen_from_file.setText(QtGui.QApplication.translate("MainWindow", "Import graph nodes", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen_from_file_weight.setText(QtGui.QApplication.translate("MainWindow", "Import graph weights", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("MainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExport.setText(QtGui.QApplication.translate("MainWindow", "Export graph", None, QtGui.QApplication.UnicodeUTF8))

