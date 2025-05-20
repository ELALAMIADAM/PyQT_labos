# https://stackoverflow.com/questions/55780918/pyqt5-i-cant-understand-qgraphicsscenes-setscenerectx-y-w-h
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

class Scene(QtWidgets.QGraphicsScene):
    def __init__(self):
        super(Scene, self).__init__()
        # self.resize(300, 300)
        self.setSceneRect(50, 50, 150, 150)

        self.line = QtWidgets.QGraphicsLineItem()
        self.line.setLine(0, 0, 100, 100)

        self.view = QtWidgets.QGraphicsView()
        self.view.setGeometry(50, 50, 150, 150)
       
        self.addItem(self.line)
        rect_item = self.addRect(QtCore.QRectF(60, 60, 130, 130))
        rect_item.setPen(QtGui.QPen(QtGui.QColor("green")))
    
        self.view.setAlignment(QtCore.Qt.AlignTop|QtCore.Qt.AlignLeft)
        self.view.setScene(self)
        self.bounding_rect()
    
    def get_view(self) :
        return self.view
    
    def bounding_rect(self) :
        top=QtCore.QLineF(self.sceneRect().topLeft(),self.sceneRect().topRight())
        left=QtCore.QLineF(self.sceneRect().topLeft(),self.sceneRect().bottomLeft())
        right=QtCore.QLineF(self.sceneRect().topRight(),self.sceneRect().bottomRight())
        bottom=QtCore.QLineF(self.sceneRect().bottomLeft(),self.sceneRect().bottomRight())
        pen=QtGui.QPen(QtCore.Qt.red)
        self.addLine(top,pen)
        self.addLine(left,pen)
        self.addLine(right,pen)
        self.addLine(bottom,pen)
        
    def resizeEvent(self,event):
        print("Scene.resizeEvent()")
        print(self.size())
        print(self.geometry())
        print("width : {}, height : {}".format(self.size().width(),self.size().height()))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    scene = Scene()
    scene.get_view().show()
    sys.exit(app.exec_())

