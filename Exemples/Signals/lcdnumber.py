from PyQt5 import QtCore,QtWidgets
import sys

class SliderLCD(QtWidgets.QWidget):
  def __init__(self, parent=None):
    QtWidgets.QWidget.__init__(self, parent)
    self.gui()
    self.slots_connection()

  def gui(self,parent=None) :
    self.lcd=QtWidgets.QLCDNumber(self)
    self.slider=QtWidgets.QSlider(QtCore.Qt.Horizontal,self)

  def slots_connection(self) :
    self.slider.valueChanged.connect(self.lcd.display)

  def layout(self) :
    vbox=QtWidgets.QVBoxLayout()
    vbox.addWidget(self.lcd)
    vbox.addWidget(self.slider)
    self.setLayout(vbox)

if __name__ == "__main__" :
  app=QtWidgets.QApplication(sys.argv)
  mw=SliderLCD()
  mw.resize(500,100)
  mw.layout()
  mw.show()
  sys.exit(app.exec_())
