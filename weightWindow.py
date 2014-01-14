from PyQt4 import QtGui
from PySide.QtGui import QDialog
from layout.weight_window import Ui_Form


class Form(QDialog, Ui_Form):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.setupUi(self)