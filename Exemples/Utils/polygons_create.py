# coding: utf-8
# https://ensip.gitlab.io/pages-info/ressources/transverse/tuto_pyqt.html#qgraphicsview-et-qgraphicsscene

import sys
from PyQt5 import QtCore,QtGui,QtWidgets

class MainWindow(QtWidgets.QWidget):
    def __init__(self, titre,x=0,y=0,width=600,height=800):
        QtWidgets.QWidget.__init__(self) 
        self.setWindowTitle(titre)
        self.setGeometry(x,y,width,height)
        self.scene=QtWidgets.QGraphicsScene()
        self.view =QtWidgets.QGraphicsView(self.scene,self)
        self.view.setGeometry(0,0,400,400)
        self.scene.setSceneRect(QtCore.QRectF(0,0,400,400))
        self.create_items()

        self.view.installEventFilter(self)

        self.polygon=[]
        self.start,self.end=QtCore.QPoint(0,0),QtCore.QPoint(0,0),

    def create_items(self) :
            rect=QtWidgets.QGraphicsRectItem(100.0,100.0,100.0,200)
            rect.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable,True)
            self.scene.addItem(rect)
        

    def mousePressEvent(self, event):
        print("mousePressEvent()")
        point=event.pos()
        print("event.pos()",point)
        # point=self.view.mapToScene(point)
        # print("self.view.mapToScene(event.pos()): ",point)

    def mouseMoveEvent(self, event):
        # print("mouseMoveEvent()")
        pass

    def mouseReleaseEvent(self, event):
        print("mouseReleaseEvent()")
        point=event.pos()
        print("event.pos()",point)
        
    def mouseDoubleClickEvent(self, event):
        print("mouseDoubleClickEvent()")
        print(self.polygon)
        qpoly=QtGui.QPolygonF(self.polygon)
        qgpoly=QtWidgets.QGraphicsPolygonItem(qpoly)
        self.scene.addItem(qgpoly)
        del self.polygon[:]


    def eventFilter(self,obj,event):
        if obj == self.view:
            if event.type() == QtCore.QEvent.MouseButtonPress:
                self.button_press_event(event)
                return True
        return False
 
    def button_press_event(self, event):
        print("button_press_event()")
        point=event.pos()
        # Conversion en coordonnées scene :
        point=self.view.mapToScene(point)
        # Ajout de point de polygone 
        self.scene.addRect(point.x()-10,point.y()-10,20,20)
        self.polygon.append(point)
             
    def display(self) :
        self.view.show()
        self.show()
 
if __name__=="__main__":
    app=QtWidgets.QApplication(sys.argv)   
    mw=MainWindow("Fenêtre principale")
    mw.display()

    sys.exit(app.exec_())
