import os
import sys
import time
import math
from random import randint, choice

# Add parent directory to path to import ascii_engine
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from ascii_engine.main import Canvas, COLORS

def add_ansi_effects():
    """Add additional ANSI effects and colors to the existing color palette"""
    effects = {
        # Bright colors
        'bright_black': '\033[90m',
        'bright_red': '\033[91m',
        'bright_green': '\033[92m',
        'bright_yellow': '\033[93m',
        'bright_blue': '\033[94m',
        'bright_magenta': '\033[95m',
        'bright_cyan': '\033[96m',
        'bright_white': '\033[97m',
        
        # Background colors
        'bg_black': '\033[40m',
        'bg_red': '\033[41m',
        'bg_green': '\033[42m',
        'bg_yellow': '\033[43m',
        'bg_blue': '\033[44m',
        'bg_magenta': '\033[45m',
        'bg_cyan': '\033[46m',
        'bg_white': '\033[47m',
        
        # Text effects
        'bold': '\033[1m',
        'dim': '\033[2m',
        'italic': '\033[3m',
        'underline': '\033[4m',
        'blink': '\033[5m',
        'reverse': '\033[7m',
        'strikethrough': '\033[9m',
    }
    
    # Add to global COLORS dict
    COLORS.update(effects)
    return effects

class CrazyCanvas(Canvas):
    """Extended Canvas with crazy ANSI character support"""
    
    def __init__(self, rows, cols):
        super().__init__(rows, cols)
        self.crazy_chars = [
            # Block elements
            '█', '▓', '▒', '░', '▄', '▀', '▌', '▐',
            # Geometric shapes
            '●', '○', '◉', '◯', '◦', '•', '∘', '⊙', '⊚', '⊛',
            '■', '□', '▪', '▫', '▬', '▭', '▮', '▯',
            '▲', '△', '▼', '▽', '◆', '◇', '◈', '◊',
            # Special symbols
            '★', '☆', '✦', '✧', '✩', '✪', '✫', '✬', '✭', '✮', '✯',
            '♠', '♣', '♥', '♦', '♤', '♧', '♡', '♢',
            # Mathematical symbols
            '∞', '∅', '∈', '∉', '∋', '∌', '∩', '∪', '⊂', '⊃',
            # Arrows and directions
            '→', '←', '↑', '↓', '↗', '↘', '↙', '↖', '↔', '↕',
            '⇒', '⇐', '⇑', '⇓', '⇗', '⇘', '⇙', '⇖', '⇔', '⇕',
            # Miscellaneous
            '※', '§', '¶', '†', '‡', '•', '‰', '′', '″', '‴',
            '℀', '℁', '℃', '℉', '℗', '℘', '℞', '℟', '℠', '℡',
        ]
        
        # Add ANSI effects
        add_ansi_effects()
    
    def set_crazy_pixel(self, row, col, char=None, color='white', effect=None, bg_color=None):
        """Set a pixel with crazy ANSI effects"""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            if char is None:
                char = choice(self.crazy_chars)
            
            # Build ANSI sequence
            ansi_sequence = ""
            
            # Add effect
            if effect and effect in COLORS:
                ansi_sequence += COLORS[effect]
            
            # Add background color
            if bg_color and f'bg_{bg_color}' in COLORS:
                ansi_sequence += COLORS[f'bg_{bg_color}']
            
            # Add foreground color
            if color in COLORS:
                ansi_sequence += COLORS[color]
            
            # Add character and reset
            colored_char = f"{ansi_sequence}{char}{COLORS['reset']}"
            self.canvas[row][col] = colored_char
    
    def crazy_circle(self, center_x, center_y, radius, filled=True, char=None, color='white', effect=None, bg_color=None):
        """Draw a circle with crazy ANSI effects"""
        if radius <= 0:
            return
        
        # Use midpoint circle algorithm
        x = 0
        y = radius
        d = 1 - radius
        
        self._draw_crazy_circle_points(center_x, center_y, x, y, filled, char, color, effect, bg_color)
        
        while x < y:
            if d < 0:
                d += 2 * x + 3
            else:
                d += 2 * (x - y) + 5
                y -= 1
            x += 1
            self._draw_crazy_circle_points(center_x, center_y, x, y, filled, char, color, effect, bg_color)
    
    def _draw_crazy_circle_points(self, cx, cy, x, y, filled, char, color, effect, bg_color):
        """Draw crazy circle points"""
        if filled:
            # Fill horizontal lines for filled circle
            for py in [cy + y, cy - y, cy + x, cy - x]:
                if py == cy + y or py == cy - y:
                    for px in range(cx - x, cx + x + 1):
                        self.set_crazy_pixel(py, px, char, color, effect, bg_color)
                elif py == cy + x or py == cy - x:
                    for px in range(cx - y, cx + y + 1):
                        self.set_crazy_pixel(py, px, char, color, effect, bg_color)
        else:
            # Just draw the outline points
            points = [
                (cx + x, cy + y), (cx - x, cy + y),
                (cx + x, cy - y), (cx - x, cy - y),
                (cx + y, cy + x), (cx - y, cy + x),
                (cx + y, cy - x), (cx - y, cy - x)
            ]
            for px, py in points:
                self.set_crazy_pixel(py, px, char, color, effect, bg_color)
    
    def crazy_rect(self, x, y, width, height, filled=True, char=None, color='white', effect=None, bg_color=None):
        """Draw a rectangle with crazy ANSI effects"""
        if width <= 0 or height <= 0:
            return
        
        if filled:
            # Fill the entire rectangle
            for row in range(y, y + height):
                for col in range(x, x + width):
                    self.set_crazy_pixel(row, col, char, color, effect, bg_color)
        else:
            # Draw just the outline
            for col in range(x, x + width):
                self.set_crazy_pixel(y, col, char, color, effect, bg_color)  # Top
                self.set_crazy_pixel(y + height - 1, col, char, color, effect, bg_color)  # Bottom
            for row in range(y, y + height):
                self.set_crazy_pixel(row, x, char, color, effect, bg_color)  # Left
                self.set_crazy_pixel(row, x + width - 1, char, color, effect, bg_color)  # Right
    
    def crazy_line(self, x1, y1, x2, y2, char=None, color='white', effect=None, bg_color=None):
        """Draw a line with crazy ANSI effects using Bresenham's algorithm"""
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        
        x, y = x1, y1
        
        while True:
            self.set_crazy_pixel(y, x, char, color, effect, bg_color)
            
            if x == x2 and y == y2:
                break
                
            e2 = 2 * err
            
            if e2 > -dy:
                err -= dy
                x += sx
                
            if e2 < dx:
                err += dx
                y += sy
    
    def rainbow_text(self, x, y, text, direction='horizontal'):
        """Draw text with rainbow colors"""
        colors = ['red', 'bright_red', 'yellow', 'bright_yellow', 'green', 'bright_green', 
                 'cyan', 'bright_cyan', 'blue', 'bright_blue', 'magenta', 'bright_magenta']
        
        for i, char in enumerate(text):
            color = colors[i % len(colors)]
            if direction == 'horizontal':
                self.set_crazy_pixel(y, x + i, char, color, 'bold')
            else:  # vertical
                self.set_crazy_pixel(y + i, x, char, color, 'bold')

