# -*- coding: utf-8 -*-
import os,sys
from PyQt5 import QtCore,QtGui,QtWidgets

from view import View

class Window(QtWidgets.QMainWindow):
    def __init__(self,position=(0,0),dimension=(500,300)):
        QtWidgets.QMainWindow.__init__(self)
        self.setWindowTitle("CAI  2425P : MainWindow")
        x,y=position
        w,h=dimension

        self.view=View()       
        self.scene=QtWidgets.QGraphicsScene()
        self.view.setScene(self.scene)
        self.setCentralWidget(self.view)

        self.view.setGeometry(x,y,w,h)
        self.scene.setSceneRect(x,y,w,h) 

        self.create_actions()
        self.connect_actions()
        self.create_menus()
 
    def get_view(self) :
        return self.view
    def set_view(self,view) :
        self.view=view
    def get_scene(self) :
        return self.scene
    def set_scene(self,scene) :
        self.scene=scene


    def create_actions(self) :
        # File actions
        self.action_file_open=QtWidgets.QAction(QtGui.QIcon('Icons/open.png'),"Open",self)
        self.action_file_open.setShortcut("Ctrl+O")
        self.action_file_open.setStatusTip("Open file")
        # Tools actions
        self.action_tools=QtWidgets.QActionGroup(self)
        self.action_tools_line=QtWidgets.QAction(
        self.tr("&Line"),self)
        self.action_tools_line.setCheckable(True)
        self.action_tools_line.setChecked(True)
        self.action_tools.addAction(self.action_tools_line)
        # Style actions    
        self.action_style_pen_color=QtWidgets.QAction(self.tr("&Color"),self)
        # Help actions    
    def connect_actions(self) :
        self.action_file_open.triggered.connect(self.file_open)
        self.action_tools_line.triggered.connect(
            lambda checked,tool="line": self.tools_selection(checked,tool)
        )
        self.action_style_pen_color.triggered.connect(self.style_pen_color_selection)

    # File actions implementation
    def file_open(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self,"Open File", os.getcwd())
        fileopen=QtCore.QFile(filename[0])
        print("open",fileopen)

    # Tools actions implementation
    def tools_selection(self,checked,tool) :
        print("Window.tools_selection()")
        print("checked : ",checked)
        print("tool : ",tool)
        self.view.set_tool(tool)

    # Style actions implementation
    def style_pen_color_selection(self):
        color = QtWidgets.QColorDialog.getColor(QtCore.Qt.yellow,self)
        if color.isValid() :
            self.view.set_pen_color(color.name())
 
    # Help actions implementation
    def help_about_us(self) :
        pass

    def create_menus(self) :
        # Menubar actions
        menubar = self.menuBar()
        menu_file = menubar.addMenu('&File')
        menu_file.addAction(self.action_file_open)
        menu_tool = menubar.addMenu('&Tools')
        menu_tool.addAction(self.action_tools_line)

        menu_style= menubar.addMenu('&Style')
        menu_style_pen= menu_style.addMenu('&Pen')
        menu_style_pen.addAction(self.action_style_pen_color)

        # # Toolbar actions
        toolbar=self.addToolBar("File")
        toolbar.addAction(self.action_file_open)
        # toolbar=self.addToolBar("Tools")
        # toolbar.addAction(self.action_tools_line)
        # # Statusbar 
        statusbar=self.statusBar()

    def resizeEvent(self, event):
        print("MainWindow.resizeEvent() : View")
        if self.view :
            print("dx : ",self.size().width()-self.view.size().width())
            print("dy : ",self.size().height()-self.view.size().height())
        else :
            print("MainWindow need  a view !!!!! ")
        print("menubar size : ", self.menuBar().size())

if __name__ == "__main__" :  
    print(QtCore.QT_VERSION_STR)
    app=QtWidgets.QApplication(sys.argv)

    position=0,0
    dimension=600,400

    mw=Window(position,dimension)

    offset=5
    xd,yd=offset,offset
    xf,yf=200+offset,100+offset
    line=QtWidgets.QGraphicsLineItem(xd,yd,xf,yf)
    line.setPen(mw.get_view().get_pen())
    mw.get_scene().addItem(line)

    mw.show()

    sys.exit(app.exec_())
