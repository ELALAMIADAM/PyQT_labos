#!/usr/bin/python
import sys
from PyQt5 import QtCore,QtGui,QtWidgets
from PyQt5.QtGui import QPolygonF
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QUndoCommand
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

class EditableTextItem(QtWidgets.QGraphicsTextItem):
    def __init__(self, text="click to edit text, and press ESC to save"):
        super().__init__(text)
        self.setFlag(QtWidgets.QGraphicsTextItem.ItemIsSelectable)
        self.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)

    def focusOutEvent(self, event):
        self.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        # Save the edited text when focus is lost
        self.saveText()
        super().focusOutEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            # Save the edited text when the Escape key is pressed
            self.saveText()
            self.clearFocus()  # Remove focus to end editing
        else:
            super().keyPressEvent(event)

    def saveText(self):
        edited_text = self.toPlainText()
        # Here, you can implement the logic to save the edited text.
        # For example, you can update a variable, emit a signal, or
        # save the text to a file/database.
        print("Saved text:", edited_text)

class View (QtWidgets.QGraphicsView) :
    def __init__(self,position=(0,0),dimension=(600,400)):
        QtWidgets.QGraphicsView.__init__(self)
        x,y=position
        w,h=dimension
        self.setGeometry(x,y,w,h)

        self.begin,self.end=QtCore.QPoint(0,0),QtCore.QPoint(0,0)
        self.offset=QtCore.QPoint(0,0)
        self.pen,self.brush=None,None
        self.tool="line"  # Default tool is line
        self.item=None
        self.preview_item=None  # For elastic drawing

        self.polygonPointsSets = []  # Initialize an empty list for sets of polygon points
        self.currentPolygonPoints = []  # Current working polygon points
        
        self.create_style()
        self.thickness=1.0
        self.selected_font_family = "Arial"  # Default font family
        # undo_stack will be set by the parent window
        self.undo_stack = None

    def __repr__(self):
        return "<View({},{},{})>".format(self.pen,self.brush,self.tool)
    
    def get_pen(self) :
        return self.pen
    def set_pen(self,pen) :
        self.pen=pen
    def set_pen_color(self,color) :
        print("View.set_pen_color(self,color)",color)
        self.pen.setColor(QtGui.QColor(color))
    def get_brush(self) :
        return self.brush
    def set_brush(self,brush) :
        self.brush=brush
    def set_brush_color(self,color) :
        print("View.set_brush_color(self,color)",color)
        self.brush.setColor(QtGui.QColor(color))

    def get_tool(self) :
        return self.tool
    def set_tool(self,tool) :
        print("View.set_tool(self,tool)",tool)
        self.tool=tool

    def create_style(self) :
        self.create_pen()
        self.create_brush()
    def create_pen(self) :
        self.pen=QtGui.QPen()
        self.pen.setColor(QtCore.Qt.red)
    def create_brush(self) :
        self.brush=QtGui.QBrush()
        self.brush.setColor(QtCore.Qt.blue)
        self.brush.setStyle(QtCore.Qt.CrossPattern)
    def set_pen_thickness(self,thickness) :
        print("View.set_pen_thickness(self,thickness)",thickness)
        if isinstance(thickness, (int, float)) and thickness >= 0:
            self.pen.setWidthF(float(thickness))
        else:
            print("Invalid pen thickness:", thickness)
    
    def set_pen_color(self,color) :
        print("View.set_pen_color(self,color)",color)
        self.pen.setColor(QtGui.QColor(color))
    def set_brush_color(self,color) :
        print("View.set_brush_color(self,color)",color)
        self.brush.setColor(QtGui.QColor(color))
    def change_pen_style(self,style) :
        print("View.change_pen_style(self,style)",style)
        if style in [QtCore.Qt.SolidLine, QtCore.Qt.DashLine, QtCore.Qt.DotLine, QtCore.Qt.DashDotLine, QtCore.Qt.DashDotDotLine]:
            self.pen.setStyle(style)
        else:
            print("Invalid pen style:", style)
    def change_brush_style(self,style) :
        print("View.change_brush_style(self,style)",style)
        if style in [QtCore.Qt.SolidPattern, QtCore.Qt.Dense1Pattern, QtCore.Qt.Dense2Pattern, QtCore.Qt.Dense3Pattern,
                     QtCore.Qt.Dense4Pattern, QtCore.Qt.Dense5Pattern, QtCore.Qt.Dense6Pattern, QtCore.Qt.Dense7Pattern,
                     QtCore.Qt.HorPattern, QtCore.Qt.VerPattern, QtCore.Qt.CrossPattern, QtCore.Qt.BDiagPattern,
                     QtCore.Qt.FDiagPattern, QtCore.Qt.DiagCrossPattern]:
            self.brush.setStyle(style)
        else:
            print("Invalid brush style:", style)
    # def change_pen_width(self,width) :
    #     print("View.change_pen_width(self,width)",width)
    #     if isinstance(width, (int, float)) and width >= 0:
    #         self.pen.setWidthF(float(width))
    #     else:
    #         print("Invalid pen width:", width)
    def change_pen_cap_style(self,cap_style) :
        print("View.change_pen_cap_style(self,cap_style)",cap_style)
        if cap_style in [QtCore.Qt.FlatCap, QtCore.Qt.SquareCap, QtCore.Qt.RoundCap]:
            self.pen.setCapStyle(cap_style)
        else:
            print("Invalid pen cap style:", cap_style)
    
    
    def set_pen_style(self,style) :
        print("View.set_pen_style(self,style)",style)
        if style in [QtCore.Qt.SolidLine, QtCore.Qt.DashLine, QtCore.Qt.DotLine, QtCore.Qt.DashDotLine, QtCore.Qt.DashDotDotLine]:
            self.pen.setStyle(style)
        else:
            print("Invalid pen style:", style)
    def set_brush_style(self,style) :
        print("View.set_brush_style(self,style)",style)
        if style in [QtCore.Qt.SolidPattern, QtCore.Qt.Dense1Pattern, QtCore.Qt.Dense2Pattern, QtCore.Qt.Dense3Pattern,
                     QtCore.Qt.Dense4Pattern, QtCore.Qt.Dense5Pattern, QtCore.Qt.Dense6Pattern, QtCore.Qt.Dense7Pattern,
                     QtCore.Qt.HorPattern, QtCore.Qt.VerPattern, QtCore.Qt.CrossPattern, QtCore.Qt.BDiagPattern,
                     QtCore.Qt.FDiagPattern, QtCore.Qt.DiagCrossPattern]:
            self.brush.setStyle(style)
        else:
            print("Invalid brush style:", style)
    def set_pen_width(self,width) :
        print("View.set_pen_width(self,width)",width)
        if isinstance(width, (int, float)) and width >= 0:
            self.pen.setWidthF(float(width))
        else:
            print("Invalid pen width:", width)
    
    def change_font_family(self,family) :
        print("View.change_font_family(self,family)",family)
        if isinstance(family, str):
            font = self.font()
            font.setFamily(family)
            self.setFont(font)
        else:
            print("Invalid font family:", family)
    
    def style_font_family_selection(self):
        print("View.style_font_family_selection()")
        font_db = QtGui.QFontDatabase()  # Create an instance of QFontDatabase
        families = font_db.families()  # Get the list of font families
        family, ok = QtWidgets.QInputDialog.getItem(self, "Select Font Family", "Font Family:", families)
        if ok and family:
            self.selected_font_family = family
    
    
    def style_pen_thickness_selection(self):
        print("Window.style_pen_thickness_selection()")
        thickness, ok = QtWidgets.QInputDialog.getInt(self, "Pen Thickness", "Enter pen thickness:", 1, 1, 10)
        if ok:
            self.set_pen_thickness(thickness)
    
    def mousePressEvent(self, event):
        # Only handle left-click for drawing operations
        if event.button() != QtCore.Qt.LeftButton:
            return
            
        print("View.mousePressEvent()")
        print("event.pos() : ", event.pos())
        print("event.screenPos() : ", event.screenPos())
        self.begin = self.end = event.pos()
        if self.scene():
            self.item = self.scene().itemAt(self.begin, QtGui.QTransform())
            if self.item:
                self.offset = self.begin - self.item.pos()
            if self.tool == "polygon" and self.scene() and self.undo_stack:
                # Add the clicked point to the current polygon
                new_point = event.pos()
                self.currentPolygonPoints.append(new_point)

                if len(self.currentPolygonPoints) > 1:
                    # Draw a temporary line between the last two points
                    temp_line = QtWidgets.QGraphicsLineItem(
                        QtCore.QLineF(self.currentPolygonPoints[-2], self.currentPolygonPoints[-1])
                    )
                    temp_line.setPen(self.pen)
                    self.scene().addItem(temp_line)

                    # Define undo and redo functions
                    def do_func():
                        if new_point not in self.currentPolygonPoints:
                            self.currentPolygonPoints.append(new_point)
                        if temp_line.scene() is None:
                            self.scene().addItem(temp_line)
                        print("DO: Added point and temporary line")

                    def undo_func():
                        if new_point in self.currentPolygonPoints:
                            self.currentPolygonPoints.remove(new_point)
                        if temp_line.scene() is not None:
                            self.scene().removeItem(temp_line)
                        print("UNDO: Removed point and temporary line")

                    # Create and push the command to the undo stack
                    command = UndoableCommand("Add Polygon Point", do_func, undo_func)
                    self.undo_stack.push(command)

    def mouseDoubleClickEvent(self, event):
        # Only handle left-click for drawing operations
        if event.button() != QtCore.Qt.LeftButton:
            return
            
        if self.tool == "polygon":
            self.finalizeCurrentPolygon()


    def finalizeCurrentPolygon(self):
        # Finalize the current polygon
        if self.tool == "polygon" and self.scene() and self.currentPolygonPoints:
            polygon = QPolygonF(self.currentPolygonPoints)
            polygonItem = QtWidgets.QGraphicsPolygonItem(polygon)
            polygonItem.setPen(self.pen)
            polygonItem.setBrush(self.brush)
            self.scene().addItem(polygonItem)
            self.polygonPointsSets.append(self.currentPolygonPoints.copy())

            # Remove temporary lines
            temp_lines = []
            for line in self.scene().items():
                if isinstance(line, QtWidgets.QGraphicsLineItem):
                    temp_lines.append(line)
                    self.scene().removeItem(line)

            # Add undo functionality
            if self.undo_stack:
                points_copy = self.currentPolygonPoints.copy()
                def do_func():
                    if polygonItem.scene() is None:
                        self.scene().addItem(polygonItem)
                    if points_copy not in self.polygonPointsSets:
                        self.polygonPointsSets.append(points_copy)
                def undo_func():
                    if polygonItem.scene() is not None:
                        self.scene().removeItem(polygonItem)
                    if points_copy in self.polygonPointsSets:
                        self.polygonPointsSets.remove(points_copy)
                    # Restore temporary lines
                    for line in temp_lines:
                        if line.scene() is None:
                            self.scene().addItem(line)
                command = UndoableCommand("Draw Polygon", do_func, undo_func)
                self.undo_stack.push(command)

            # Clear the current points list for a new polygon
            self.currentPolygonPoints = []


    def mouseMoveEvent(self, event):
        self.end=event.pos()
        if self.scene() :
            if self.item :
                self.item.setPos(event.pos() - self.offset)
            else :
                # Only show elastic drawing if we started with a left-click
                # Check if left button is currently pressed for drawing operations
                if event.buttons() & QtCore.Qt.LeftButton:
                    # Elastic drawing - show preview during drawing
                    if self.preview_item:
                        self.scene().removeItem(self.preview_item)
                        self.preview_item = None
                    
                    # Create preview item with simple outline only
                    preview_pen = QtGui.QPen(QtCore.Qt.gray)
                    preview_pen.setStyle(QtCore.Qt.DashLine)
                    preview_pen.setWidth(1)
                    
                    if self.tool == "line":
                        self.preview_item = QtWidgets.QGraphicsLineItem(
                            self.begin.x(), self.begin.y(), self.end.x(), self.end.y()
                        )
                        self.preview_item.setPen(preview_pen)
                        self.scene().addItem(self.preview_item)
                        
                    elif self.tool == "rectangle":
                        self.preview_item = QtWidgets.QGraphicsRectItem(
                            self.begin.x(), self.begin.y(),
                            abs(self.end.x() - self.begin.x()),
                            abs(self.end.y() - self.begin.y())
                        )
                        self.preview_item.setPen(preview_pen)
                        self.scene().addItem(self.preview_item)
                        
                    elif self.tool == "ellipse":
                        self.preview_item = QtWidgets.QGraphicsEllipseItem(
                            self.begin.x(), self.begin.y(),
                            abs(self.end.x() - self.begin.x()),
                            abs(self.end.y() - self.begin.y())
                        )
                        self.preview_item.setPen(preview_pen)
                        self.scene().addItem(self.preview_item)
        else :
            print("View need a scene to display items !!")
            
    def mouseReleaseEvent(self, event):
        # Only handle left-click release for drawing operations
        if event.button() != QtCore.Qt.LeftButton:
            return
            
        print("View.mouseReleaseEvent()")
        print("nb items : ",len(self.items()))
        self.end=event.pos()
        
        # Clean up preview item
        if self.preview_item:
            self.scene().removeItem(self.preview_item)
            self.preview_item = None
            
        if self.scene() :
            if self.item :
                self.item.setPos(event.pos() - self.offset)
                self.item=None
            elif self.tool=="line" :
                # Create final styled line
                line=QtWidgets.QGraphicsLineItem(self.begin.x(), self.begin.y(), self.end.x(), self.end.y())
                line.setPen(self.pen)
                self.scene().addItem(line)
                
                # Add undo functionality
                if self.undo_stack:
                    def do_func():
                        if line.scene() is None:
                            self.scene().addItem(line)
                    def undo_func():
                        if line.scene() is not None:
                            self.scene().removeItem(line)
                    command = UndoableCommand("Draw Line", do_func, undo_func)
                    self.undo_stack.push(command)
                    
            elif self.tool=="rectangle" :
                rect=QtWidgets.QGraphicsRectItem(
                                    self.begin.x(),self.begin.y(),
                                    abs(self.end.x()-self.begin.x()),
                                    abs(self.end.y()-self.begin.y())
                            )
                rect.setPen(self.pen)
                rect.setBrush(self.brush)
                self.scene().addItem(rect)
                
                # Add undo functionality
                if self.undo_stack:
                    def do_func():
                        if rect.scene() is None:
                            self.scene().addItem(rect)
                    def undo_func():
                        if rect.scene() is not None:
                            self.scene().removeItem(rect)
                    command = UndoableCommand("Draw Rectangle", do_func, undo_func)
                    self.undo_stack.push(command)
                    
            elif self.tool=="ellipse" :
                ellipse=QtWidgets.QGraphicsEllipseItem(
                                    self.begin.x(),self.begin.y(),
                                    abs(self.end.x()-self.begin.x()),
                                    abs(self.end.y()-self.begin.y())
                            )
                ellipse.setPen(self.pen)
                ellipse.setBrush(self.brush)
                self.scene().addItem(ellipse)
                
                # Add undo functionality
                if self.undo_stack:
                    def do_func():
                        if ellipse.scene() is None:
                            self.scene().addItem(ellipse)
                    def undo_func():
                        if ellipse.scene() is not None:
                            self.scene().removeItem(ellipse)
                    command = UndoableCommand("Draw Ellipse", do_func, undo_func)
                    self.undo_stack.push(command)

            elif self.tool == "polygon" and self.scene():
                # If the user releases the mouse while drawing a polygon, update the temporary line
                if len(self.currentPolygonPoints) > 0:
                    temp_line = QtWidgets.QGraphicsLineItem(
                        QtCore.QLineF(self.currentPolygonPoints[-1], self.end)
                    )
                    temp_line.setPen(self.pen)
                    self.scene().addItem(temp_line)
                


            elif self.tool == 'text':
                # Check if there's an existing text item at the clicked position
                text_item = self.scene().itemAt(event.pos(), QtGui.QTransform())
                if isinstance(text_item, EditableTextItem):
                    # Enable editing for the existing text item
                    text_item.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
                    text_item.setFocus(QtCore.Qt.MouseFocusReason)
                else:
                    # Create a new editable text item if none exists
                    text_item = EditableTextItem("edit text")
                    text_item.setPos(event.pos())
                    text_item.setFont(QtGui.QFont(self.selected_font_family, 20))
                    text_item.setDefaultTextColor(self.pen.color())
                    self.scene().addItem(text_item)
                    # Enable editing immediately after creation
                    text_item.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
                    text_item.setFocus(QtCore.Qt.MouseFocusReason)
                    
                    # Add undo functionality for new text items
                    if self.undo_stack:
                        def do_func():
                            if text_item.scene() is None:
                                self.scene().addItem(text_item)
                        def undo_func():
                            if text_item.scene() is not None:
                                self.scene().removeItem(text_item)
                        command = UndoableCommand("Add Text", do_func, undo_func)
                        self.undo_stack.push(command)
                        
            else :
                print("nothing to draw !")
        else :
            print("View need a scene to display items !!")

    def resizeEvent(self,event):
        print("View.resizeEvent()")
        print("width : {}, height : {}".format(self.size().width(),self.size().height()))
   

    def contextMenuEvent(self, event):
        menu = QtWidgets.QMenu()
        
        # Tools submenu (referring to action bar tools)
        tools_menu = menu.addMenu("Tools")
        line_action = tools_menu.addAction("Line")
        rect_action = tools_menu.addAction("Rectangle")
        ellipse_action = tools_menu.addAction("Ellipse")
        polygon_action = tools_menu.addAction("Polygon")
        text_action = tools_menu.addAction("Text")
        
        # Style submenu (referring to action bar styles)
        style_menu = menu.addMenu("Style")
        pen_menu = style_menu.addMenu("Pen")
        pen_color_action = pen_menu.addAction("Color")
        pen_width_action = pen_menu.addAction("Width")
        pen_style_action = pen_menu.addAction("Style")
        
        brush_menu = style_menu.addMenu("Brush")
        brush_color_action = brush_menu.addAction("Color")
        brush_style_action = brush_menu.addAction("Fill")
        
        # Separator line
        menu.addSeparator()
        
        # Erase action with warning dialog
        erase_action = menu.addAction("Erase")
        
        # Execute menu
        action = menu.exec_(event.globalPos())
        
        # Handle tool selection
        if action == line_action:
            self.set_tool("line")
        elif action == rect_action:
            self.set_tool("rectangle")
        elif action == ellipse_action:
            self.set_tool("ellipse")
        elif action == polygon_action:
            self.set_tool("polygon")
        elif action == text_action:
            self.set_tool("text")
        # Handle style actions
        elif action == pen_color_action:
            color = QtWidgets.QColorDialog.getColor()
            if color.isValid():
                self.set_pen_color(color)
        elif action == pen_width_action:
            width, ok = QtWidgets.QInputDialog.getInt(self, "Pen Width", "Enter width:", 
                                                 self.pen.width(), 1, 20)
            if ok:
                self.set_pen_width(width)
        elif action == pen_style_action:
            styles = {
                "Solid": QtCore.Qt.SolidLine,
                "Dash": QtCore.Qt.DashLine,
                "Dot": QtCore.Qt.DotLine,
                "Dash Dot": QtCore.Qt.DashDotLine,
                "Dash Dot Dot": QtCore.Qt.DashDotDotLine
            }
            style, ok = QtWidgets.QInputDialog.getItem(self, "Pen Style", 
                                                  "Select style:", styles.keys(), 0, False)
            if ok and style:
                self.set_pen_style(styles[style])
        elif action == brush_color_action:
            color = QtWidgets.QColorDialog.getColor()
            if color.isValid():
                self.set_brush_color(color)
        elif action == brush_style_action:
            styles = {
                "Solid": QtCore.Qt.SolidPattern,
                "Dense1": QtCore.Qt.Dense1Pattern,
                "Dense2": QtCore.Qt.Dense2Pattern,
                "Dense3": QtCore.Qt.Dense3Pattern,
                "Dense4": QtCore.Qt.Dense4Pattern,
                "Dense5": QtCore.Qt.Dense5Pattern,
                "Dense6": QtCore.Qt.Dense6Pattern,
                "Dense7": QtCore.Qt.Dense7Pattern,
                "Horizontal": QtCore.Qt.HorPattern,
                "Vertical": QtCore.Qt.VerPattern,
                "Cross": QtCore.Qt.CrossPattern,
                "BDiag": QtCore.Qt.BDiagPattern,
                "FDiag": QtCore.Qt.FDiagPattern,
                "DiagCross": QtCore.Qt.DiagCrossPattern
            }
            style, ok = QtWidgets.QInputDialog.getItem(self, "Brush Style", 
                                                  "Select style:", styles.keys(), 0, False)
            if ok and style:
                self.set_brush_style(styles[style])
        # Handle erase action
        elif action == erase_action:
            reply = QtWidgets.QMessageBox.warning(self, "Warning", 
                                             "Are you sure you want to erase everything?", 
                                             QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                try:
                    scene = self.scene()
                    if scene is not None:
                        scene.clear()
                    
                    if hasattr(self, 'undo_stack') and self.undo_stack:
                        self.undo_stack.clear()
                        
                    # Clear polygon points
                    self.currentPolygonPoints = []
                    self.polygonPointsSets = []
                    
                except Exception as e:
                    QtWidgets.QMessageBox.critical(
                        self,
                        "Error",
                        f"An error occurred while erasing: {str(e)}"
                    )






if __name__ == "__main__" :  

    print(QtCore.QT_VERSION_STR)
    app=QtWidgets.QApplication(sys.argv)

    # View
    x,y=0,0
    w,h=600,400
    view=View(position=(x,y),dimension=(w,h))
    view.setWindowTitle("CAI 2425P  : View")

    # Scene
    model=QtWidgets.QGraphicsScene()
    model.setSceneRect(x,y,w,h)
    view.setScene(model)

    addItem=QtWidgets.QGraphicsRectItem(0,0,100,100)

    # Items
    offset=5
    xd,yd=offset,offset
    xf,yf=200+offset,100+offset
    line=QtWidgets.QGraphicsLineItem(xd,yd,xf,yf)
    line.setPen(view.get_pen())
    model.addItem(line)

    view.show()
    sys.exit(app.exec_())

