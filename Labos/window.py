# -*- coding: utf-8 -*-
import os,sys
from PyQt5 import QtCore,QtGui,QtWidgets

from view import View
import json

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
        # File New
        self.action_file_new = QtWidgets.QAction(QtGui.QIcon('Icons/new.png'), "New", self)
        self.action_file_new.setShortcut("Ctrl+N")
        self.action_file_new.setStatusTip("Create new file")
        self.action_file_new.triggered.connect(self.file_new)

        # File Open
        self.action_file_open=QtWidgets.QAction(QtGui.QIcon('Icons/open.png'),"Open",self)
        self.action_file_open.setShortcut("Ctrl+O")
        self.action_file_open.setStatusTip("Open file")

        # File Save
        self.action_file_save=QtWidgets.QAction(QtGui.QIcon('Icons/save.png'),"Save",self)
        self.action_file_save.setShortcut("Ctrl+S")
        self.action_file_save.setStatusTip("Save file")

        # File Save As
        self.action_file_save_as=QtWidgets.QAction(QtGui.QIcon('Icons/save_as.png'),"Save as",self)
        self.action_file_save_as.setShortcut("Ctrl+Shift+S")
        self.action_file_save_as.setStatusTip("Save file as")

        # File Exit
        self.action_file_exit=QtWidgets.QAction(QtGui.QIcon('Icons/exit.png'),"Exit",self)
        self.action_file_exit.setShortcut("Ctrl+Q")
        self.action_file_exit.setStatusTip("Exit application")
        self.action_file_exit.triggered.connect(self.close)


        
         # Tools actions
        self.action_tools=QtWidgets.QActionGroup(self)
        # Line tool
        self.action_tools_line=QtWidgets.QAction(QtGui.QIcon('Icons/tool_line.png'),self.tr("&Line"),self)
        self.action_tools_line.setCheckable(True)
        self.action_tools_line.setChecked(True)
        self.action_tools.addAction(self.action_tools_line)
        # Rectangle tool
        self.action_tools_rect=QtWidgets.QAction(self.tr("&Rect"),self)
        self.action_tools_rect.setCheckable(True)
        self.action_tools.addAction(self.action_tools_rect)
        # Ellipse tool
        self.action_tools_ellip=QtWidgets.QAction(self.tr("&Ellipse"),self)
        self.action_tools_ellip.setCheckable(True)
        self.action_tools.addAction(self.action_tools_ellip)
        # Poly tool
        self.action_tools_poly=QtWidgets.QAction(self.tr("&Polygon"),self)
        self.action_tools_poly.setCheckable(True)
        self.action_tools.addAction(self.action_tools_poly)
        # Text tool
        self.action_tools_text=QtWidgets.QAction(self.tr("&Text"),self)
        self.action_tools_text.setCheckable(True)
        self.action_tools.addAction(self.action_tools_text)


        # Style actions    
        self.action_style_pen_color=QtWidgets.QAction(self.tr("&Color"),self)


        # # Style
        # self.action_style_pen_color.triggered.connect(self.style_pen_color_selection)
        # self.action_brush_color_style.triggered.connect(self.style_brush_color_selection)
        # self.action_pen_thickness.triggered.connect(self.style_pen_thickness_selection)
        # self.action_pen_solid.triggered.connect(lambda: self.change_pen_style(QtCore.Qt.SolidLine))
        # self.action_pen_dash.triggered.connect(lambda: self.change_pen_style(QtCore.Qt.DashLine))
        # self.action_pen_dot.triggered.connect(lambda: self.change_pen_style(QtCore.Qt.DotLine))

        # self.action_brush_solid.triggered.connect(lambda: self.change_brush_style(QtCore.Qt.SolidPattern))
        # self.action_brush_dense.triggered.connect(lambda: self.change_brush_style(QtCore.Qt.Dense1Pattern))
        # self.action_brush_diag.triggered.connect(lambda: self.change_brush_style(QtCore.Qt.DiagCrossPattern))
        # Help
        self.action_help=QtWidgets.QActionGroup(self)
        self.action_help_aboutus=QtWidgets.QAction(self.tr("&About Us"),self)

        # Help actions    
    def connect_actions(self) :
        self.action_file_new.triggered.connect(self.file_new)

        self.action_file_open.triggered.connect(self.file_open)

        self.action_file_save.triggered.connect(self.file_save)

        self.action_file_save_as.triggered.connect(self.file_save_as)

        

        self.action_file_exit.triggered.connect(self.close)

        self.action_tools_line.triggered.connect(
            lambda checked, tool="line": self.tools_selection(checked, tool)
        )
        self.action_tools_rect.triggered.connect(
            lambda checked, tool="rectangle": self.tools_selection(checked, tool)
        )
        self.action_tools_ellip.triggered.connect(
            lambda checked, tool="ellipse": self.tools_selection(checked, tool)
        )
        self.action_tools_poly.triggered.connect(
            lambda checked, tool="polygon": self.tools_selection(checked, tool)
        )
        self.action_tools_text.triggered.connect(
            lambda checked, tool="text": self.tools_selection(checked, tool)
        )

        self.action_style_pen_color.triggered.connect(self.style_pen_color_selection)

        self.action_help_aboutus.triggered.connect(self.about_us)

    # File actions implementation
    def file_new(self):
        reply = QtWidgets.QMessageBox.warning(self, "Warning", 
                                            "Are you sure you want to create a new file? Unsaved changes will be lost.", 
                                            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            # Logique pour créer un nouveau fichier
            self.scene.clear()  # Efface tous les éléments de la scène
            self.image_counter = 1  # Réinitialise le compteur d'image
            print("New file created")
        else:
            print("New file creation cancelled.")

    def about_us(self):
        # Create a dialog
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("About Us")
        layout = QtWidgets.QVBoxLayout(dialog)
        about_text = QtWidgets.QLabel("Realise par :\n\n "
                                    "- EL ALAMI ADAM\n"
                                    "- MOHAMAD Moustafa\n")
        about_text.setWordWrap(True)
        layout.addWidget(about_text)
        close_button = QtWidgets.QPushButton("Close", dialog)
        close_button.clicked.connect(dialog.close)
        layout.addWidget(close_button)
        dialog.setLayout(layout)
        dialog.exec_()


    def file_open(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self,"Open File", os.getcwd())
        fileopen=QtCore.QFile(filename[0])
        print("open",fileopen)

# Méthode de sauvegarde
    def file_save(self):
        try:
            # Demander à l'utilisateur de choisir un emplacement de sauvegarde
            directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory to Save File")
            
            if not directory:  # Vérifiez si le répertoire est vide
                print("No directory selected. Save operation cancelled.")
                return  # Quittez la méthode si le répertoire est vide

            # Créer un menu pour choisir le type de fichier à sauvegarder
            file_type, _ = QtWidgets.QInputDialog.getItem(self, "Choose File Type", 
                "Select the type of file to save:", ["Image", "JSON"], 0, False)
            
            if not file_type:  # Vérifiez si aucune option n'est sélectionnée
                print("No file type selected. Save operation cancelled.")
                return

            if file_type == "Image":
                # Créez le nom de fichier basé sur le compteur
                file_name = os.path.join(directory, f"image_{self.image_counter}.png")
                
                # Incrémenter le compteur pour le prochain enregistrement
                self.image_counter += 1

                # Créer une image vide avec la taille de la scène
                rect = self.scene.sceneRect()
                image = QtGui.QImage(rect.size().toSize(), QtGui.QImage.Format_ARGB32)
                image.fill(QtCore.Qt.white)  # Remplir l'image avec du blanc

                # Créer un paint device pour dessiner sur l'image
                painter = QtGui.QPainter(image)
                
                # Dessiner la scène sur l'image
                self.scene.render(painter)
                painter.end()

                # Vérifiez si l'image est valide
                if image.isNull():
                    print("Image is null, cannot save.")
                    return

                # Enregistrer l'image
                if not image.save(file_name):
                    print(f"Failed to save the image as: {file_name}")
                else:
                    print(f"Image saved as: {file_name}")
            
            elif file_type == "JSON":
                file_name = os.path.join(directory, f"scene_{self.image_counter}.json")
                self.save_scene_to_json(file_name)  # Appeler une méthode pour sauvegarder la scène en JSON

        except Exception as e:
            print(f"Error while saving the file: {e}")

    def save_scene_to_json(self, file_name):
        scene_data = []  # Liste pour stocker les données de la scène

        for item in self.scene.items():
            if isinstance(item, QtWidgets.QGraphicsRectItem):
                scene_data.append({
                    'type': 'rectangle',
                    'x': item.x(),
                    'y': item.y(),
                    'width': item.rect().width(),
                    'height': item.rect().height(),
                    'brush_color': item.brush().color().name(),
                    'brush_pattern': item.brush().style()
                })
            elif isinstance(item, QtWidgets.QGraphicsLineItem):
                scene_data.append({
                    'type': 'line',
                    'x1': item.line().x1(),
                    'y1': item.line().y1(),
                    'x2': item.line().x2(),
                    'y2': item.line().y2(),
                    'pen_color': item.pen().color().name(),
                    'pen_width': item.pen().width()
                })
            # Ajoutez d'autres types d'éléments si nécessaire

        # Sauvegarder les données de la scène dans un fichier JSON
        with open(file_name, 'w') as json_file:
            json.dump(scene_data, json_file, indent=4)
        print(f"Scene saved as JSON: {file_name}")

    def file_save_as(self):
        try:
            # Demander à l'utilisateur de choisir un emplacement et un nom de fichier
            options = QtWidgets.QFileDialog.Options()
            file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File As", "", 
                "Images (*.png *.jpg *.bmp);;JSON Files (*.json);;All Files (*)", options=options)
            
            if file_name:
                if file_name.endswith('.json'):
                    self.save_scene_to_json(file_name)  # Appeler la méthode pour sauvegarder la scène en JSON
                else:
                    # Créer une image vide avec la taille de la scène
                    rect = self.scene.sceneRect()
                    image = QtGui.QImage(rect.size().toSize(), QtGui.QImage.Format_ARGB32)
                    image.fill(QtCore.Qt.white)  # Remplir l'image avec du blanc

                    # Créer un paint device pour dessiner sur l'image
                    painter = QtGui.QPainter(image)
                    
                    # Dessiner la scène sur l'image
                    self.scene.render(painter)
                    painter.end()

                    # Vérifiez si l'image est valide
                    if image.isNull():
                        print("Image is null, cannot save.")
                        return

                    # Enregistrer l'image
                    if not image.save(file_name):
                        print(f"Failed to save the image as: {file_name}")
                    else:
                        print(f"Image saved as: {file_name}")
        except Exception as e:
            print(f"Error while saving the file: {e}")


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
        menu_file.addAction(self.action_file_new)
        menu_file.addAction(self.action_file_open)
        menu_file.addAction(self.action_file_save)
        # menu_file.addAction(self.action_file_save_as)
        # menu_file.addAction(self.action_file_print)
        menu_file.addSeparator()
        menu_file.addAction(self.action_file_exit)
        menu_tool = menubar.addMenu('&Tools')
        menu_tool.addAction(self.action_tools_line)
        menu_tool.addAction(self.action_tools_rect)
        menu_tool.addAction(self.action_tools_ellip)
        menu_tool.addAction(self.action_tools_poly)
        menu_file.addSeparator()
        menu_tool.addAction(self.action_tools_text)
        
        

        menu_style= menubar.addMenu('&Style')
        menu_style_pen= menu_style.addMenu('&Pen')
        menu_style_pen.addAction(self.action_style_pen_color)

        menu_help = menubar.addMenu('&Help')
        menu_help.addAction(self.action_help_aboutus)

        # # Toolbar actions
        toolbar=self.addToolBar("File")
        toolbar.addAction(self.action_file_new)
        toolbar.addAction(self.action_file_open)
        toolbar.addAction(self.action_file_save)
        # toolbar.addAction(self.action_file_save_as)
        # toolbar.addAction(self.action_file_print)
        toolbar.addSeparator()
        toolbar.addAction(self.action_file_exit)
        toolbar=self.addToolBar("Tools")
        toolbar.addAction(self.action_tools_line)
        toolbar.addAction(self.action_tools_rect)
        toolbar.addAction(self.action_tools_ellip)
        toolbar.addAction(self.action_tools_poly)
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