def demo_crazy_shapes():
    """Demonstrate crazy ANSI shapes"""
    rows = 50
    cols = 150
    canvas = CrazyCanvas(rows, cols)
    
    print("🎨 CRAZY ANSI SHAPES DEMO 🎨")
    print("=" * 50)
    print()
    
    # Frame 1: Rainbow circles with effects
    print("Frame 1: Rainbow Circles with Blink Effect")
    canvas.clear()
    
    for i in range(8):
        x = 20 + i * 15
        y = 10 + i * 2
        radius = 3 + i
        effects = ['bold', 'blink', 'underline', 'reverse']
        colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'magenta', 'bright_red', 'bright_cyan']
        
        canvas.crazy_circle(x, y, radius, filled=True, 
                          char='●', color=colors[i], effect=effects[i % len(effects)])
    
    canvas.draw()
    time.sleep(3)
    
    # Frame 2: Geometric patterns with backgrounds
    print("\nFrame 2: Geometric Patterns with Background Colors")
    canvas.clear()
    
    shapes = ['■', '▲', '●', '◆', '★', '♠', '♥', '♦']
    colors = ['white', 'bright_yellow', 'bright_green', 'bright_red', 'bright_blue', 'bright_magenta', 'bright_cyan', 'yellow']
    bg_colors = ['red', 'blue', 'green', 'magenta', 'cyan', 'yellow', 'black', 'white']
    
    for i in range(len(shapes)):
        for j in range(10):
            x = 10 + j * 12
            y = 5 + i * 5
            canvas.set_crazy_pixel(y, x, shapes[i], colors[i], 'bold', bg_colors[i])
    
    canvas.draw()
    time.sleep(3)
    
    # Frame 3: Mathematical symbols with effects
    print("\nFrame 3: Mathematical Symbols with Various Effects")
    canvas.clear()
    
    math_symbols = ['∞', '∅', '∈', '∉', '∋', '∌', '∩', '∪', '⊂', '⊃', '∀', '∃', '∇', '∂', '∫', '∑']
    effects = ['bold', 'italic', 'underline', 'reverse', 'blink', 'dim']
    
    for i, symbol in enumerate(math_symbols):
        x = 10 + (i % 8) * 16
        y = 10 + (i // 8) * 8
        color = choice(['bright_red', 'bright_green', 'bright_blue', 'bright_yellow', 'bright_magenta', 'bright_cyan'])
        effect = choice(effects)
        canvas.set_crazy_pixel(y, x, symbol, color, effect)
        
        # Add some decoration around each symbol
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx != 0 or dy != 0:
                    deco_char = choice(['·', '∘', '•', '‧'])
                    canvas.set_crazy_pixel(y + dy, x + dx, deco_char, 'dim')
    
    canvas.draw()
    time.sleep(3)
    
    # Frame 4: Arrow patterns
    print("\nFrame 4: Arrow Patterns with Movement Effect")
    canvas.clear()
    
    arrows = ['→', '←', '↑', '↓', '↗', '↘', '↙', '↖', '⇒', '⇐', '⇑', '⇓']
    
    # Create spiral of arrows
    center_x, center_y = 75, 25
    for i in range(len(arrows) * 3):
        angle = i * 0.5
        radius = 2 + i * 0.8
        x = int(center_x + radius * math.cos(angle))
        y = int(center_y + radius * math.sin(angle))
        
        arrow = arrows[i % len(arrows)]
        color = ['bright_red', 'bright_yellow', 'bright_green', 'bright_cyan'][i % 4]
        canvas.set_crazy_pixel(y, x, arrow, color, 'bold')
    
    canvas.draw()
    time.sleep(3)
    
    # Frame 5: Playing card suits with effects
    print("\nFrame 5: Playing Card Suits with Blinking Effects")
    canvas.clear()
    
    suits = ['♠', '♣', '♥', '♦']
    suit_colors = ['white', 'bright_green', 'bright_red', 'bright_blue']
    
    for suit_idx, suit in enumerate(suits):
        for row in range(8):
            for col in range(15):
                x = 10 + suit_idx * 35 + col * 2
                y = 8 + row * 3
                
                # Create pattern
                if (row + col) % 2 == 0:
                    canvas.set_crazy_pixel(y, x, suit, suit_colors[suit_idx], 'blink', 'black')
                else:
                    canvas.set_crazy_pixel(y, x, choice(['·', '∘']), 'dim')
    
    canvas.draw()
    time.sleep(3)
    
    # Frame 6: Star field with twinkling effect
    print("\nFrame 6: Twinkling Star Field")
    canvas.clear()
    
    stars = ['★', '☆', '✦', '✧', '✩', '✪', '✫', '✬', '✭', '✮', '✯', '⋆', '✱', '✲', '✳', '✴']
    
    for _ in range(80):
        x = randint(5, cols - 5)
        y = randint(3, rows - 3)
        star = choice(stars)
        color = choice(['white', 'bright_white', 'bright_yellow', 'yellow', 'bright_cyan'])
        effect = choice(['bold', 'blink', None])
        
        canvas.set_crazy_pixel(y, x, star, color, effect)
    
    canvas.draw()
    time.sleep(3)
    
    # Frame 7: Rainbow text with effects
    print("\nFrame 7: Rainbow Text Effects")
    canvas.clear()
    
    messages = [
        "CRAZY ANSI SHAPES!",
        "TERMINAL ART ROCKS!",
        "ASCII ENGINE POWER!",
        "COLORFUL CHARACTERS!"
    ]
    
    for i, message in enumerate(messages):
        canvas.rainbow_text(10, 8 + i * 8, message)
    
    # Add decorative border
    border_chars = ['═', '║', '╔', '╗', '╚', '╝', '╠', '╣', '╦', '╩', '╬']
    
    # Top and bottom borders
    for col in range(5, cols - 5):
        canvas.set_crazy_pixel(2, col, '═', 'bright_cyan', 'bold')
        canvas.set_crazy_pixel(rows - 3, col, '═', 'bright_cyan', 'bold')
    
    # Left and right borders
    for row in range(2, rows - 2):
        canvas.set_crazy_pixel(row, 5, '║', 'bright_cyan', 'bold')
        canvas.set_crazy_pixel(row, cols - 6, '║', 'bright_cyan', 'bold')
    
    # Corners
    canvas.set_crazy_pixel(2, 5, '╔', 'bright_cyan', 'bold')
    canvas.set_crazy_pixel(2, cols - 6, '╗', 'bright_cyan', 'bold')
    canvas.set_crazy_pixel(rows - 3, 5, '╚', 'bright_cyan', 'bold')
    canvas.set_crazy_pixel(rows - 3, cols - 6, '╝', 'bright_cyan', 'bold')
    
    canvas.draw()
    time.sleep(3)
    
    print("\n🎆 Demo complete! 🎆")
    print("The ASCII engine supports:")
    print("• Unicode block elements and geometric shapes")
    print("• Mathematical and special symbols") 
    print("• ANSI color effects (bold, blink, underline, etc.)")
    print("• Background colors")
    print("• Bright color variants")
    print("• Complex character combinations")

if __name__ == "__main__":
    demo_crazy_shapes()