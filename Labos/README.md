# PyQt5 Graphics Editor - CAI 2425P

## Description
A comprehensive graphics editor built with PyQt5 that allows users to create, edit, and manipulate various geometric shapes and text elements. This application provides a complete interface for drawing operations with undo/redo functionality, style customization, and file management.

## Features

### Drawing Tools
- **Line Tool**: Draw straight lines between two points
- **Rectangle Tool**: Create rectangular shapes by dragging
- **Ellipse Tool**: Draw elliptical and circular shapes
- **Polygon Tool**: Create multi-point polygons (double-click to complete)
- **Text Tool**: Add and edit text elements

### Style Customization
- **Pen Settings**: 
  - Color selection via color picker
  - Line width adjustment (1-20 pixels)
  - Line styles: Solid, Dash, Dot, Dash-Dot, Dash-Dot-Dot
- **Brush Settings**:
  - Fill color selection
  - Fill patterns: Solid, Dense, Cross, Diagonal patterns
- **Font Settings**:
  - Font family selection from system fonts
  - Text color matches pen color

### Interface Features
- **Menu Bar**: Complete access to all application functions
- **Toolbar**: Quick access to frequently used tools
- **Context Menu**: Right-click menu for tools and styles within drawing area
- **Keyboard Shortcuts**:
  - Ctrl+N: New file
  - Ctrl+O: Open file
  - Ctrl+S: Save file
  - Ctrl+Shift+S: Save as
  - Ctrl+Q: Exit
  - Ctrl+Z: Undo
  - Ctrl+Shift+Z: Redo

### File Operations
- **New**: Clear the canvas (with confirmation dialog)
- **Open**: Load saved drawings from JSON format
- **Save**: Save current drawing to file
- **Save As**: Save with new filename
- **Export**: Save as image (PNG, JPG, etc.)

### Advanced Features
- **Undo/Redo**: Complete undo/redo stack for all operations
- **Object Selection**: Click and drag to move objects
- **Group Operations**: Select and move multiple objects
- **Warning Dialogs**: Confirmation for destructive operations

## Usage Instructions

### Basic Drawing
1. Select a tool from the Tools menu or toolbar
2. Click and drag on the canvas to create shapes
3. Release mouse to finalize the shape

### Polygon Drawing
1. Select the Polygon tool
2. Click to add points to the polygon
3. **Double-click** to complete and close the polygon
4. Temporary lines show the current polygon state

### Text Editing
1. Select the Text tool
2. Click where you want to add text
3. Type your text directly
4. Press **ESC** to finish editing
5. Click on existing text to edit it again

### Object Manipulation
- Click on any drawn object to select and move it
- Multiple objects can be selected and moved together
- Use Undo (Ctrl+Z) to reverse any operation

### Style Changes
- Changes to pen/brush settings affect new objects only
- Use the Style menu or context menu to modify settings
- Color dialogs provide full color selection

### File Management
- Save files in JSON format to preserve all object properties
- Open previously saved files to continue editing
- Export final drawings as image files

## Development Issues Encountered

### 1. Undo/Redo System Integration
**Problem**: The application had two separate undo stacks (one in Window, one in View) causing conflicts.

**Solution**: Unified the undo system by connecting the View's undo stack to the Window's undo stack, ensuring consistent behavior across the application.

### 2. Tool Selection Synchronization
**Problem**: Tool selection in the window menu wasn't properly synchronized with the view's active tool.

**Solution**: Enhanced the `tools_selection` method to properly communicate tool changes between the window and view components.

### 3. Polygon Tool Implementation
**Problem**: Polygon drawing lacked proper undo functionality and had issues with temporary line management.

**Solution**: Implemented comprehensive undo commands for polygon points and temporary lines, with proper cleanup during finalization.

### 4. Memory Management
**Problem**: Graphics items weren't properly managed during undo operations, leading to potential memory leaks.

**Solution**: Added proper scene membership checks before adding/removing items in undo/redo operations.

### 5. Context Menu Robustness
**Problem**: Context menu operations could crash if undo stack wasn't properly initialized.

**Solution**: Added null checks and proper error handling for all context menu operations.

### 6. Text Editing User Experience
**Problem**: Text editing interface wasn't intuitive for users.

**Solution**: Enhanced text editing with clear focus management and ESC key functionality for saving changes.

## Technical Architecture

### Main Components
- **window.py**: Main window class handling menus, toolbars, and file operations
- **view.py**: Graphics view handling drawing operations and user interactions
- **Utils/tools.py**: Enum definitions for drawing tools
- **Utils/**: Additional utility modules for specific functionality

### Design Patterns Used
- **Command Pattern**: For undo/redo functionality using QUndoCommand
- **Observer Pattern**: For tool selection synchronization
- **Factory Pattern**: For creating different types of graphics items

## Installation and Running

### Requirements
- Python 3.6+
- PyQt5

### Installation
```bash
pip install PyQt5
```

### Running the Application
```bash
python main.py
```

## Future Enhancements
- Layer support for complex drawings
- Export to vector formats (SVG)
- Grid and snap functionality
- Shape templates and symbols
- Improved selection tools (lasso, rectangular selection)
- Zoom and pan functionality
- Print support

## Credits
Developed for CAI 2425P course - PyQt5 Graphics Editor Project

## License
Educational use only - CAI 2425P Course Project 