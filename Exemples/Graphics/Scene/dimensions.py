from PyQt5 import QtCore,QtGui,QtWidgets

def bounding_rect(scene) :
    top= QtCore.QLineF(scene.sceneRect().topLeft(),
                       scene.sceneRect().topRight())
    left= QtCore.QLineF(scene.sceneRect().topLeft(),
                        scene.sceneRect().bottomLeft())
    right=QtCore.QLineF(scene.sceneRect().topRight(), 
                        scene.sceneRect().bottomRight())
    bottom=QtCore.QLineF(scene.sceneRect().bottomLeft(),
                         scene.sceneRect().bottomRight())
    pen = QtGui.QPen(QtCore.Qt.red)   
    scene.addLine(top,pen)
    scene.addLine(left,pen)
    scene.addLine(right,pen)
    scene.addLine(bottom,pen)


if __name__ == '__main__':
    import sys
    scene_dimension=True
    app = QtWidgets.QApplication(sys.argv)
    view = QtWidgets.QGraphicsView()
    view.setWindowTitle("QGraphics : scene dimension")
    x,y=0,0
    width,height=800,600
    view.setGeometry(QtCore.QRect(x,y,width,height))
    scene=QtWidgets.QGraphicsScene()
    view.setScene(scene)
    #------------- scene creation -------------------- 
    if scene_dimension :
      scene.setSceneRect(-150,-150,300,300)
    else :
      scene.setSceneRect(x,y,width,height)
    # #-------------- alignment ----------------------   
    # view.setAlignment(QtCore.Qt.AlignTop)
    # view.setAlignment(QtCore.Qt.AlignLeft)
    # view.setAlignment(QtCore.Qt.AlignTop|QtCore.Qt.AlignLeft)

    bounding_rect(scene)
    view.setScene(scene)

    #-------------------------------------------------
    item=QtWidgets.QGraphicsRectItem(0,0, 50, 100)
    scene.addItem(item)
    item=QtWidgets.QGraphicsRectItem(width/2,height/2,50,100)
    scene.addItem(item)
    item=QtWidgets.QGraphicsRectItem(width-50,height-100, 50, 100)
    scene.addItem(item)
    if scene_dimension :
        item=QtWidgets.QGraphicsRectItem(-150,-150, 50, 100)
        scene.addItem(item)
        item=QtWidgets.QGraphicsRectItem(0,0,20,40)
        scene.addItem(item)
        item=QtWidgets.QGraphicsRectItem(100,50, 50, 100)
        scene.addItem(item)
#-------------------------------------------------
    view.show()
    sys.exit(app.exec_())
