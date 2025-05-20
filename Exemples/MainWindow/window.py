# -*- coding: utf-8 -*-
import os,sys
from PyQt5 import QtCore,QtGui,QtWidgets
from numpy import size
from scene import Scene

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self,scene=None,position=(0,0),dimension=(500,300)):
        QtWidgets.QMainWindow.__init__(self)
        self.setWindowTitle("CAI : Editeur v0.1")
        x,y=position
        width,height=dimension
        self.setGeometry(QtCore.QRect(x,y,width,height))
        self.scene=scene
        self.view=None
        position=0,0
        self.create_scene(position,dimension)
        self.create_actions()
        self.create_menus()
        self.connect_actions()
        # self.statusBar()
        # self.dock=QtWidgets.QDockWidget("Left Right Dock",self)
        # self.dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        # self.addDockWidget(QtCore.Qt.LeftDockWidgetArea,self.dock)
    def set_scene(self,scene) :
        self.scene=scene
    def get_scene(self) :
        return self.scene
    def set_view(self,view) :
        self.view=view
    def get_view(self) :
        return self.view
    def create_scene(self,position,dimension) :
        x,y=position
        width,height=dimension
        self.view=QtWidgets.QGraphicsView()
        self.view.setGeometry(QtCore.QRect(x,y,width,height))
        if self.scene :
            self.scene.setSceneRect(x,y,width,height)
            # self.scene.setSceneRect(-width/2,-height/2,width/2,height/2)
            self.view.setScene(self.scene)
        else :
            print("MainWindow need  a scene ")
        self.setCentralWidget(self.view)
    def create_actions(self) :
        self.action_file_open=QtWidgets.QAction(QtGui.QIcon('icons/open.png'),"Open",self)
        self.action_file_open.setShortcut("Ctrl+O")
        self.action_file_open.setStatusTip("Open file")
        self.action_tools=QtWidgets.QActionGroup(self)
        self.action_tools_line=QtWidgets.QAction(
        self.tr("&Line"),self)
        self.action_tools_line.setCheckable(True)
        self.action_tools_line.setChecked(True)
        self.action_tools.addAction(self.action_tools_line)
    def create_menus(self) :
        menubar = self.menuBar()
        menu_file = menubar.addMenu('&File')
        menu_file.addAction(self.action_file_open)
        menu_file = menubar.addMenu('&Tools')
        menu_file.addAction(self.action_tools_line)
        # toolbar=self.addToolBar("File")
        # toolbar.addAction(self.action_file_open)
        # toolbar=self.addToolBar("Tools")
        # toolbar.addAction(self.action_tools_line)
    def connect_actions(self) :
        self.action_file_open.triggered.connect(self.open)
        self.action_tools_line.triggered.connect(
            lambda checked,tool="line": self.set_action_tools(checked,tool)
        ) 
    def open(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self,"Open File", os.getcwd())
        fileopen=QtCore.QFile(filename[0])

    def set_action_tools(self,checked,tool) :
        print("checked : ",checked)
        print("tool : ",tool)
        self.scene.set_tool(tool)
    def resizeEvent(self, event):
        print("MainWindow.resizeEvent()")
        print("dx : ",self.size().width()-self.view.size().width())
        print("dy : ",self.size().height()-self.view.size().height())
        print("menubar size : ", self.menuBar().size())

if __name__ == "__main__" :  
    print(QtCore.QT_VERSION_STR)
    app=QtWidgets.QApplication(sys.argv)
    scene=Scene()
    position=500,500
    dimension=600,400
    main=MainWindow(scene,position,dimension)
    main.show()
    sys.exit(app.exec_())
