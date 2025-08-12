import os
import sys
import time
import math
from random import randint, choice

# Add parent directory to path to import ascii_engine
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from ascii_engine.main import Canvas

class MidiDemoCanvas(Canvas):
    """Demo version without MIDI dependency"""
    
    def __init__(self, rows, cols):
        super().__init__(rows, cols)
        self.shapes = []
        self.max_shapes = 15
        
        # Note to color mapping
        self.note_colors = {
            0: 'red', 1: 'magenta', 2: 'yellow', 3: 'white',
            4: 'green', 5: 'cyan', 6: 'blue', 7: 'red',
            8: 'magenta', 9: 'yellow', 10: 'green', 11: 'cyan'
        }
        
        self.shape_types = ['circle', 'rect', 'line', 'triangle', 'star']
        
    def add_shape(self, note, velocity):
        """Add a shape based on simulated MIDI input"""
        color = self.note_colors[note % 12]
        size = max(2, int(velocity / 127.0 * 12))
        
        shape = {
            'type': choice(self.shape_types),
            'x': randint(size + 2, self.cols - size - 2),
            'y': randint(size + 2, self.rows - size - 2),
            'size': size,
            'color': color,
            'note': note,
            'age': 0,
            'max_age': max(20, int(velocity / 3))
        }
        
        self.shapes.append(shape)
        
        if len(self.shapes) > self.max_shapes:
            self.shapes.pop(0)
    
    def update_shapes(self):
        """Update shapes"""
        self.shapes = [s for s in self.shapes if s['age'] < s['max_age']]
        for shape in self.shapes:
            shape['age'] += 1
    
    def draw_shape(self, shape):
        """Draw a single shape"""
        x, y = shape['x'], shape['y']
        size = shape['size']
        color = shape['color']
        shape_type = shape['type']
        
        try:
            if shape_type == 'circle':
                self.circle(x, y, size, filled=True, color=color)
            elif shape_type == 'rect':
                self.rect(x - size, y - size//2, size*2, size, filled=True, color=color)
            elif shape_type == 'line':
                for angle in range(0, 360, 45):
                    end_x = x + int(size * math.cos(math.radians(angle)))
                    end_y = y + int(size * math.sin(math.radians(angle)))
                    self.line(x, y, end_x, end_y, color=color)
            elif shape_type == 'triangle':
                points = []
                for i in range(3):
                    angle = i * 120 * math.pi / 180
                    px = x + int(size * math.cos(angle))
                    py = y + int(size * math.sin(angle))
                    points.append((px, py))
                self.triangle(points[0][0], points[0][1], 
                            points[1][0], points[1][1],
                            points[2][0], points[2][1], 
                            filled=True, color=color)
            elif shape_type == 'star':
                for angle in range(0, 360, 30):
                    radius = size if angle % 60 == 0 else size // 2
                    end_x = x + int(radius * math.cos(math.radians(angle)))
                    end_y = y + int(radius * math.sin(math.radians(angle)))
                    self.line(x, y, end_x, end_y, color=color)
        except:
            pass
    
    def draw_shapes(self):
        """Draw all shapes"""
        for shape in self.shapes:
            self.draw_shape(shape)

def run_demo():
    """Run MIDI reactive shapes demo"""
    print("🎵 MIDI Reactive Shapes - Demo Mode 🎵")
    print("=" * 50)
    print("Simulating MIDI input with random notes")
    print("Shows colored shapes based on musical notes")
    print("Press Ctrl+C to exit\n")
    
    canvas = MidiDemoCanvas(50, 150)
    frame_count = 0
    notes_played = 0
    
    # Musical scale for more pleasant demo
    scale_notes = [60, 62, 64, 65, 67, 69, 71, 72]  # C major scale
    
    try:
        while True:
            canvas.clear()
            
            # Add new shape every few frames
            if frame_count % 8 == 0:
                note = choice(scale_notes) + randint(-12, 12)  # Add some variation
                velocity = randint(60, 127)
                canvas.add_shape(note, velocity)
                notes_played += 1
            
            # Update and draw
            canvas.update_shapes()
            canvas.draw_shapes()
            
            # Draw info
            title = "MIDI REACTIVE SHAPES - DEMO"
            for i, char in enumerate(title[:canvas.cols-4]):
                canvas.set_pixel(1, i + 2, char, 'white')
            
            info = f"Notes: {notes_played}  Shapes: {len(canvas.shapes)}"
            for i, char in enumerate(info[:canvas.cols-4]):
                canvas.set_pixel(3, i + 2, char, 'yellow')
            
            # Color legend
            legend = "Colors: C=Red D=Yellow E=Green F=Cyan G=Blue A=Magenta"
            for i, char in enumerate(legend[:canvas.cols-4]):
                canvas.set_pixel(canvas.rows-2, i + 2, char, 'cyan')
            
            canvas.draw()
            time.sleep(1/15)  # 15 FPS
            frame_count += 1
            
    except KeyboardInterrupt:
        print(f"\n\nDemo stopped! Notes played: {notes_played}")

if __name__ == "__main__":
    run_demo()