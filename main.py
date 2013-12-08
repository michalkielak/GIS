import sys
from view import View
from PySide import QtGui


def main():
    app = QtGui.QApplication(sys.argv)
    myapp = View()
    myapp.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
