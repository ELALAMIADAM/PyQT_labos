import sys
from PyQt5 import QtCore,QtGui
from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QGraphicsProxyWidget
from PyQt5.QtWidgets import QGraphicsScene,QGraphicsView,QGraphicsItem
#from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtWebEngineWidgets import QWebEngineView as QWebView,QWebEnginePage as QWebPage
from PyQt5.QtWebEngineWidgets import QWebEngineSettings as QWebSettings

app=QApplication(sys.argv)
scene=QGraphicsScene()

web = QWebView()
web.load(QtCore.QUrl("http://www.developpez.com"))
rect=scene.addRect(QtCore.QRectF(0, 0, 100, 100))
proxy = QGraphicsProxyWidget()
proxy.setWidget(web)
scene.addItem(proxy)

view=QGraphicsView(scene)
view.resize(500,300)
view.move(500, 500)
view.show()
sys.exit(app.exec_())
