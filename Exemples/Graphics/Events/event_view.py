#!/usr/bin/env python3
# https://stackoverflow.com/questions/53627056/how-to-get-cursor-click-position-in-qgraphicsitem-coordinate-system

from PyQt5 import QtCore, QtGui, QtWidgets

class View(QtWidgets.QGraphicsView):
    def __init__(self,scene,parent=None,x=0,y=0,w=400,h=400):
        super(View, self).__init__(scene, parent)
        self.setGeometry(x,y,w,h)
        self.width,self.height=w,h
        self.create_items()

    def create_items(self) :
        pixmap=QtGui.QPixmap(200,100)
        pixmap.fill(QtCore.Qt.red)
        self.pix_item = self.scene().addPixmap(pixmap)
        self.pix_item.setPos(self.width/2,self.height/2)
        self.pix_item.setFlags(QtWidgets.QGraphicsItem.ItemIsSelectable| QtWidgets.QGraphicsItem.ItemIsMovable)

    def mousePressEvent(self, event):
        print("View.mousePressEvent()")
        print("event.pos() :",event.pos())
        # print("self.mapToScene() : ",self.mapToScene(event.pos()))
        # print("self.mapFromScene() : ",self.mapFromScene(event.pos()))
        items = self.items(event.pos())
        for item in items:
            if item is self.pix_item:
                print("item.mapToScene()  :  ",item.mapToScene(event.pos()))
                print("item.mapFromScene() : ",item.mapFromScene(event.pos()))
        super(View, self).mousePressEvent(event)

def bounding_rect(scene) :
    top=QtCore.QLineF(scene.sceneRect().topLeft(),scene.sceneRect().topRight())
    left=QtCore.QLineF(scene.sceneRect().topLeft(),scene.sceneRect().bottomLeft())
    right=QtCore.QLineF(scene.sceneRect().topRight(), scene.sceneRect().bottomRight())
    bottom=QtCore.QLineF(scene.sceneRect().bottomLeft(), scene.sceneRect().bottomRight())
    pen = QtGui.QPen(QtCore.Qt.red)   
    scene.addLine(top, pen)
    scene.addLine(left, pen)
    scene.addLine(right, pen)
    scene.addLine(bottom, pen)

if __name__ == '__main__':
    import sys
    app=QtWidgets.QApplication(sys.argv)

    # Scene 600x400
    scene=QtWidgets.QGraphicsScene()
    x,y=0,0
    w,h=600,400
    scene.setSceneRect(x,y,w,h)
    bounding_rect(scene)

    # View 400x400
    view= View(scene=scene)
    
    view.setWindowTitle("QGraphics : Event on View")
    view.show()
    sys.exit(app.exec_())
