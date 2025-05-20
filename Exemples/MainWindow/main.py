# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtCore,QtWidgets

from scene import Scene
from window import MainWindow

print(QtCore.QT_VERSION_STR)
app=QtWidgets.QApplication(sys.argv)
scene=Scene()                             # QGraphicsScene
position=500,500
dimension=600,400
main=MainWindow(scene,position,dimension) # QGraphicsView
main.show()
sys.exit(app.exec_())
