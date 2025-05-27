# -*- coding: utf-8 -*-
import os,sys
from PyQt5 import QtCore,QtGui,QtWidgets
from PyQt5.QtWidgets import QUndoCommand, QUndoStack, QColorDialog, QMessageBox, QTextEdit

from view import View, EditableTextItem
from Utils.tools import Tool
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
        
        # Connect view's undo stack to window's undo stack
        self.view.undo_stack = self.undo_stack
        
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
        # Get the current directory path 
        current_dir = os.path.dirname(__file__)
        
        # Construct the path to README.md in the same directory
        readme_path = os.path.join(current_dir, "README.md")

        try:
            with open(readme_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            content = f"Error reading README file: {e}\n\nREADME.md should be in the same directory as this application."

        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("About the Application")
        layout = QtWidgets.QVBoxLayout(dialog)

        text_area = QtWidgets.QTextEdit()
        text_area.setReadOnly(True)
        text_area.setPlainText(content)  # Use setPlainText for better markdown display
        layout.addWidget(text_area)

        close_button = QtWidgets.QPushButton("Close", dialog)
        close_button.clicked.connect(dialog.close)
        layout.addWidget(close_button)

        dialog.setLayout(layout)
        dialog.resize(800, 600)  # Make it larger for better readability
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
                item = None
                
                if item_data['type'] == 'rectangle':
                    # Create rectangle item
                    item = QtWidgets.QGraphicsRectItem(
                        item_data['x'], item_data['y'],
                        item_data['width'], item_data['height']
                    )
                    
                    # Set complete pen properties
                    pen = QtGui.QPen()
                    pen.setColor(QtGui.QColor(item_data['pen_color']))
                    pen.setWidthF(item_data.get('pen_width', 1.0))
                    pen.setStyle(item_data.get('pen_style', QtCore.Qt.SolidLine))
                    pen.setCapStyle(item_data.get('pen_cap_style', QtCore.Qt.SquareCap))
                    pen.setJoinStyle(item_data.get('pen_join_style', QtCore.Qt.BevelJoin))
                    pen.setMiterLimit(item_data.get('pen_miter_limit', 2.0))
                    item.setPen(pen)
                    
                    # Set complete brush properties
                    brush = QtGui.QBrush()
                    brush.setColor(QtGui.QColor(item_data['brush_color']))
                    brush.setStyle(item_data.get('brush_style', QtCore.Qt.SolidPattern))
                    item.setBrush(brush)
                    
                elif item_data['type'] == 'line':
                    # Create line item
                    item = QtWidgets.QGraphicsLineItem(
                        item_data['x1'], item_data['y1'],
                        item_data['x2'], item_data['y2']
                    )
                    
                    # Set complete pen properties
                    pen = QtGui.QPen()
                    pen.setColor(QtGui.QColor(item_data['pen_color']))
                    pen.setWidthF(item_data.get('pen_width', 1.0))
                    pen.setStyle(item_data.get('pen_style', QtCore.Qt.SolidLine))
                    pen.setCapStyle(item_data.get('pen_cap_style', QtCore.Qt.SquareCap))
                    pen.setJoinStyle(item_data.get('pen_join_style', QtCore.Qt.BevelJoin))
                    pen.setMiterLimit(item_data.get('pen_miter_limit', 2.0))
                    item.setPen(pen)
                    
                elif item_data['type'] == 'ellipse':
                    # Create ellipse item
                    item = QtWidgets.QGraphicsEllipseItem(
                        item_data['x'], item_data['y'],
                        item_data['width'], item_data['height']
                    )
                    
                    # Set complete pen properties
                    pen = QtGui.QPen()
                    pen.setColor(QtGui.QColor(item_data['pen_color']))
                    pen.setWidthF(item_data.get('pen_width', 1.0))
                    pen.setStyle(item_data.get('pen_style', QtCore.Qt.SolidLine))
                    pen.setCapStyle(item_data.get('pen_cap_style', QtCore.Qt.SquareCap))
                    pen.setJoinStyle(item_data.get('pen_join_style', QtCore.Qt.BevelJoin))
                    pen.setMiterLimit(item_data.get('pen_miter_limit', 2.0))
                    item.setPen(pen)
                    
                    # Set complete brush properties
                    brush = QtGui.QBrush()
                    brush.setColor(QtGui.QColor(item_data['brush_color']))
                    brush.setStyle(item_data.get('brush_style', QtCore.Qt.SolidPattern))
                    item.setBrush(brush)
                    
                elif item_data['type'] == 'polygon':
                    # Create polygon item
                    polygon = QtGui.QPolygonF([
                        QtCore.QPointF(*point) for point in item_data['points']
                    ])
                    item = QtWidgets.QGraphicsPolygonItem(polygon)
                    
                    # Set complete pen properties
                    pen = QtGui.QPen()
                    pen.setColor(QtGui.QColor(item_data['pen_color']))
                    pen.setWidthF(item_data.get('pen_width', 1.0))
                    pen.setStyle(item_data.get('pen_style', QtCore.Qt.SolidLine))
                    pen.setCapStyle(item_data.get('pen_cap_style', QtCore.Qt.SquareCap))
                    pen.setJoinStyle(item_data.get('pen_join_style', QtCore.Qt.BevelJoin))
                    pen.setMiterLimit(item_data.get('pen_miter_limit', 2.0))
                    item.setPen(pen)
                    
                    # Set complete brush properties
                    brush = QtGui.QBrush()
                    brush.setColor(QtGui.QColor(item_data['brush_color']))
                    brush.setStyle(item_data.get('brush_style', QtCore.Qt.SolidPattern))
                    item.setBrush(brush)
                    
                elif item_data['type'] == 'text':
                    # Create editable text item
                    item = EditableTextItem(item_data['text'])
                    
                    # Set complete font properties
                    font = QtGui.QFont()
                    font.setFamily(item_data.get('font_family', 'Arial'))
                    font.setPointSize(item_data.get('font_size', 12))
                    font.setWeight(item_data.get('font_weight', QtGui.QFont.Normal))
                    font.setItalic(item_data.get('font_italic', False))
                    font.setUnderline(item_data.get('font_underline', False))
                    font.setBold(item_data.get('font_bold', False))
                    font.setStrikeOut(item_data.get('font_strikeout', False))
                    item.setFont(font)
                    
                    # Set text color
                    text_color = QtGui.QColor(item_data.get('text_color', '#000000'))
                    item.setDefaultTextColor(text_color)
                    
                    # Set text alignment if available
                    if 'text_alignment' in item_data:
                        cursor = item.textCursor()
                        block_format = cursor.blockFormat()
                        block_format.setAlignment(QtCore.Qt.Alignment(item_data['text_alignment']))
                        cursor.setBlockFormat(block_format)
                        item.setTextCursor(cursor)
                
                # Apply common properties to all items
                if item:
                    # Set position (use new pos_x/pos_y if available, fallback to old x/y)
                    pos_x = item_data.get('pos_x', item_data.get('x', 0))
                    pos_y = item_data.get('pos_y', item_data.get('y', 0))
                    item.setPos(pos_x, pos_y)
                    
                    # Set transformation properties
                    if 'z_value' in item_data:
                        item.setZValue(item_data['z_value'])
                    if 'opacity' in item_data:
                        item.setOpacity(item_data['opacity'])
                    if 'visible' in item_data:
                        item.setVisible(item_data['visible'])
                    if 'rotation' in item_data:
                        item.setRotation(item_data['rotation'])
                    
                    # Set scale if available
                    scale_x = item_data.get('scale_x', 1.0)
                    scale_y = item_data.get('scale_y', 1.0)
                    if scale_x != 1.0 or scale_y != 1.0:
                        item.setScale(scale_x)  # Note: QGraphicsItem uses uniform scaling
                    
                    # Add item to scene
                    self.scene.addItem(item)
                    
            print(f"Loaded {len(scene_data)} items with complete parameters")
                    
        except FileNotFoundError:
            print(f"Error: File '{file_name}' not found")
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in file '{file_name}'")
        except KeyError as e:
            print(f"Error: Missing key {e} in JSON data")
        except Exception as e:
            print(f"Error loading data: {e}")
            import traceback
            traceback.print_exc()

# Méthode de sauvegarde
    def file_save(self):
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save File", "", "JSON Files (*.json)"
        )
        if filename:
            self.save_scene_to_json(filename)

    def save_scene_to_json(self, file_name):
        scene_data = []  # List to store scene data

        for item in self.scene.items():
            # Common properties for all items
            common_props = {
                'z_value': item.zValue(),
                'opacity': item.opacity(),
                'visible': item.isVisible(),
                'rotation': item.rotation(),
                'scale_x': item.transform().m11(),
                'scale_y': item.transform().m22(),
                'pos_x': item.x(),
                'pos_y': item.y()
            }
            
            if isinstance(item, QtWidgets.QGraphicsRectItem):
                pen = item.pen()
                brush = item.brush()
                scene_data.append({
                    'type': 'rectangle',
                    'x': item.rect().x(),
                    'y': item.rect().y(),
                    'width': item.rect().width(),
                    'height': item.rect().height(),
                    # Complete pen properties
                    'pen_color': pen.color().name(),
                    'pen_width': pen.widthF(),
                    'pen_style': pen.style(),
                    'pen_cap_style': pen.capStyle(),
                    'pen_join_style': pen.joinStyle(),
                    'pen_miter_limit': pen.miterLimit(),
                    # Complete brush properties
                    'brush_color': brush.color().name(),
                    'brush_style': brush.style(),
                    **common_props
                })
                
            elif isinstance(item, QtWidgets.QGraphicsLineItem):
                pen = item.pen()
                line = item.line()
                scene_data.append({
                    'type': 'line',
                    'x1': line.x1(),
                    'y1': line.y1(),
                    'x2': line.x2(),
                    'y2': line.y2(),
                    # Complete pen properties
                    'pen_color': pen.color().name(),
                    'pen_width': pen.widthF(),
                    'pen_style': pen.style(),
                    'pen_cap_style': pen.capStyle(),
                    'pen_join_style': pen.joinStyle(),
                    'pen_miter_limit': pen.miterLimit(),
                    **common_props
                })
                
            elif isinstance(item, QtWidgets.QGraphicsEllipseItem):
                pen = item.pen()
                brush = item.brush()
                scene_data.append({
                    'type': 'ellipse',
                    'x': item.rect().x(),
                    'y': item.rect().y(),
                    'width': item.rect().width(),
                    'height': item.rect().height(),
                    # Complete pen properties
                    'pen_color': pen.color().name(),
                    'pen_width': pen.widthF(),
                    'pen_style': pen.style(),
                    'pen_cap_style': pen.capStyle(),
                    'pen_join_style': pen.joinStyle(),
                    'pen_miter_limit': pen.miterLimit(),
                    # Complete brush properties
                    'brush_color': brush.color().name(),
                    'brush_style': brush.style(),
                    **common_props
                })
                
            elif isinstance(item, QtWidgets.QGraphicsPolygonItem):
                pen = item.pen()
                brush = item.brush()
                polygon_points = [(point.x(), point.y()) for point in item.polygon()]
                scene_data.append({
                    'type': 'polygon',
                    'points': polygon_points,
                    # Complete pen properties
                    'pen_color': pen.color().name(),
                    'pen_width': pen.widthF(),
                    'pen_style': pen.style(),
                    'pen_cap_style': pen.capStyle(),
                    'pen_join_style': pen.joinStyle(),
                    'pen_miter_limit': pen.miterLimit(),
                    # Complete brush properties
                    'brush_color': brush.color().name(),
                    'brush_style': brush.style(),
                    **common_props
                })
                
            elif isinstance(item, (QtWidgets.QGraphicsTextItem, EditableTextItem)):
                font = item.font()
                scene_data.append({
                    'type': 'text',
                    'text': item.toPlainText(),
                    # Complete font properties
                    'font_family': font.family(),
                    'font_size': font.pointSize(),
                    'font_weight': font.weight(),
                    'font_italic': font.italic(),
                    'font_underline': font.underline(),
                    'font_bold': font.bold(),
                    'font_strikeout': font.strikeOut(),
                    # Text color
                    'text_color': item.defaultTextColor().name(),
                    # Text alignment (if available)
                    'text_alignment': int(item.textCursor().blockFormat().alignment()) if hasattr(item, 'textCursor') else 0,
                    **common_props
                })

        # Save scene data to JSON file
        with open(file_name, 'w') as json_file:
            json.dump(scene_data, json_file, indent=4)
        print(f"Scene saved as JSON: {file_name}")
        print(f"Saved {len(scene_data)} items with complete parameters")

    def file_save_as(self):
        try:
            # Ask user to choose location and filename
            options = QtWidgets.QFileDialog.Options()
            file_name, selected_filter = QtWidgets.QFileDialog.getSaveFileName(
                self, "Save File As", "", 
                "JSON Files (*.json);;PNG Images (*.png);;JPEG Images (*.jpg);;BMP Images (*.bmp);;All Files (*)", 
                options=options
            )
            
            if file_name:
                # Determine file type based on extension or selected filter
                if file_name.lower().endswith('.json') or 'JSON' in selected_filter:
                    # Ensure .json extension
                    if not file_name.lower().endswith('.json'):
                        file_name += '.json'
                    self.save_scene_to_json(file_name)
                    QtWidgets.QMessageBox.information(self, "Success", f"Scene saved as JSON: {file_name}")
                    
                else:
                    # Handle image export
                    # Ensure proper extension based on selected filter
                    if 'PNG' in selected_filter and not file_name.lower().endswith('.png'):
                        file_name += '.png'
                    elif 'JPEG' in selected_filter and not file_name.lower().endswith(('.jpg', '.jpeg')):
                        file_name += '.jpg'
                    elif 'BMP' in selected_filter and not file_name.lower().endswith('.bmp'):
                        file_name += '.bmp'
                    
                    # Create image with scene size
                    rect = self.scene.sceneRect()
                    if rect.isEmpty():
                        # If scene rect is empty, use a default size
                        rect = QtCore.QRectF(0, 0, 800, 600)
                    
                    # Create image with high quality
                    image = QtGui.QImage(
                        int(rect.width()), 
                        int(rect.height()), 
                        QtGui.QImage.Format_ARGB32_Premultiplied
                    )
                    image.fill(QtCore.Qt.white)  # Fill with white background

                    # Create painter for rendering
                    painter = QtGui.QPainter(image)
                    painter.setRenderHint(QtGui.QPainter.Antialiasing)
                    painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)
                    
                    # Render scene to image
                    self.scene.render(painter, QtCore.QRectF(image.rect()), rect)
                    painter.end()

                    # Save image
                    if image.save(file_name):
                        QtWidgets.QMessageBox.information(self, "Success", f"Image saved as: {file_name}")
                        print(f"Image saved successfully: {file_name}")
                    else:
                        QtWidgets.QMessageBox.warning(self, "Error", f"Failed to save image: {file_name}")
                        print(f"Failed to save image: {file_name}")
                        
        except Exception as e:
            error_msg = f"Error while saving file: {str(e)}"
            QtWidgets.QMessageBox.critical(self, "Save Error", error_msg)
            print(error_msg)


    def file_exit(self):
        self.close()
        print("exit")

    # Tools actions implementation
    def tools_selection(self,checked,tool) :
        print("Window.tools_selection(self,checked,tool)",checked,tool)
        if checked:
            self.view.set_tool(tool)
        return

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
