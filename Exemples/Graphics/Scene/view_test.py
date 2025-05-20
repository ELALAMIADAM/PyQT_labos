# https://stackoverflow.com/questions/55780918/pyqt5-i-cant-understand-qgraphicsscenes-setscenerectx-y-w-h
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

class View(QtWidgets.QGraphicsView):
    def __init__(self,scene=None,position=(50,50),dimension=(150,150)):
        super(View, self).__init__(scene)
        if scene==None :
            print("View need a scene !!!")
            exit(0)
        x,y=position
        w,h=dimension
        self.setGeometry(x,y,w,h)
        self.scene().setSceneRect(50,50,150,150)
        self.setAlignment(QtCore.Qt.AlignTop|QtCore.Qt.AlignLeft)
        self.bounding_rect()

        self.line=QtWidgets.QGraphicsLineItem()
        self.line.setLine(0,0,100,100)
        print("mapToScene",self.mapToScene(0,0))
        print("mapFromScene",self.mapFromScene(0,0))
        self.scene().addItem(self.line)
        rect_item=self.scene().addRect(QtCore.QRectF(60,60,130,130))
        rect_item.setPen(QtGui.QPen(QtGui.QColor("blue")))


    def bounding_rect(self) :
        scene=self.scene()
        top=QtCore.QLineF(scene.sceneRect().topLeft(),scene.sceneRect().topRight())
        left=QtCore.QLineF(scene.sceneRect().topLeft(),scene.sceneRect().bottomLeft())
        right=QtCore.QLineF(scene.sceneRect().topRight(),scene.sceneRect().bottomRight())
        bottom=QtCore.QLineF(scene.sceneRect().bottomLeft(),scene.sceneRect().bottomRight())
        pen=QtGui.QPen(QtCore.Qt.red)
        scene.addLine(top,pen)
        scene.addLine(left,pen)
        scene.addLine(right,pen)
        scene.addLine(bottom,pen)
        
    def resizeEvent(self,event):
        print("View.resizeEvent()")
        print(self.size())
        print(self.geometry())
        print("width : {}, height : {}".format(self.size().width(),self.size().height()))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    scene=QtWidgets.QGraphicsScene()
    view = View(scene)
    # x,y=0,0
    # w,h=600,400
    # scene.setSceneRect(x,y,w,h)
    # position=x,y
    # dimension=w,h
    # view = View(scene,position,dimension)
    view.show()
    sys.exit(app.exec_())

