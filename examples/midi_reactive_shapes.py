import os
import sys
import time
import math
import threading
from random import randint, choice

# Add parent directory to path to import ascii_engine
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from ascii_engine.main import Canvas

try:
    import mido
except ImportError:
    print("Error: mido library not found!")
    print("Please install with: pip install mido")
    print("For MIDI backend support, also install:")
    print("  - macOS: pip install python-rtmidi")
    print("  - Linux: pip install python-rtmidi")
    print("  - Windows: pip install python-rtmidi")
    sys.exit(1)

class MidiReactiveCanvas(Canvas):
    """Canvas that reacts to MIDI input with visual shapes"""
    
    def __init__(self, rows, cols):
        super().__init__(rows, cols)
        self.midi_shapes = []  # Store active shapes
        self.max_shapes = 20   # Maximum shapes on screen
        self.shape_decay = 0.1 # How fast shapes fade
        
        # MIDI note to color mapping (12-tone chromatic scale)
        # Using only standard ANSI colors available in the Canvas
        self.note_colors = {
            0: 'red',        # C
            1: 'magenta',    # C#
            2: 'yellow',     # D
            3: 'white',      # D#
            4: 'green',      # E
            5: 'cyan',       # F
            6: 'blue',       # F#
            7: 'red',        # G
            8: 'magenta',    # G#
            9: 'yellow',     # A
            10: 'green',     # A#
            11: 'cyan'       # B
        }
        
        # Extended colors for higher contrast (using only available colors)
        self.extended_colors = [
            'red', 'yellow', 'green', 'cyan', 'blue', 'magenta', 'white', 'black'
        ]
        
        # Shape types
        self.shape_types = ['circle', 'rect', 'line', 'triangle', 'star']
        
    def add_midi_shape(self, note, velocity, channel=0):
        """Add a new shape based on MIDI input"""
        # Map note to color (using modulo 12 for chromatic scale)
        color_index = note % 12
        color = self.note_colors.get(color_index, 'white')
        
        # Map velocity to size and intensity
        size = max(2, int(velocity / 127.0 * 15))  # Size 2-15 based on velocity
        alpha = velocity / 127.0  # Transparency based on velocity
        
        # Map channel to shape type
        shape_type = self.shape_types[channel % len(self.shape_types)]
        
        # Random position
        x = randint(size + 2, self.cols - size - 2)
        y = randint(size + 2, self.rows - size - 2)
        
        # Create shape data
        shape = {
            'type': shape_type,
            'x': x,
            'y': y,
            'size': size,
            'color': color,
            'note': note,
            'velocity': velocity,
            'channel': channel,
            'age': 0,
            'max_age': max(30, int(velocity / 2)),  # Longer life for louder notes
            'alpha': alpha
        }
        
        self.midi_shapes.append(shape)
        
        # Remove oldest shapes if too many
        if len(self.midi_shapes) > self.max_shapes:
            self.midi_shapes.pop(0)
    
    def update_shapes(self):
        """Update all active shapes (aging, fading)"""
        shapes_to_remove = []
        
        for i, shape in enumerate(self.midi_shapes):
            shape['age'] += 1
            
            # Mark for removal if too old
            if shape['age'] > shape['max_age']:
                shapes_to_remove.append(i)
        
        # Remove old shapes (in reverse order to maintain indices)
        for i in reversed(shapes_to_remove):
            self.midi_shapes.pop(i)
    
    def draw_midi_shape(self, shape):
        """Draw a single MIDI-triggered shape"""
        x, y = shape['x'], shape['y']
        size = shape['size']
        color = shape['color']
        shape_type = shape['type']
        age_ratio = shape['age'] / shape['max_age']
        
        # Modify appearance based on age (fade effect)
        if age_ratio > 0.7:  # Start fading in last 30% of life
            # Use dimmer colors for fading effect
            if 'bright_' not in color:
                pass  # Keep normal color
            else:
                pass  # Could implement actual fading here
        
        try:
            if shape_type == 'circle':
                self.circle(x, y, size, filled=True, color=color)
            
            elif shape_type == 'rect':
                width = size * 2
                height = size
                self.rect(x - width//2, y - height//2, width, height, filled=True, color=color)
            
            elif shape_type == 'line':
                # Draw radiating lines from center
                for angle in range(0, 360, 45):
                    end_x = x + int(size * math.cos(math.radians(angle)))
                    end_y = y + int(size * math.sin(math.radians(angle)))
                    self.line(x, y, end_x, end_y, color=color)
            
            elif shape_type == 'triangle':
                # Simple triangle using lines
                points = []
                for i in range(3):
                    angle = i * 120 * math.pi / 180
                    px = x + int(size * math.cos(angle))
                    py = y + int(size * math.sin(angle))
                    points.append((px, py))
                
                if len(points) == 3:
                    self.triangle(points[0][0], points[0][1], 
                                points[1][0], points[1][1],
                                points[2][0], points[2][1], 
                                filled=True, color=color)
            
            elif shape_type == 'star':
                # Draw star pattern with lines
                for angle in range(0, 360, 30):
                    radius = size if angle % 60 == 0 else size // 2
                    end_x = x + int(radius * math.cos(math.radians(angle)))
                    end_y = y + int(radius * math.sin(math.radians(angle)))
                    self.line(x, y, end_x, end_y, color=color)
        
        except Exception as e:
            # Skip drawing if coordinates are out of bounds
            pass
    
    def draw_shapes(self):
        """Draw all active MIDI shapes"""
        for shape in self.midi_shapes:
            self.draw_midi_shape(shape)
    
    def get_note_name(self, note):
        """Convert MIDI note number to note name"""
        note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        octave = (note // 12) - 1
        note_name = note_names[note % 12]
        return f"{note_name}{octave}"

class MidiVisualizer:
    """Main MIDI visualizer application"""
    
    def __init__(self):
        self.canvas = MidiReactiveCanvas(50, 150)
        self.running = False
        self.midi_input = None
        self.stats = {
            'notes_played': 0,
            'last_note': None,
            'last_velocity': 0,
            'last_channel': 0
        }
    
    def list_midi_ports(self):
        """List available MIDI input ports"""
        print("Available MIDI input ports:")
        input_ports = mido.get_input_names()
        
        if not input_ports:
            print("  No MIDI input ports found!")
            print("  Make sure a MIDI device is connected.")
            return []
        
        for i, port in enumerate(input_ports):
            print(f"  {i}: {port}")
        
        return input_ports
    
    def select_midi_port(self):
        """Let user select MIDI input port"""
        ports = self.list_midi_ports()
        
        if not ports:
            return None
        
        if len(ports) == 1:
            print(f"\nUsing MIDI port: {ports[0]}")
            return ports[0]
        
        while True:
            try:
                choice = input(f"\nSelect MIDI port (0-{len(ports)-1}), or 'v' for virtual port: ")
                
                if choice.lower() == 'v':
                    print("Creating virtual MIDI port 'ASCII Engine Input'...")
                    return 'virtual'
                
                port_index = int(choice)
                if 0 <= port_index < len(ports):
                    return ports[port_index]
                else:
                    print("Invalid selection. Try again.")
            
            except ValueError:
                print("Invalid input. Enter a number or 'v' for virtual port.")
            except KeyboardInterrupt:
                return None
    
    def midi_callback(self, message):
        """Handle incoming MIDI messages"""
        if message.type == 'note_on' and message.velocity > 0:
            # Note on with velocity > 0
            self.canvas.add_midi_shape(
                note=message.note,
                velocity=message.velocity,
                channel=message.channel
            )
            
            # Update stats
            self.stats['notes_played'] += 1
            self.stats['last_note'] = message.note
            self.stats['last_velocity'] = message.velocity
            self.stats['last_channel'] = message.channel
            
        elif message.type == 'note_off' or (message.type == 'note_on' and message.velocity == 0):
            # Note off - could implement note-off effects here
            pass
        
        elif message.type == 'control_change':
            # Control change - could map to visual effects
            if message.control == 1:  # Modulation wheel
                # Could affect shape behavior
                pass
    
    def midi_listener_thread(self):
        """Thread function for listening to MIDI messages"""
        try:
            while self.running:
                if self.midi_input:
                    # Process pending MIDI messages
                    for message in self.midi_input.iter_pending():
                        self.midi_callback(message)
                
                time.sleep(0.001)  # Small delay to prevent busy waiting
                
        except Exception as e:
            print(f"MIDI listener error: {e}")
    
    def draw_ui(self):
        """Draw user interface information"""
        # Draw stats in top-left corner
        info_lines = [
            f"Notes: {self.stats['notes_played']}",
            f"Shapes: {len(self.canvas.midi_shapes)}",
        ]
        
        if self.stats['last_note'] is not None:
            note_name = self.canvas.get_note_name(self.stats['last_note'])
            info_lines.extend([
                f"Last: {note_name} ({self.stats['last_note']})",
                f"Vel: {self.stats['last_velocity']}",
                f"Ch: {self.stats['last_channel'] + 1}"
            ])
        
        for i, line in enumerate(info_lines):
            for j, char in enumerate(line[:20]):  # Limit to 20 chars
                if i < self.canvas.rows - 2 and j < self.canvas.cols - 2:
                    self.canvas.set_pixel(i + 1, j + 1, char, 'white')
        
        # Draw color legend
        legend_y = self.canvas.rows - 8
        legend_x = 2
        
        legend_title = "Note Colors:"
        for i, char in enumerate(legend_title):
            if legend_x + i < self.canvas.cols - 2:
                self.canvas.set_pixel(legend_y, legend_x + i, char, 'white')
        
        note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        for i, (note_name, color) in enumerate(zip(note_names, self.canvas.note_colors.values())):
            y = legend_y + 1 + i // 6
            x = legend_x + (i % 6) * 12
            
            if y < self.canvas.rows - 1 and x + 8 < self.canvas.cols - 2:
                display_text = f"{note_name}:●"
                for j, char in enumerate(display_text):
                    if char == '●':
                        self.canvas.set_pixel(y, x + j, char, color)
                    else:
                        self.canvas.set_pixel(y, x + j, char, 'white')
    
    def run(self):
        """Main application loop"""
        print("🎵 MIDI Reactive Shapes - ASCII Engine 🎵")
        print("=" * 50)
        print()
        
        # Select MIDI port
        selected_port = self.select_midi_port()
        if not selected_port:
            print("No MIDI port selected. Exiting.")
            return
        
        try:
            # Open MIDI input
            if selected_port == 'virtual':
                print("Creating virtual MIDI port...")
                self.midi_input = mido.open_input('ASCII Engine Input', virtual=True)
                print("Virtual port created! Connect your MIDI software to 'ASCII Engine Input'")
            else:
                print(f"Opening MIDI port: {selected_port}")
                self.midi_input = mido.open_input(selected_port)
            
            print("\n🎹 MIDI port opened successfully!")
            print("Play some notes on your MIDI device to see reactive shapes!")
            print("Press Ctrl+C to exit\n")
            
            # Start MIDI listener thread
            self.running = True
            midi_thread = threading.Thread(target=self.midi_listener_thread, daemon=True)
            midi_thread.start()
            
            # Main visualization loop
            frame_count = 0
            while self.running:
                # Clear canvas
                self.canvas.clear()
                
                # Update shapes
                self.canvas.update_shapes()
                
                # Draw shapes
                self.canvas.draw_shapes()
                
                # Draw UI
                self.draw_ui()
                
                # Draw canvas
                self.canvas.draw()
                
                # Control frame rate
                time.sleep(1/30)  # 30 FPS
                frame_count += 1
                
        except KeyboardInterrupt:
            print("\n\n🛑 Stopping MIDI visualizer...")
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            
        finally:
            self.running = False
            if self.midi_input:
                self.midi_input.close()
                print("MIDI port closed.")
            
            print("\n📊 Session Stats:")
            print(f"  Notes played: {self.stats['notes_played']}")
            print(f"  Max shapes: {len(self.canvas.midi_shapes)}")
            print("\n👋 Thanks for using MIDI Reactive Shapes!")

def demo_without_midi():
    """Demo mode for when no MIDI device is available"""
    print("🎵 MIDI Reactive Shapes - Demo Mode 🎵")
    print("=" * 50)
    print("No MIDI input - running automated demo")
    print("This shows what the visualizer looks like with MIDI input")
    print("Press Ctrl+C to exit\n")
    
    canvas = MidiReactiveCanvas(50, 150)
    
    try:
        frame_count = 0
        while True:
            canvas.clear()
            
            # Simulate MIDI input
            if frame_count % 10 == 0:  # Add new shape every 10 frames
                note = randint(36, 84)  # Typical MIDI note range
                velocity = randint(40, 127)
                channel = randint(0, 4)
                canvas.add_midi_shape(note, velocity, channel)
            
            # Update and draw shapes
            canvas.update_shapes()
            canvas.draw_shapes()
            
            # Draw title
            title = "MIDI REACTIVE SHAPES - DEMO MODE"
            for i, char in enumerate(title):
                if i < canvas.cols - 2:
                    canvas.set_pixel(1, i + 1, char, 'bright_yellow')
            
            # Draw canvas
            canvas.draw()
            
            time.sleep(1/20)  # 20 FPS
            frame_count += 1
            
    except KeyboardInterrupt:
        print("\n\n🛑 Demo stopped.")

if __name__ == "__main__":
    # Check if we can access MIDI
    try:
        input_ports = mido.get_input_names()
        visualizer = MidiVisualizer()
        visualizer.run()
    except Exception as e:
        print(f"MIDI not available ({e}), running demo mode...")
        demo_without_midi()