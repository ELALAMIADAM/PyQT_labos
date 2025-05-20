#!/usr/bin/env python3
# https://stackoverflow.com/questions/53627056/how-to-get-cursor-click-position-in-qgraphicsitem-coordinate-system

from PyQt5 import QtCore, QtGui, QtWidgets

class PixmapItem(QtWidgets.QGraphicsPixmapItem):
    def __init__(self,pixmap,name="pix",parent=None):
        super(PixmapItem, self).__init__(pixmap,parent)
        self.name=name
        self.setFlags(QtWidgets.QGraphicsItem.ItemIsSelectable| QtWidgets.QGraphicsItem.ItemIsMovable)

    def get_name(self) :
        return self.name
    def set_name(self,name) :
        self.name=name

    def mousePressEvent(self,event):
        super(PixmapItem,self).mousePressEvent(event)
        print("PixMapItem.mousePressEvent() on :", self.get_name())
        print("event.pos() : ",event.pos())
        print("self.isSelected()", self.isSelected())

class Scene(QtWidgets.QGraphicsScene):
    def __init__(self,x,y,w,h):
        super(Scene, self).__init__()
        self.setSceneRect(x,y,w,h)
        self.bounding_rect()
        self.create_items()
 
    def create_items(self) :
        pixmap=QtGui.QPixmap(100,100)
        pixmap.fill(QtCore.Qt.red)
        item=PixmapItem(pixmap,name="Red Pixmap")
        item.setPos(150,150)
        self.addItem(item)
        pixmap=QtGui.QPixmap(100,100)
        pixmap.fill(QtCore.Qt.green)
        item=PixmapItem(pixmap,name="Green Pixmap")
        item.setPos(100,100)
        self.addItem(item)
        pixmap=QtGui.QPixmap(100,100)
        pixmap.fill(QtCore.Qt.blue)
        item=PixmapItem(pixmap,name="Blue Pixmap")
        item.setPos(50,50)
        self.addItem(item)

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
        super(Scene,self).mousePressEvent(event)
        print("Scene.mousePressEvent()")
        print("event.scenePos() :",event.scenePos())
        items = self.items(event.scenePos())
        print("items at position : ",event.scenePos())
        for item in items :
            print("   name : ",item.get_name())
        print("selected items : ")
        for item in self.selectedItems() :
            print("   name : ",item.get_name())
        selected_item=self.itemAt(event.scenePos(),QtGui.QTransform())
        if selected_item :
            print("item at : ",selected_item.get_name())
            print("item at selected ?: ",selected_item.isSelected())
            print("colliding items : ")
            for item in self.collidingItems(selected_item) :
                print("   name : ",item.get_name())
                item.mousePressEvent(event)

if __name__ == '__main__':
    import sys
    app=QtWidgets.QApplication(sys.argv)

    # Scene 600x400
    x,y=0,0
    width,height=600,400
    scene=Scene(x,y,width,height)

    # View 400x400
    view=QtWidgets.QGraphicsView(scene)
    width,height=400,400
    view.setGeometry(x,y,width,height)

    view.setWindowTitle("QGraphics : Event on Scene Items")
    view.show()
    sys.exit(app.exec_())
