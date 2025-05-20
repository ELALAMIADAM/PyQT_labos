from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal,pyqtSlot
DEBUG=True

class SigSlot (QtCore.QObject) :
    value_changed = pyqtSignal(int)
    def __init__(self,name):
        QtCore.QObject.__init__(self)
        self.value=0
        self.name=name

    def get_value(self) :
        if DEBUG :
            print(type(self).__name__+".get_value()")
        return self.value

    def set_value(self,v) :
        if DEBUG :
            print(type(self).__name__+".set_value()")
        if (v!=self.value) :
            print(f"set_value({self.name},{v})")
            self.value=v
            self.value_changed.emit(v)

if __name__ == "__main__" :
    a,b=SigSlot("A"),SigSlot("B")
    a.value_changed.connect(b.set_value)
    b.value_changed.connect(a.set_value)
    b.set_value(10)
    print(f"---------> a.get_value({a.get_value()})") # 0 or 10 ?
    a.set_value(100)
    print(f"---------> b.get_value({b.get_value()})") # 10 or 100  ?
