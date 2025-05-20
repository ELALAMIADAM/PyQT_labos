import sys
from PyQt5 import QtCore,QtGui
from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QGraphicsProxyWidget
from PyQt5.QtWidgets import QGraphicsScene,QGraphicsView,QGraphicsItem

translate_rotate=False

app=QApplication(sys.argv)
scene=QGraphicsScene()
view=QGraphicsView(scene)
x,y=0,0
w,h=300,300
view.setGeometry(QtCore.QRect(x,y,w,h))
scene.setSceneRect(x,y,w,h)
#------------- scene creation --------------------
rect=scene.addRect(QtCore.QRectF(0,0,100,100))
rect.setFlag(QGraphicsItem.ItemIsMovable)
button = QPushButton("Un bouton")
proxy = QGraphicsProxyWidget()
proxy.setWidget(button)
scene.addItem(proxy)

matrix=QtGui.QTransform()
if translate_rotate :
  matrix.translate(100,0)
  matrix.rotate(45)
else :
  matrix.rotate(45)
  matrix.translate(100,0)

matrix.scale(2,1)
proxy.setTransform(matrix)
#-------------------------------------------------
view.show()
sys.exit(app.exec_())
