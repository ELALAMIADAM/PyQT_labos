# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtCore,QtGui,QtWidgets
from scene import Scene

class View(QtWidgets.QGraphicsView):
    def __init__(self):
        QtWidgets.QGraphicsView.__init__(self)
        self.begin,self.end=QtCore.QPoint(0,0),QtCore.QPoint(0,0)
        self.offset=QtCore.QPoint(0,0)
        self.tool="rectangle"
        self.item=None
        self.pen,self.brush=None,None
    def __repr__(self):
        return "<View({})>".format(self.tool)
    def create(self) :
        text=self.scene().addText("Hello World !")
        text.setPos(0,0)
        self.create_pen()
        line=QtWidgets.QGraphicsLineItem(0,0,100,100)
        line.setPen(self.pen)
        self.scene().addItem(line)
        self.create_brush()
        rect=QtWidgets.QGraphicsRectItem(110,110,100,50)
        rect.setPen(self.pen)
        rect.setBrush(self.brush)
        self.scene().addItem(rect)
        line=QtWidgets.QGraphicsLineItem(180,180,360,360)
        line.setPen(self.pen)
        self.scene().addItem(line)
    
    def create_pen(self) :
        self.pen=QtGui.QPen()
        self.pen.setColor(QtCore.Qt.red)
    def create_brush(self) :
        self.brush=QtGui.QBrush()
        self.brush.setColor(QtCore.Qt.blue)
        self.brush.setStyle(QtCore.Qt.CrossPattern)
    def set_tool(self,tool) :
        print("View.set_tool(self,tool)",tool)
        self.tool=tool
    def set_pen_color(self,color) :
        print("View.set_pen_color(self,color)",color)
        self.pen.setColor(color)
    def set_brush_color(self,color) :
        print("View.set_brush_color(self,color)",color)
        self.brush.setColor(color)

    def mousePressEvent(self, event):
        print("View.mousePressEvent()")
        print("event.pos() : ",event.pos())
        print("event.screenPos() : ",event.screenPos())
        self.begin=self.end=event.pos()
        self.item=self.scene().itemAt(self.begin,QtGui.QTransform())
        if self.item :
            self.offset =self.begin-self.item.pos()                
    def mouseMoveEvent(self, event):
        # print("View.mouseMoveEvent()")
        self.end = event.pos()
        if self.item :
            self.item.setPos(event.pos() - self.offset)
    def mouseReleaseEvent(self, event):
        print("View.mouseReleaseEvent()")
        print("View or Scene",self)
        print("self.tool : ",self.tool)
        print("self.item : ",self.item)
        print("items number : ",len(self.items()))
        self.end = event.pos()
        if self.item :
            self.item.setPos(event.pos() - self.offset)
            self.item=None
        elif self.tool=="line" :
            line=QtWidgets.QGraphicsLineItem(self.begin.x(), self.begin.y(), self.end.x(), self.end.y())
            line.setPen(self.pen)
            self.scene().addItem(line)
        elif self.tool=="rectangle" :
            rect=QtWidgets.QGraphicsRectItem(
                                self.begin.x(),self.begin.y(),
                                self.end.x()-self.begin.x(),
                                self.end.y()-self.begin.y()
                        )
            rect.setPen(self.pen)
            rect.setBrush(self.brush)
            self.scene().addItem(rect)
        else :
            print("nothing to draw !")
    def resizeEvent(self,event):
        print("geometry : ",self.size().width(),self.size().height())
        print("dy : ",self.size().height()-self.scene().height())

if __name__ == "__main__" :  
    print(QtCore.QT_VERSION_STR)
    app=QtWidgets.QApplication(sys.argv)
    root=View()
    x,y=0,0
    w,h=600,400
    root.setGeometry(QtCore.QRect(x,y,w,h))
    scene=QtWidgets.QGraphicsScene()
    scene.setSceneRect(x,y,w,h)
    root.setScene(scene)
    root.create()
    root.show()
    sys.exit(app.exec_())
