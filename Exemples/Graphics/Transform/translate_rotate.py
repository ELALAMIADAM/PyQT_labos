#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys,math
from PyQt5 import QtCore,QtGui,QtWidgets 

def dimension(scene) :
    rect=scene.sceneRect()
    top= QtCore.QLineF(rect.topLeft(),rect.topRight())
    left= QtCore.QLineF(rect.topLeft(),rect.bottomLeft())
    right=QtCore.QLineF(rect.topRight(),rect.bottomRight())
    bottom=QtCore.QLineF(rect.bottomLeft(),rect.bottomRight())

    pen = QtGui.QPen(QtCore.Qt.red)
    
    scene.addLine(top, pen)
    scene.addLine(left, pen)
    scene.addLine(right, pen)
    scene.addLine(bottom, pen)

if __name__=="__main__" :
    app=QtWidgets.QApplication(sys.argv)
    scene=QtWidgets.QGraphicsScene()
    view=QtWidgets.QGraphicsView(scene)
    x,y=0,0
    w,h=600,400
    view.setGeometry(QtCore.QRect(x,y,w,h))
    scene.setSceneRect(x,y,w,h)
    #scene.setSceneRect(0,0,w/2.0,h/2.0)
    #x,y=-view.width()/2,-view.height()/2
    #w,h=view.width()/2,view.height()/2
    #scene.setSceneRect(x,y,w,h)
    
    dimension(scene)
    #------------- scene creation --------------------
    
    line=QtCore.QLineF(0,0,view.width()/2,view.height()/2)
    scene.addLine(line)
    scene.addRect(QtCore.QRectF(view.width()/2,view.height()/2,200,100))

    text=QtWidgets.QGraphicsTextItem("Translate/Rotate")

    transform=QtGui.QTransform()
    bottomLeft=scene.sceneRect().bottomLeft()
    toTranslate=bottomLeft.y()/2
    transform.translate(0,toTranslate)
    transform.rotate(-45)
    # text.setTransform(transform)
    scene.addItem(text)

    text=QtWidgets.QGraphicsTextItem("Rotate/Translate")
    transform=QtGui.QTransform()
    transform.rotate(-45)
    transform.translate(0,toTranslate)
    # text.setTransform(transform)
    scene.addItem(text)

    #-------------------------------------------------
    view.show()
    sys.exit(app.exec_())
