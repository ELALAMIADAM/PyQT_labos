from PyQt5 import QtCore,QtWidgets
import sys

class Keypad(QtWidgets.QWidget):
    def __init__(self,nbuttons=10,parent=None) :
        super(Keypad, self).__init__()
        self.layout = QtWidgets.QVBoxLayout(self)
        self.buttons=[]
        self.create_buttons(nbuttons)
        
    def create_buttons(self,number) :
        for i in range(number) :
            button=QtWidgets.QPushButton(str(i),self)
            button.clicked.connect(lambda state,x=i:self.on_selected(state,x))
            self.buttons.append(button)
            self.layout.addWidget(button)
            
    def on_selected(self,state,index):
        print('state', state)
        print('index', index)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    keypad = Keypad(2)
    keypad.show()
    sys.exit(app.exec_())
