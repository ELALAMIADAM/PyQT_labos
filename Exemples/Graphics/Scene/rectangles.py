import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication,\
    QGraphicsScene,QGraphicsView,QGraphicsItem

app=QApplication(sys.argv)
scene=QGraphicsScene()
x,y=0,0
width,height=800,400
scene.setSceneRect(x,y,width,height)
view=QGraphicsView(scene)
view.setGeometry(x,y,width,height)

#------------- scene creation --------------------
rect=scene.addRect(QtCore.QRectF(200,100,200,100))
rect.setFlag(QGraphicsItem.ItemIsMovable)
rect.setFlag(QGraphicsItem.ItemIsSelectable)

rect=scene.addRect(QtCore.QRectF(400,200,200,100))
rect.setFlag(QGraphicsItem.ItemIsMovable)
rect.setFlag(QGraphicsItem.ItemIsSelectable)
#-------------------------------------------------
view.show()
sys.exit(app.exec_())
