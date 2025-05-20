import sys
from PyQt5 import QtCore,QtGui
from PyQt5.QtWidgets import qApp,QApplication,QWidget,QPushButton,QGraphicsProxyWidget
from PyQt5.QtWidgets import QGraphicsScene,QGraphicsView,QGraphicsItem
#from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtWebEngineWidgets import QWebEngineView as QWebView,QWebEnginePage as QWebPage
from PyQt5.QtWebEngineWidgets import QWebEngineSettings as QWebSettings

class WebProxy(QGraphicsProxyWidget) :
    def __init__(self):
        super().__init__()
        self.angle=0.0
    def get_rotate(self) :
        return self.angle
    def set_rotate(self,angle) :
        self.angle=angle

class Scene(QGraphicsScene) :
    def __init__(self):
        super().__init__()
        self.setSceneRect(0,0,1000,800)
        web = QWebView()
        web.load(QtCore.QUrl("http://www.enib.fr"))
#        web.load(QtCore.QUrl("https://pythonspot.com/pyqt5-browser/"))
        self.proxy = WebProxy()
        self.proxy.setWidget(web)
        self.addItem(self.proxy)

    def mouseMoveEvent(self,event) :
        if (event.buttons() & QtCore.Qt.LeftButton) :
            delta=QtCore.QPointF(event.scenePos() 
                                - event.lastScenePos())
            rotation = delta.y()
            self.proxy.set_rotate(rotation + self.proxy.get_rotate())
        matrix=QtGui.QTransform()
        matrix.translate(self.proxy.widget().width()/2.0, self.proxy.widget().height()/2.0)
        matrix.rotate(self.proxy.get_rotate(), QtCore.Qt.YAxis)
        self.proxy.setTransform(matrix)

if __name__ == "__main__" :
    app=QApplication(sys.argv)
    button = QPushButton("Quit application")
    button.move(100,100)
    button.clicked.connect(app.quit)
    proxy = QGraphicsProxyWidget()
    proxy.setWidget(button)

    scene=Scene()
    scene.addItem(proxy)
    view = QGraphicsView(scene)
    view.setWindowTitle("Ma scene WEB")
    view.show()
    sys.exit(app.exec_())
