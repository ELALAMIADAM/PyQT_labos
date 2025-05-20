# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtCore,QtWidgets
from view import View
from scene import Scene

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self,position=(0,0),dimension=(500,300)):
        QtWidgets.QMainWindow.__init__(self)
        self.setWindowTitle("CAI : Editeur v0.1")
        x,y=position
        w,h=dimension
        self.setGeometry(QtCore.QRect(x,y,w,h))
        self.create_actions()
        self.create_menus()
        self.connect_actions()
        self.create_scene((0,0),dimension)
    # self.dock=QtWidgets.QDockWidget("Left Right Dock",self)
        # self.dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        # self.addDockWidget(QtCore.Qt.LeftDockWidgetArea,self.dock)
    def set_view(self,view) :
        self.view=view
    def get_view(self) :
        return self.view

    def create_scene(self,position,dimension) :
        self.scene=QtWidgets.QGraphicsScene()
        self.view=View()
        print(position)
        x,y=position
        w,h=dimension
        self.scene.setSceneRect(x,y-self.menuBar().height(),w,h)
        self.view.setGeometry(x,y,w,h)
        self.view.setScene(self.scene)
        self.view.create()
        self.setCentralWidget(self.view)

    def create_actions(self) :
        self.action_tools=QtWidgets.QActionGroup(self)
        self.action_tools_line=QtWidgets.QAction(
        self.tr("&Line"),self)
        self.action_tools_line.setCheckable(True)
        self.action_tools_line.setChecked(True)
        self.action_tools.addAction(self.action_tools_line)
    def create_menus(self) :
        menubar = self.menuBar()
        menu_file = menubar.addMenu('&Tools')
        menu_file.addAction(self.action_tools_line)
    def connect_actions(self) :
        self.action_tools_line.triggered.connect(
            lambda checked,tool="line": self.set_action_tools(checked,tool)
        ) 
    def set_action_tools(self,checked,tool) :
        print("checked : ",checked)
        print("tool : ",tool)
        self.view.set_tool(tool)
    def resizeEvent(self, event):
        print("MainWindow.resizeEvent()")
        print("dx : ",self.size().width()-self.view.size().width())
        print("dy : ",self.size().height()-self.view.size().height())
        print("menubar size : ", self.menuBar().size())

if __name__ == "__main__" :  
    print(QtCore.QT_VERSION_STR)
    app=QtWidgets.QApplication(sys.argv)
    position=500,500
    dimension=600,400
    main=MainWindow(position,dimension)
    main.show()
    sys.exit(app.exec_())
