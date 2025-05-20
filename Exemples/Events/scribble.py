from PyQt5 import QtCore,QtGui,QtWidgets
import sys

class Scribble(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.start=QtCore.QPoint(0,0)
        self.end=QtCore.QPoint(0,0)
        self.pen_color=QtCore.Qt.blue
        self.pen_width=10

    def mousePressEvent(self,event) :
        if event.button() == QtCore.Qt.LeftButton :
            self.start=self.end=event.pos()
    def mouseMoveEvent(self,event) :
        if event.buttons() & QtCore.Qt.LeftButton :
            self.end=event.pos()
            self.update()
    def mouseReleaseEvent(self,event) :
        if event.button()== QtCore.Qt.LeftButton :
            self.end=event.pos()
            self.update()

    def paintEvent(self,event) :
        print("paintEvent(self,event")
        painter=QtGui.QPainter(self)
        painter.setPen(QtGui.QPen(
                                    self.pen_color,
                                    self.pen_width,
                                    QtCore.Qt.SolidLine,
                                    QtCore.Qt.RoundCap,
                                    QtCore.Qt.RoundJoin
                                )
                        )
        painter.drawLine(self.start,self.end)
    def resizeEvent(self,event) :
        print(self.width(),self.height())

if __name__ == "__main__":
    app=QtWidgets.QApplication(sys.argv)
    mw=Scribble()
    mw.resize(300,200)
    mw.show()
    app.exec_()
