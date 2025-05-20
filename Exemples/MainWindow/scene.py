#!/usr/bin/python
import sys
from PyQt5 import QtCore,QtGui,QtWidgets

class Scene (QtWidgets.QGraphicsScene) :
    def __init__(self):
        QtWidgets.QGraphicsScene.__init__(self)
        self.begin,self.end=QtCore.QPoint(0,0),QtCore.QPoint(0,0)
        self.offset=QtCore.QPoint(0,0)
        self.tool="rectangle"
        self.item=None
        self.pen,self.brush=None,None
        self.create()
    def __repr__(self):
        return "<Scene({},{},{})>".format(self.pen,self.brush,self.tool)
    def create(self) :
        text=self.addText("Hello World !")
        text.setPos(0,0)
        self.create_pen()
        line=QtWidgets.QGraphicsLineItem(0,0,100,100)
        line.setPen(self.pen)
        self.addItem(line)
        self.create_brush()
        rect=QtWidgets.QGraphicsRectItem(110,110,100,50)
        rect.setPen(self.pen)
        rect.setBrush(self.brush)
        self.addItem(rect)
        # line=QtWidgets.QGraphicsLineItem(180,180,360,360)
        # line.setPen(self.pen)
        # self.addItem(line)
    def create_pen(self) :
        self.pen=QtGui.QPen()
        self.pen.setColor(QtCore.Qt.red)
    def create_brush(self) :
        self.brush=QtGui.QBrush()
        self.brush.setColor(QtCore.Qt.blue)
        self.brush.setStyle(QtCore.Qt.CrossPattern)
    def set_tool(self,tool) :
        print("Scene.set_tool(self,tool)",tool)
        self.tool=tool
    def set_pen_color(self,color) :
        print("Scene.set_pen_color(self,color)",color)
        self.pen.setColor(color)
    def set_brush_color(self,color) :
        print("Scene.set_brush_color(self,color)",color)
        self.brush.setColor(color)
    # events
    def mousePressEvent(self, event):
        print("Scene.mousePressEvent()")
        print("event.scenePos() : ",event.scenePos())
        print("event.screenPos() : ",event.screenPos())
        self.begin=self.end=event.scenePos()
        self.item=self.itemAt(self.begin,QtGui.QTransform())
        if self.item :
            self.offset =self.begin-self.item.pos()                
    def mouseMoveEvent(self, event):
            # print("Scene.mouseMoveEvent()")
            # print("event.scenePos() : ",event.scenePos())
            self.end = event.scenePos()
            if self.item :
                self.item.setPos(event.scenePos() - self.offset)
    def mouseReleaseEvent(self, event):
        print("Scene.mouseReleaseEvent()")
        print("Scene or View",self)
        print("event.scenePos() : ",event.scenePos())
        print("self.tool : ",self.tool)
        print("self.item : ",self.item)
        print("items number : ",len(self.items()))
        print("pen : ",self.pen)
        self.end = event.scenePos()
        if self.item :
            self.item.setPos(event.scenePos() - self.offset)
            self.item=None
        elif self.tool=="line" :
            line=QtWidgets.QGraphicsLineItem(self.begin.x(), self.begin.y(), self.end.x(), self.end.y())
            line.setPen(self.pen)
            self.addItem(line)
        elif self.tool=="rectangle" :
            rect=QtWidgets.QGraphicsRectItem(
                                self.begin.x(),self.begin.y(),
                                self.end.x()-self.begin.x(),
                                self.end.y()-self.begin.y()
                        )
            rect.setPen(self.pen)
            rect.setBrush(self.brush)
            self.addItem(rect)
        else :
            print("nothing to draw !")

    def resizeEvent(self,event):
        print("geometry : ",self.width,self.height)
        print("dy : ",self.size().height()-self.view.size().height())
    
if __name__ == "__main__" :  
    print(QtCore.QT_VERSION_STR)
    app=QtWidgets.QApplication(sys.argv)
    scene=Scene()
    x,y=0,0
    w,h=600,400
    scene.setSceneRect(x,y,w,h)
    scene.create()
    root=QtWidgets.QGraphicsView()
    root.setGeometry(x,y,w,h)
    root.setScene(scene)
    # scene.setSceneRect(x-50,y-50,width,height)
    root.show()
    sys.exit(app.exec_())

