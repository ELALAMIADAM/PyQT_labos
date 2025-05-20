#!/usr/bin/python
import sys
from PyQt5 import QtCore,QtGui,QtWidgets
from PyQt5.QtGui import QPolygonF
from PyQt5.QtCore import Qt
import json

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
        self.tool="rectangle"
        self.item=None

        self.polygonPointsSets = []  # Initialize an empty list for sets of polygon points
        self.currentPolygonPoints = []  # Current working polygon points
        
        self.create_style()

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
    
    def set_pen_color(self,color) :
        print("View.set_pen_color(self,color)",color)
        self.pen.setColor(QtGui.QColor(color))
    def set_brush_color(self,color) :
        print("View.set_brush_color(self,color)",color)
        self.brush.setColor(QtGui.QColor(color))

    # Events
    # def mousePressEvent(self, event):
    #     print("View.mousePressEvent()")
    #     print("event.pos() : ",event.pos())
    #     print("event.screenPos() : ",event.screenPos())
    #     self.begin=self.end=event.pos()
    #     if self.scene() :
    #         self.item=self.scene().itemAt(self.begin,QtGui.QTransform())
    #         if self.item :
    #             self.offset =self.begin-self.item.pos()
    #     else :
    #         print("View need a scene to display items !!")

    def mousePressEvent(self, event):
        print("View.mousePressEvent()")
        print("event.pos() : ", event.pos())
        print("event.screenPos() : ", event.screenPos())
        self.begin = self.end = event.pos()
        if self.scene():
            self.item = self.scene().itemAt(self.begin, QtGui.QTransform())
            if self.item:
                self.offset = self.begin - self.item.pos()
            if self.tool == "polygon" and self.scene():
                # Add the clicked point to the current polygon
                self.currentPolygonPoints.append(event.pos())
                if len(self.currentPolygonPoints) > 1:
                    # Draw a temporary line between the last two points
                    temp_line = QtWidgets.QGraphicsLineItem(
                        QtCore.QLineF(self.currentPolygonPoints[-2], self.currentPolygonPoints[-1])
                    )
                    temp_line.setPen(self.pen)
                    self.scene().addItem(temp_line)

    def mouseDoubleClickEvent(self, event):
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
            self.polygonPointsSets.append(self.currentPolygonPoints)

            # Remove temporary lines
            for line in self.scene().items():
                if isinstance(line, QtWidgets.QGraphicsLineItem):
                    self.scene().removeItem(line)

            # Clear the current points list for a new polygon
            self.currentPolygonPoints = []


    def mouseMoveEvent(self, event):
        self.end=event.pos()
        if self.scene() :
            if self.item :
                self.item.setPos(event.pos() - self.offset)
            else :
                print("draw bounding box !")
        else :
            print("View need a scene to display items !!")
            
    def mouseReleaseEvent(self, event):
        print("View.mouseReleaseEvent()")
        print("nb items : ",len(self.items()))
        self.end=event.pos()        
        if self.scene() :
            if self.item :
                self.item.setPos(event.pos() - self.offset)
                self.item=None
            elif self.tool=="line" :
                line=QtWidgets.QGraphicsLineItem(self.begin.x(), self.begin.y(), self.end.x(), self.end.y())
                line.setPen(self.pen)
                self.scene().addItem(line)
            elif self.tool=="rectangle" :
                rect=QtWidgets.QGraphicsRectItem(
                                    self.begin.x(),self.begin.y(),
                                    abs(self.end.x()-self.begin.x()),
                                    abs(self.end.y()-self.begin.y())
                            )
                rect.setPen(self.pen)
                rect.setBrush(self.brush)
                self.scene().addItem(rect)
            elif self.tool=="ellipse" :
                ellipse=QtWidgets.QGraphicsEllipseItem(
                                    self.begin.x(),self.begin.y(),
                                    abs(self.end.x()-self.begin.x()),
                                    abs(self.end.y()-self.begin.y())
                            )
                ellipse.setPen(self.pen)
                ellipse.setBrush(self.brush)
                self.scene().addItem(ellipse)
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
                    text_item = EditableTextItem("Click to edit text")
                    text_item.setPos(event.pos())
                    text_item.setFont(QtGui.QFont("Arial", 20))
                    text_item.setDefaultTextColor(self.pen.color())
                    self.scene().addItem(text_item)
                    # Enable editing immediately after creation
                    text_item.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
                    text_item.setFocus(QtCore.Qt.MouseFocusReason)
                        
            else :
                print("nothing to draw !")
        else :
            print("View need a scene to display items !!")

    def resizeEvent(self,event):
        print("View.resizeEvent()")
        print("width : {}, height : {}".format(self.size().width(),self.size().height()))
   
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

    # Items
    offset=5
    xd,yd=offset,offset
    xf,yf=200+offset,100+offset
    line=QtWidgets.QGraphicsLineItem(xd,yd,xf,yf)
    line.setPen(view.get_pen())
    model.addItem(line)

    view.show()
    sys.exit(app.exec_())

