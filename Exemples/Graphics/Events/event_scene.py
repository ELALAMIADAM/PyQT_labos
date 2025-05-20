#!/usr/bin/env python3
# https://stackoverflow.com/questions/53627056/how-to-get-cursor-click-position-in-qgraphicsitem-coordinate-system

from PyQt5 import QtCore, QtGui, QtWidgets

class Scene(QtWidgets.QGraphicsScene):
    def __init__(self,parent=None,x=0,y=0,w=600,h=400):
        super(Scene, self).__init__(parent)
        self.setSceneRect(x,y,w,h)
        self.width,self.height=w,h
        self.bounding_rect()
        self.create_items()
    
    def create_items(self) :
        pixmap=QtGui.QPixmap(200,100)
        pixmap.fill(QtCore.Qt.red)
        self.pix_item=self.addPixmap(pixmap)
        self.pix_item.setPos(self.width/2,self.height/2)
        self.pix_item.setFlags(QtWidgets.QGraphicsItem.ItemIsSelectable| QtWidgets.QGraphicsItem.ItemIsMovable)


    def bounding_rect(self) :
        top= QtCore.QLineF(self.sceneRect().topLeft(),self.sceneRect().topRight())
        left= QtCore.QLineF(self.sceneRect().topLeft(),self.sceneRect().bottomLeft())
        right=QtCore.QLineF(self.sceneRect().topRight(), self.sceneRect().bottomRight())
        bottom=QtCore.QLineF(self.sceneRect().bottomLeft(), self.sceneRect().bottomRight())
        pen = QtGui.QPen(QtCore.Qt.red)
        self.addLine(top, pen)
        self.addLine(left, pen)
        self.addLine(right, pen)
        self.addLine(bottom, pen)

    def mousePressEvent(self, event):
        print("Scene.mousePressEvent()")
        print("event.scenePos() : ",event.scenePos())
        items = self.items(event.scenePos())
        for item in items:
            if item is self.pix_item:
                print("item.pos()",item.pos())
                print("item.scenePos()",item.scenePos())
                print("item.mapFromScene()",item.mapFromScene(event.scenePos()))
                print("item.mapToScene()",item.mapToScene(event.scenePos()))
        super(Scene, self).mousePressEvent(event)

    def resizeEvent(self,event):
        print("Scene.resizeEvent()")
        print("width : {}, height : {}".format(self.size().width(),self.size().height()))
    

if __name__ == '__main__':
    import sys
    app=QtWidgets.QApplication(sys.argv)

    # Scene 600x400
    scene=Scene()

    # View 400x400
    view=QtWidgets.QGraphicsView(scene)
    x,y=0,0
    w,h=400,400
    view.setGeometry(x,y,w,h)

    view.setWindowTitle("QGraphics : Event on  Scene")
    view.show()
    sys.exit(app.exec_())
