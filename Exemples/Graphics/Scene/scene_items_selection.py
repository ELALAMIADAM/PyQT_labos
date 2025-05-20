import sys
from PyQt5.QtCore import  Qt
from PyQt5.QtGui import  QPixmap
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsItem

app=QApplication(sys.argv)
view=QGraphicsView()
x,y=0,0
width,height=800,400
# view.setGeometry(x,y,width,height)
scene=QGraphicsScene()
# scene.setSceneRect(x,y,width,height)
view.setScene(scene)
#------------- scene creation --------------------
pix=scene.addPixmap(QPixmap('Icons/open.png'))
pix.setFlags(QGraphicsItem.ItemIsSelectable| QGraphicsItem.ItemIsMovable)
pix.setSelected(True)

pix=scene.addPixmap(QPixmap('Icons/exit.png'))
pix.setFlags(QGraphicsItem.ItemIsSelectable| QGraphicsItem.ItemIsMovable)
pix.setPos(100,50)   
pix.setSelected(True)
#-------------------------------------------------
for item in scene.selectedItems() :
    print(item)
view.show()
sys.exit(app.exec_())
