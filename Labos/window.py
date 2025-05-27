# -*- coding: utf-8 -*-
import os,sys
from PyQt5 import QtCore,QtGui,QtWidgets
from PyQt5.QtWidgets import QUndoCommand, QUndoStack, QColorDialog, QMessageBox, QTextEdit

from view import View
import json


class UndoableCommand(QUndoCommand):
    def __init__(self, description, do_func, undo_func):
        super().__init__(description)
        self.do_func = do_func
        self.undo_func = undo_func

    def redo(self):
        self.do_func()

    def undo(self):
        self.undo_func()

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
        self.undo_stack = QtWidgets.QUndoStack(self)
        self.data = []
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
        self.action_tools_rect=QtWidgets.QAction(QtGui.QIcon('Icons/tool_rectangle.png'),self.tr("&Rect"),self)
        self.action_tools_rect.setCheckable(True)
        self.action_tools.addAction(self.action_tools_rect)
        # Ellipse tool
        self.action_tools_ellip=QtWidgets.QAction(QtGui.QIcon('Icons/tool_ellipse.png'),self.tr("&Ellipse"),self)
        self.action_tools_ellip.setCheckable(True)
        self.action_tools.addAction(self.action_tools_ellip)
        # Poly tool
        self.action_tools_poly=QtWidgets.QAction(QtGui.QIcon('Icons/tool_polygon.png'),self.tr("&Polygon"),self)
        self.action_tools_poly.setCheckable(True)
        self.action_tools.addAction(self.action_tools_poly)
        # Text tool
        self.action_tools_text=QtWidgets.QAction(QtGui.QIcon('Icons/tool_text.png'),self.tr("&Text"),self)
        self.action_tools_text.setCheckable(True)
        self.action_tools.addAction(self.action_tools_text)


        # Style actions    
        self.action_style_pen_color=QtWidgets.QAction(QtGui.QIcon('Icons/colorize.png'),self.tr("&Color"),self)
        self.action_brush_color_style=QtWidgets.QAction(QtGui.QIcon('Icons/colorize.png'),self.tr("&Brush Color"),self)
        self.action_style_pen_line_solid=QtWidgets.QAction(self.tr("&Solid"),self)
        self.action_style_pen_line_dash=QtWidgets.QAction(self.tr("&Dash"),self)
        self.action_style_pen_line_dot=QtWidgets.QAction(self.tr("&Dot"),self)
        # self.action_style_pen_thickness=QtWidgets.QAction(self.tr("&Thickness"),self)
        # self.action_style_width_1=QtWidgets.QAction(self.tr("&Width 1"),self)
        # self.action_style_width_2=QtWidgets.QAction(self.tr("&Width 2"),self)
        self.action_set_width=QtWidgets.QAction(self.tr("&Width"),self)
        self.action_brush_fill_solid=QtWidgets.QAction(self.tr("&Solid"),self)
        self.action_brush_fill_dense=QtWidgets.QAction(self.tr("&Dense"),self)
        self.action_brush_fill_diag=QtWidgets.QAction(self.tr("&Diagonal"),self)
        self.action_set_font_family=QtWidgets.QAction(QtGui.QIcon('Icons/tool_font.png'),self.tr("&Font Family"),self)
        # Help
        self.action_help=QtWidgets.QActionGroup(self)
        self.action_help_aboutus=QtWidgets.QAction(self.tr("&About Us"),self)

        self.action_help_aboutqt = QtWidgets.QAction(self.tr("&About Qt"), self)
        self.action_help_aboutapp = QtWidgets.QAction(self.tr("&About the Application"), self)

        self.action_undo = QtWidgets.QAction("Undo", self)
        self.action_undo.setShortcut("Ctrl+Z")
        self.action_undo.triggered.connect(self.undo_stack.undo)

        self.action_redo = QtWidgets.QAction("Redo", self)
        self.action_redo.setShortcut("Ctrl+Shift+Z")
        self.action_redo.triggered.connect(self.undo_stack.redo)


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
        self.action_brush_color_style.triggered.connect(self.style_brush_color_selection)
        self.action_style_pen_line_solid.triggered.connect(lambda: self.view.change_pen_style(QtCore.Qt.SolidLine))
        self.action_style_pen_line_dash.triggered.connect(lambda: self.view.change_pen_style(QtCore.Qt.DashLine))
        self.action_style_pen_line_dot.triggered.connect(lambda: self.view.change_pen_style(QtCore.Qt.DotLine))
        self.action_set_width.triggered.connect(self.view.style_pen_thickness_selection)
        # self.action_style_width_1.triggered.connect(lambda: self.view.change_pen_width(1))
        # self.action_style_width_2.triggered.connect(lambda: self.view.change_pen_width(2))
        self.action_brush_fill_solid.triggered.connect(lambda: self.view.change_brush_style(QtCore.Qt.SolidPattern))
        self.action_brush_fill_dense.triggered.connect(lambda: self.view.change_brush_style(QtCore.Qt.Dense1Pattern))
        self.action_brush_fill_diag.triggered.connect(lambda: self.view.change_brush_style(QtCore.Qt.DiagCrossPattern))
        self.action_set_font_family.triggered.connect(self.view.style_font_family_selection)


        # Help actions
        self.action_help_aboutus.triggered.connect(self.about_us)

        self.action_help_aboutqt.triggered.connect(self.about_qt)
        self.action_help_aboutapp.triggered.connect(self.about_app)



    def add_item(self, item):
            # Define the do and undo functions
            def do_func():
                self.data.append(item)
                print(f"Added: {item}, Data: {self.data}")

            def undo_func():
                self.data.remove(item)
                print(f"Removed: {item}, Data: {self.data}")
            command = UndoableCommand(f"Add {item}", do_func, undo_func)
            self.undo_stack.push(command)


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


    def about_qt(self):
        QtWidgets.QMessageBox.aboutQt(self, "About Qt")

    def about_app(self):

        # Obtenir le chemin du fichier actuel (main.py)
        current_dir = os.path.dirname(__file__)

        # Aller dans le dossier parent (../)
        parent_dir = os.path.dirname(current_dir)

        # Construire le chemin vers README.md
        readme_path = os.path.join(parent_dir, "README.md")

        try:
            with open(readme_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            content = f"Erreur lors de la lecture du fichier README : {e}"

        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("About the Application")
        layout = QtWidgets.QVBoxLayout(dialog)

        text_area = QtWidgets.QTextEdit()
        text_area.setReadOnly(True)
        text_area.setText(content)
        layout.addWidget(text_area)

        close_button = QtWidgets.QPushButton("Close", dialog)
        close_button.clicked.connect(dialog.close)
        layout.addWidget(close_button)

        dialog.setLayout(layout)
        dialog.resize(600, 400)
        dialog.exec_()





    def file_open(self):
        # Open a file dialog to select a JSON file
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", os.getcwd(), "JSON Files (*.json);;All Files (*)")
        
        if filename:  # Check if a file was selected
            try:
                # Call the load_data function to load the scene
                self.load_data(filename)
                print(f"File opened and scene loaded: {filename}")
            except Exception as e:
                print(f"Error opening file: {e}")
    def load_data(self, file_name):
        try:
            with open(file_name, 'r') as json_file:
                scene_data = json.load(json_file)
            
            self.scene.clear()  # Clear the current scene before loading new data
            
            for item_data in scene_data:
                if item_data['type'] == 'rectangle':
                    rect_item = QtWidgets.QGraphicsRectItem(
                        item_data['x'], item_data['y'],
                        item_data['width'], item_data['height']
                    )
                    rect_item.setBrush(QtGui.QBrush(
                        QtGui.QColor(item_data['brush_color']), 
                        item_data['brush_pattern']
                    ))
                    rect_item.setPen(QtGui.QPen(
                        QtGui.QColor(item_data['pen_color']), 
                        item_data['pen_width']
                    ))
                    self.scene.addItem(rect_item)
                    
                elif item_data['type'] == 'line':
                    line_item = QtWidgets.QGraphicsLineItem(
                        item_data['x1'], item_data['y1'],
                        item_data['x2'], item_data['y2']
                    )
                    line_item.setPen(QtGui.QPen(
                        QtGui.QColor(item_data['pen_color']), 
                        item_data['pen_width'],
                        style=item_data.get('pen_style', QtCore.Qt.SolidLine)
                    ))
                    self.scene.addItem(line_item)
                    
                elif item_data['type'] == 'ellipse':
                    ellipse_item = QtWidgets.QGraphicsEllipseItem(
                        item_data['x'], item_data['y'],
                        item_data['width'], item_data['height']
                    )
                    ellipse_item.setBrush(QtGui.QBrush(
                        QtGui.QColor(item_data['brush_color']), 
                        item_data['brush_pattern']
                    ))
                    ellipse_item.setPen(QtGui.QPen(
                        QtGui.QColor(item_data['pen_color']), 
                        item_data['pen_width']
                    ))
                    self.scene.addItem(ellipse_item)
                    
                elif item_data['type'] == 'polygon':
                    polygon = QtGui.QPolygonF([
                        QtCore.QPointF(*point) for point in item_data['points']
                    ])
                    polygon_item = QtWidgets.QGraphicsPolygonItem(polygon)
                    polygon_item.setBrush(QtGui.QBrush(
                        QtGui.QColor(item_data['brush_color']), 
                        item_data['brush_pattern']
                    ))
                    polygon_item.setPen(QtGui.QPen(
                        QtGui.QColor(item_data['pen_color']), 
                        item_data['pen_width'],
                        style=item_data.get('pen_style', QtCore.Qt.SolidLine)
                    ))
                    self.scene.addItem(polygon_item)
                    
                else:  # text item
                    text_item = QtWidgets.QGraphicsTextItem(item_data['text'])
                    text_item.setFont(QtGui.QFont(
                        item_data['font_family'], 
                        item_data['font_size']
                    ))
                    text_item.setPos(item_data['x'], item_data['y'])
                    self.scene.addItem(text_item)
                    
        except FileNotFoundError:
            print(f"Error: File '{file_name}' not found")
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in file '{file_name}'")
        except KeyError as e:
            print(f"Error: Missing key {e} in JSON data")
        except Exception as e:
            print(f"Error loading data: {e}")

# Méthode de sauvegarde
    def file_save(self):
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save File", "", "JSON Files (*.json)"
        )
        if filename:
            self.save_scene_to_json(filename)

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
                    'brush_pattern': item.brush().style(),
                    'pen_color': item.pen().color().name(),
                    'pen_width': item.pen().width()
                })
            elif isinstance(item, QtWidgets.QGraphicsLineItem):
                scene_data.append({
                    'type': 'line',
                    'x1': item.line().x1(),
                    'y1': item.line().y1(),
                    'x2': item.line().x2(),
                    'y2': item.line().y2(),
                    'pen_color': item.pen().color().name(),
                    'pen_width': item.pen().width(),
                    'pen_style': item.pen().style()

                })
            elif isinstance(item, QtWidgets.QGraphicsEllipseItem):
                scene_data.append({
                    'type': 'ellipse',
                    'x': item.x(),
                    'y': item.y(),
                    'width': item.rect().width(),
                    'height': item.rect().height(),
                    'brush_color': item.brush().color().name(),
                    'brush_pattern': item.brush().style(),
                    'pen_color': item.pen().color().name(),
                    'pen_width': item.pen().width(),
                    'pen_style': item.pen().style()

                })
            elif isinstance(item, QtWidgets.QGraphicsPolygonItem):
                polygon_points = [(point.x(), point.y()) for point in item.polygon()]  # Corrected iteration
                scene_data.append({
                    'type': 'polygon',
                    'points': polygon_points,
                    'brush_color': item.brush().color().name(),
                    'brush_pattern': item.brush().style(),
                    'pen_color': item.pen().color().name(),
                    'pen_width': item.pen().width(),
                    'pen_style': item.pen().style()
                })
            elif isinstance(item, QtWidgets.QGraphicsTextItem):
                scene_data.append({
                    'type': 'text',
                    'x': item.x(),
                    'y': item.y(),
                    'text': item.toPlainText(),
                    'font_family': item.font().family(),
                    'font_size': item.font().pointSize()
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


    def file_exit(self):
        self.close()
        print("exit")

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
    def style_brush_color_selection(self):
        color = QtWidgets.QColorDialog.getColor(QtCore.Qt.green,self)
        if color.isValid() :
            self.view.set_brush_color(color.name())
    def style_pen_style_selection(self,style) :
        print("Window.style_pen_style_selection()")
        print("style : ",style)
        self.view.set_pen_style(style)


    def style_brush_style_selection(self,style) :
        print("Window.style_brush_style_selection()")
        print("style : ",style)
        self.view.set_brush_style(style)

    # def perform_action(self):
    #     # Example of adding a command to the undo stack
    #     def do_func():
    #         print("Action performed")

    #     def undo_func():
    #         print("Action undone")

    #     command = UndoableCommand("Perform Action", do_func, undo_func)
    #     self.undo_stack.push(command)
    

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
        menu_file.addAction(self.action_file_save_as)
        menu_file.addSeparator()
        menu_file.addAction(self.action_file_exit)
        menu_tool = menubar.addMenu('&Tools')
        menu_tool.addAction(self.action_tools_line)
        menu_tool.addAction(self.action_tools_rect)
        menu_tool.addAction(self.action_tools_ellip)
        menu_tool.addAction(self.action_tools_poly)
        menu_file.addSeparator()
        menu_tool.addAction(self.action_tools_text)
        
        
        # Style menu
        menu_style= menubar.addMenu('&Style')
        menu_style_pen= menu_style.addMenu('&Pen')
        menu_style_pen.addAction(self.action_style_pen_color)
        menu_style_pen_line= menu_style_pen.addMenu('&Line Style')
        menu_style_pen_line.addAction(self.action_style_pen_line_solid)
        menu_style_pen_line.addAction(self.action_style_pen_line_dash)
        menu_style_pen_line.addAction(self.action_style_pen_line_dot)
        # menu_style_pen_width= menu_style_pen.addMenu('&Width')
        menu_style_pen.addAction(self.action_set_width)
        # menu_style_pen_width.addAction(self.action_style_width_1)
        # menu_style_pen_width.addAction(self.action_style_width_2)
        menu_style_brush= menu_style.addMenu('&Brush')
        menu_style_brush.addAction(self.action_brush_color_style)
        menu_style_brush_fill= menu_style_brush.addMenu('&Fill Style')
        menu_style_brush_fill.addAction(self.action_brush_fill_solid)
        menu_style_brush_fill.addAction(self.action_brush_fill_dense)
        menu_style_brush_fill.addAction(self.action_brush_fill_diag)
        menu_style_font= menu_style.addMenu('&Font')
        menu_style_font.addAction(self.action_set_font_family)


        # Undo/Redo menu
        self.menu_edit = self.menuBar().addMenu("Edit")
        self.menu_edit.addAction(self.action_undo)
        self.menu_edit.addAction(self.action_redo)

        # Help menu
        menu_help = menubar.addMenu('&Help')
        menu_help.addAction(self.action_help_aboutus)
        menu_help.addAction(self.action_help_aboutqt)
        menu_help.addAction(self.action_help_aboutapp)


        # # Toolbar actions
        toolbar=self.addToolBar("File")
        toolbar.addAction(self.action_file_new)
        toolbar.addAction(self.action_file_open)
        toolbar.addAction(self.action_file_save)
        toolbar.addAction(self.action_file_save_as)
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

    # mw.add_Item
    mw.add_item("Items 1")
    mw.add_item("Items 2")
    

    offset=5
    xd,yd=offset,offset
    xf,yf=200+offset,100+offset
    line=QtWidgets.QGraphicsLineItem(xd,yd,xf,yf)
    line.setPen(mw.get_view().get_pen())
    mw.get_scene().addItem(line)

    mw.show()

    sys.exit(app.exec_())
