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

        self.action_file_save=QtWidgets.QAction(QtGui.QIcon('Icons/save.png'),"Save",self)
        self.action_file_save.setShortcut("Ctrl+S")
        self.action_file_save.setStatusTip("Save file")

        self.action_file_save_as=QtWidgets.QAction(QtGui.QIcon('Icons/save_as.png'),"Save as",self)
        self.action_file_save_as.setShortcut("Ctrl+Shift+S")
        self.action_file_save_as.setStatusTip("Save file as")

        # self.action_file_print=QtWidgets.QAction(QtGui.QIcon('Icons/print.png'),"Print",self)
        # self.action_file_print.setShortcut("Ctrl+P")
        # self.action_file_print.setStatusTip("Print file")
        
        self.action_file_exit=QtWidgets.QAction(QtGui.QIcon('Icons/exit.png'),"Exit",self)
        self.action_file_exit.setShortcut("Ctrl+Q")
        self.action_file_exit.setStatusTip("Exit application")
        self.action_file_exit.triggered.connect(self.close)
        # self.action_file_exit.setStatusTip("Exit application")


        
        # Tools actions
        self.action_tools=QtWidgets.QActionGroup(self)
        self.action_tools.setExclusive(True)

        # Add tool actions to the action group
        self.action_tools.addAction(self.action_tools_line)
        self.action_tools.addAction(self.action_tools_rectangle)
        self.action_tools.addAction(self.action_tools_ellipse)
        self.action_tools.addAction(self.action_tools_polygon)
        self.action_tools.addAction(self.action_tools_text)


        # Line tool
        self.action_tools_line=QtWidgets.QAction(
        self.tr("&Line"),self)
        self.action_tools_line.setCheckable(True)
        self.action_tools_line.setChecked(True)
        self.action_tools.addAction(self.action_tools_line)

        # Rectangle tool
        self.action_tools_rectangle=QtWidgets.QAction(
        self.tr("&Rectangle"),self)
        self.action_tools_rectangle.setCheckable(True)
        self.action_tools_rectangle.setChecked(True)
        self.action_tools.addAction(self.action_tools_rectangle)
        
        # Ellipse tool
        self.action_tools_ellipse=QtWidgets.QAction(
        self.tr("&Ellipse"),self)
        self.action_tools_ellipse.setCheckable(True)
        self.action_tools_ellipse.setChecked(True)
        self.action_tools.addAction(self.action_tools_ellipse)

        # Polygon tool
        self.action_tools_polygon=QtWidgets.QAction(
        self.tr("&Polygon"),self)
        self.action_tools_polygon.setCheckable(True)
        self.action_tools_polygon.setChecked(True)
        self.action_tools.addAction(self.action_tools_polygon)

        # Text tool
        self.action_tools_text=QtWidgets.QAction(
        self.tr("&Text"),self)
        self.action_tools_text.setCheckable(True)
        self.action_tools_text.setChecked(True)
        self.action_tools.addAction(self.action_tools_text)


        # Style actions    
        self.action_style_pen_color=QtWidgets.QAction(self.tr("&Color"),self)
        # Help actions    
    def connect_actions(self) :
        self.action_file_open.triggered.connect(self.file_open)

        self.action_file_save.triggered.connect(self.file_save)

        self.action_file_save_as.triggered.connect(self.file_save_as)

        # self.action_file_print.triggered.connect(self.file_print)

        self.action_file_exit.triggered.connect(self.close)

        self.action_tools_line.triggered.connect(
            lambda checked, tool="line": self.tools_selection(checked, tool)
        )
        self.action_tools_rectangle.triggered.connect(
            lambda checked, tool="rectangle": self.tools_selection(checked, tool)
        )
        self.action_tools_ellipse.triggered.connect(
            lambda checked, tool="ellipse": self.tools_selection(checked, tool)
        )
        self.action_tools_polygon.triggered.connect(
            lambda checked, tool="polygon": self.tools_selection(checked, tool)
        )
        self.action_tools_text.triggered.connect(
            lambda checked, tool="text": self.tools_selection(checked, tool)
        )

        self.action_style_pen_color.triggered.connect(self.style_pen_color_selection)

    # File actions implementation
    def file_open(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self,"Open File", os.getcwd())
        fileopen=QtCore.QFile(filename[0])
        print("open",fileopen)
    
    def file_save(self):
        filename = QtWidgets.QFileDialog.getSaveFileName(self,"Save File", os.getcwd())
        filesave=QtCore.QFile(filename[0])
        print("save",filesave)
    
    def file_save_as(self):
        filename = QtWidgets.QFileDialog.getSaveFileName(self,"Save File", os.getcwd())
        filesaveas=QtCore.QFile(filename[0])
        print("save as",filesaveas)
    
    # def file_print(self):
    #     filename = QtWidgets.QFileDialog.getSaveFileName(self,"Print File", os.getcwd())
    #     fileprint=QtCore.QFile(filename[0])
    #     print("print",fileprint)

    # def file_exit(self):
    #     self.close()
    #     print("exit")

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
        menu_file.addAction(self.action_file_save)
        menu_file.addAction(self.action_file_save_as)
        # menu_file.addAction(self.action_file_print)
        menu_file.addSeparator()
        menu_file.addAction(self.action_file_exit)
        menu_tool = menubar.addMenu('&Tools')
        menu_tool.addAction(self.action_tools_line)
        menu_tool.addAction(self.action_tools_rectangle)
        menu_tool.addAction(self.action_tools_ellipse)
        menu_tool.addAction(self.action_tools_polygon)
        menu_file.addSeparator()
        menu_tool.addAction(self.action_tools_text)
        

        menu_style= menubar.addMenu('&Style')
        menu_style_pen= menu_style.addMenu('&Pen')
        menu_style_pen.addAction(self.action_style_pen_color)

        # # Toolbar actions
        toolbar=self.addToolBar("File")
        toolbar.addAction(self.action_file_open)
        toolbar.addAction(self.action_file_save)
        toolbar.addAction(self.action_file_save_as)
        # toolbar.addAction(self.action_file_print)
        toolbar.addSeparator()
        toolbar.addAction(self.action_file_exit)
        toolbar=self.addToolBar("Tools")
        toolbar.addAction(self.action_tools_line)
        toolbar.addAction(self.action_tools_rectangle)
        toolbar.addAction(self.action_tools_ellipse)
        toolbar.addAction(self.action_tools_polygon)
        toolbar.addAction(self.action_tools_text)
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
