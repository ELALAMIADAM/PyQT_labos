import sys

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine


app = QGuiApplication(sys.argv)

engine = QQmlApplicationEngine()
engine.quit.connect(app.quit)
# engine.load('hello.qml')
# engine.load()'button.qml'
# engine.load('slider.qml')
engine.load('checkbutton.qml')
# engine.load('shapes.qml')
# engine.load('animation.qml')

sys.exit(app.exec())