# ASCII Engine IDE

A Processing-like IDE for ASCII art programming with real-time preview.

## Features

- **Split-Screen Interface**: Code editor on the left, live animation preview on the right
- **Real-Time Preview**: See your animations update as you type
- **Syntax Highlighting**: Basic Python syntax highlighting for better code readability
- **Visible Cursor**: Blinking cursor with character highlighting for easy text editing
- **Processing-Style API**: Familiar `setup()` and `draw()` functions for animation
- **Built-in Examples**: Sample sketches to get you started
- **File Management**: Save and load your ASCII art sketches

## Usage

### Starting the IDE

```bash
python ascii_ide.py
```

### Keyboard Shortcuts

- **F5**: Run/restart your sketch
- **Ctrl+S**: Save current sketch
- **Ctrl+O**: Open sketch (placeholder)
- **Ctrl+Q**: Quit IDE
- **ESC**: Quit IDE
- **Arrow Keys**: Navigate code editor
- **Home/End**: Jump to line start/end

### Programming Model

Write your sketches using the Processing-style paradigm:

```python
# Global variables
x = 0
speed = 1

def setup():
    """Called once when the sketch starts"""
    global x
    x = canvas.cols // 2

def draw():
    """Called repeatedly to create animation"""
    global x, speed
    
    # Update position
    x += speed
    
    # Bounce off edges
    if x <= 0 or x >= canvas.cols:
        speed *= -1
    
    # Draw a moving circle
    canvas.circle(x, canvas.rows // 2, 3, color='yellow')
```

### Available Canvas Methods

The `canvas` object provides drawing methods:

- `canvas.circle(x, y, radius, filled=True, color='white')`
- `canvas.rect(x, y, width, height, filled=True, color='white')`
- `canvas.line(x1, y1, x2, y2, color='white')`
- `canvas.triangle(x1, y1, x2, y2, x3, y3, filled=True, color='white')`
- `canvas.ellipse(x, y, width, height, filled=True, color='white')`
- `canvas.arc(x, y, radius, start_angle, end_angle, color='white')`
- `canvas.bezier(x1, y1, cx1, cy1, cx2, cy2, x2, y2, color='white')`
- `canvas.set_pixel(row, col, char, color='white')`

### Available Colors

- `'red'`, `'green'`, `'blue'`
- `'yellow'`, `'magenta'`, `'cyan'`
- `'white'`, `'black'`

### Available Modules

Pre-imported in the execution environment:
- `math` - Mathematical functions
- `time` - Time-related functions  
- `randint` - Random integer function

## Example Sketches

Check the `examples/` directory for sample sketches:

- `bouncing_ball.py` - A ball bouncing around the screen
- `sine_wave.py` - Animated sine waves
- `spiral.py` - Expanding spiral animation
- `simple_shapes.py` - Random shapes demo

## Technical Details

- Built with Python's `curses` library for terminal UI
- Threaded execution for smooth editor performance
- Safe code execution in isolated namespace
- Real-time error display in preview pane
- Canvas size adapts to terminal dimensions

## Requirements

- Python 3.6+
- Terminal with curses support
- Minimum terminal size: 80x24 characters

## Troubleshooting

**IDE won't start**: Ensure you're running in a terminal that supports curses (not in IDE output panes)

**No animation**: Press F5 to run your sketch after making changes

**Syntax errors**: Check the preview pane for error messages

**Performance issues**: Reduce complexity in your `draw()` function or lower the frame rate