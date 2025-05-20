#!/usr/bin/env python3
from PyQt5 import QtCore,QtGui,QtWidgets

class PixmapItem(QtWidgets.QGraphicsPixmapItem):
    def __init__(self,pixmap,parent=None):
        super(PixmapItem, self).__init__(pixmap,parent)
        self.setFlags(QtWidgets.QGraphicsItem.ItemIsSelectable| QtWidgets.QGraphicsItem.ItemIsMovable)

    def mousePressEvent(self,event):
        super(PixmapItem,self).mousePressEvent(event)
        print("PixMapItem.mousePressEvent()")
        print("event.pos() : ",event.pos())
        print("self.scenePos() : ",self.scenePos())
        print("self.isSelected()", self.isSelected())
        # self.setSelected(True)
        # print("self.isSelected()", self.isSelected())
 
def bounding_rect(scene) :
    top=QtCore.QLineF(scene.sceneRect().topLeft(),scene.sceneRect().topRight())
    left=QtCore.QLineF(scene.sceneRect().topLeft(),scene.sceneRect().bottomLeft())
    right=QtCore.QLineF(scene.sceneRect().topRight(),scene.sceneRect().bottomRight())
    bottom=QtCore.QLineF(scene.sceneRect().bottomLeft(),scene.sceneRect().bottomRight())
    pen=QtGui.QPen(QtCore.Qt.red)   
    scene.addLine(top,pen)
    scene.addLine(left,pen)
    scene.addLine(right,pen)
    scene.addLine(bottom,pen)

if __name__=="__main__":
    import sys
    app=QtWidgets.QApplication(sys.argv)
    # Scene 600x400
    scene=QtWidgets.QGraphicsScene()
    x,y=0,0
    w,h=600,400
    scene.setSceneRect(x,y,w,h)
    bounding_rect(scene)

    # Items creation
    pixmap=QtGui.QPixmap(100,100)
    pixmap.fill(QtCore.Qt.red)
    item=PixmapItem(pixmap)
    item.setPos(w/2,h/2)
    scene.addItem(item)

    # View 400x400
    w,h=400,400
    view=QtWidgets.QGraphicsView(scene)
    view.setGeometry(x,y,w,h)

    view.setWindowTitle("QGraphics : Events on Item")
    # view.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
    view.show()

    sys.exit(app.exec_())