import sys
from PyQt5 import QtCore,QtGui,QtWidgets
from PyQt5.QtWidgets import QApplication,QGraphicsScene,QGraphicsView,QGraphicsItem

class PixmapItem(QtWidgets.QGraphicsPixmapItem):
    def __init__(self,pixmap,parent=None):
        super(PixmapItem, self).__init__(pixmap,parent)
        self.pixmap=pixmap
        self.setFlags(QtWidgets.QGraphicsItem.ItemIsSelectable| QtWidgets.QGraphicsItem.ItemIsMovable)

    def mousePressEvent(self,event):
        print("PixMapItem.mousePressEvent()")
        print("position",event.pos())
        # super(PixmapItem,self).mousePressEvent(event)
        print("item selected", self.isSelected())
        print("item selected", not(self.isSelected()))
        self.setSelected(not(self.isSelected()))
        print("item selected", self.isSelected())
        self.setSelected(True)
        print("item selected", self.isSelected())
   
def dimension(scene) :
    top= QtCore.QLineF(scene.sceneRect().topLeft(),scene.sceneRect().topRight())
    left= QtCore.QLineF(scene.sceneRect().topLeft(),scene.sceneRect().bottomLeft())
    right=QtCore.QLineF(scene.sceneRect().topRight(), scene.sceneRect().bottomRight())
    bottom=QtCore.QLineF(scene.sceneRect().bottomLeft(), scene.sceneRect().bottomRight())
    pen = QtGui.QPen(QtCore.Qt.red)   
    scene.addLine(top, pen)
    scene.addLine(left, pen)
    scene.addLine(right, pen)
    scene.addLine(bottom, pen)

if __name__=="__main__":
    app=QApplication(sys.argv)
    scene=QGraphicsScene()
    scene.setSceneRect(0,0,300,300)
    dimension(scene)
    #------------- scene creation --------------------

    pixmap = QtGui.QPixmap(100,100)
    pixmap.fill(QtCore.Qt.red)
    item=PixmapItem(pixmap)
    item.setPos(150,150)
    scene.addItem(item)
    item.setFlags(QtWidgets.QGraphicsItem.ItemIsSelectable| QtWidgets.QGraphicsItem.ItemIsMovable)
    print("selected",item.isSelected())
    #-------------------------------------------------
    view=QGraphicsView(scene)
    view.show()
    sys.exit(app.exec_())
