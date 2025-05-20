
import sys
from PyQt5 import QtWidgets
# from PyQt5.QtWidgets import QApplication, QPushButton

def gui(parent):
    hello=QtWidgets.QPushButton(parent)
    hello.setText("Click To Join")
    hello.setStyleSheet("background-color:yellow;")
    hello.move(100,50)

if __name__ == "__main__":
    app=QtWidgets.QApplication(sys.argv)
    mw=QtWidgets.QWidget()
    mw.setGeometry(300,150,300,400)
    mw.setWindowTitle("PyQt5 : Hello")
    gui(mw)
    mw.show()
    sys.exit(app.exec_())