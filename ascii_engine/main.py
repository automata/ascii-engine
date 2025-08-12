import os
import time
import math
from random import randint

COLORS = {
  'black': '\u001b[30m',
  'yellow': '\u001b[33m',
  'red': '\u001b[31m',
  'green': '\u001b[32m',
  'blue': '\u001b[34m',
  'magenta': '\u001b[35m',
  'cyan': '\u001b[36m',
  'white': '\u001b[37m',
  'reset': '\u001b[0m'
}

class Canvas:
    def __init__(self, rows, cols):
        self.blank = ' '
        self.rows = rows
        self.cols = cols
        self.canvas = [[self.blank for c in range(cols)] for r in range(rows)]
        self.fill_char = '●'
        self.stroke_char = '○'
        self.rect_fill_char = '█'
        self.rect_stroke_char = '□'
        self.line_char = '█'
        self.arc_char = '●'
        self.triangle_char = '▲'
        self.ellipse_fill_char = '●'
        self.ellipse_stroke_char = '○'
        self.bezier_char = '█'
        self.curve_char = '█'

    def draw(self):
        # Build entire frame as a string first (buffer)
        output = []
        for r in range(self.rows):
            row = ''.join(self.canvas[r])
            output.append(row)
        
        # Print entire frame at once to reduce flickering
        print('\n'.join(output), flush=True)

    def set_pixel(self, row, col, char, color='white'):
        """Set a single pixel on the canvas"""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            colored_char = f"{COLORS[color]}{char}{COLORS['reset']}"
            self.canvas[row][col] = colored_char
    
    def circle(self, center_x, center_y, radius, filled=True, color='yellow'):
        """Draw a circle using the midpoint circle algorithm (Bresenham-like)"""
        if radius <= 0:
            return
            
        char = self.fill_char if filled else self.stroke_char
        
        # Handle single pixel circle
        if radius == 1:
            self.set_pixel(center_y, center_x, char, color)
            return
            
        # Midpoint circle algorithm
        x = 0
        y = radius
        d = 1 - radius
        
        # Draw initial points
        self._draw_circle_points(center_x, center_y, x, y, char, color, filled)
        
        while x < y:
            if d < 0:
                d += 2 * x + 3
            else:
                d += 2 * (x - y) + 5
                y -= 1
            x += 1
            self._draw_circle_points(center_x, center_y, x, y, char, color, filled)
    
    def _draw_circle_points(self, cx, cy, x, y, char, color, filled):
        """Draw the 8 symmetric points of a circle"""
        points = [
            (cx + x, cy + y), (cx - x, cy + y),
            (cx + x, cy - y), (cx - x, cy - y),
            (cx + y, cy + x), (cx - y, cy + x),
            (cx + y, cy - x), (cx - y, cy - x)
        ]
        
        if filled:
            # Fill horizontal lines for filled circle
            for py in [cy + y, cy - y, cy + x, cy - x]:
                if py == cy + y or py == cy - y:
                    for px in range(cx - x, cx + x + 1):
                        self.set_pixel(py, px, char, color)
                elif py == cy + x or py == cy - x:
                    for px in range(cx - y, cx + y + 1):
                        self.set_pixel(py, px, char, color)
        else:
            # Just draw the outline points
            for px, py in points:
                self.set_pixel(py, px, char, color)
    
    def bezier(self, x1, y1, cx1, cy1, cx2, cy2, x2, y2, color='white', steps=50):
        """Draw a cubic Bezier curve with two control points"""
        char = self.bezier_char
        
        # Draw curve using parametric equation
        for i in range(steps + 1):
            t = i / steps
            
            # Cubic Bezier formula: B(t) = (1-t)³P₀ + 3(1-t)²tP₁ + 3(1-t)t²P₂ + t³P₃
            t_inv = 1 - t
            t_inv2 = t_inv * t_inv
            t_inv3 = t_inv2 * t_inv
            t2 = t * t
            t3 = t2 * t
            
            x = (t_inv3 * x1 + 
                 3 * t_inv2 * t * cx1 + 
                 3 * t_inv * t2 * cx2 + 
                 t3 * x2)
            
            y = (t_inv3 * y1 + 
                 3 * t_inv2 * t * cy1 + 
                 3 * t_inv * t2 * cy2 + 
                 t3 * y2)
            
            self.set_pixel(int(round(y)), int(round(x)), char, color)
    
    def bezier_quad(self, x1, y1, cx, cy, x2, y2, color='white', steps=30):
        """Draw a quadratic Bezier curve with one control point"""
        char = self.bezier_char
        
        # Draw curve using parametric equation
        for i in range(steps + 1):
            t = i / steps
            
            # Quadratic Bezier formula: B(t) = (1-t)²P₀ + 2(1-t)tP₁ + t²P₂
            t_inv = 1 - t
            t_inv2 = t_inv * t_inv
            t2 = t * t
            
            x = t_inv2 * x1 + 2 * t_inv * t * cx + t2 * x2
            y = t_inv2 * y1 + 2 * t_inv * t * cy + t2 * y2
            
            self.set_pixel(int(round(y)), int(round(x)), char, color)
    
    def curve(self, x1, y1, x2, y2, x3, y3, x4, y4, color='white', steps=50, tension=0.5):
        """Draw a Catmull-Rom spline curve through 4 points"""
        char = self.curve_char
        
        # Catmull-Rom spline passes through the middle two points (x2,y2) and (x3,y3)
        # Uses the outer points (x1,y1) and (x4,y4) as control points
        
        for i in range(steps + 1):
            t = i / steps
            t2 = t * t
            t3 = t2 * t
            
            # Catmull-Rom basis functions
            # Tension parameter controls the "tightness" of the curve
            h1 = -tension * t + 2 * tension * t2 - tension * t3
            h2 = 1 + (tension - 3) * t2 + (2 - tension) * t3
            h3 = tension * t + (3 - 2 * tension) * t2 + (tension - 2) * t3
            h4 = -tension * t2 + tension * t3
            
            x = h1 * x1 + h2 * x2 + h3 * x3 + h4 * x4
            y = h1 * y1 + h2 * y2 + h3 * y3 + h4 * y4
            
            self.set_pixel(int(round(y)), int(round(x)), char, color)
    
    def curve_vertex(self, points, color='white', steps=50, tension=0.5, closed=False):
        """Draw a smooth curve through multiple points using Catmull-Rom splines"""
        if len(points) < 4:
            # Not enough points for Catmull-Rom, fall back to lines
            for i in range(len(points) - 1):
                x1, y1 = points[i]
                x2, y2 = points[i + 1]
                self.line(x1, y1, x2, y2, color)
            return
        
        # Draw segments between consecutive groups of 4 points
        if closed:
            # For closed curves, add wraparound points
            extended_points = [points[-1], points[0]] + points + [points[0], points[1]]
            segments = len(points)
        else:
            # For open curves, duplicate end points
            extended_points = [points[0]] + points + [points[-1]]
            segments = len(points) - 1
        
        for i in range(segments):
            if closed:
                p1, p2, p3, p4 = extended_points[i:i+4]
            else:
                p1, p2, p3, p4 = extended_points[i:i+4]
            
            self.curve(p1[0], p1[1], p2[0], p2[1], p3[0], p3[1], p4[0], p4[1], 
                      color=color, steps=steps//segments if segments > 0 else steps, tension=tension)
    
    def rect(self, x, y, width, height, filled=True, color='white'):
        """Draw a rectangle - Processing-style rect(x, y, width, height)"""
        if width <= 0 or height <= 0:
            return
            
        char = self.rect_fill_char if filled else self.rect_stroke_char
        
        if filled:
            # Fill the entire rectangle
            for row in range(y, y + height):
                for col in range(x, x + width):
                    self.set_pixel(row, col, char, color)
        else:
            # Draw just the outline
            # Top and bottom edges
            for col in range(x, x + width):
                self.set_pixel(y, col, char, color)  # Top edge
                self.set_pixel(y + height - 1, col, char, color)  # Bottom edge
            
            # Left and right edges
            for row in range(y, y + height):
                self.set_pixel(row, x, char, color)  # Left edge
                self.set_pixel(row, x + width - 1, char, color)  # Right edge
    
    def line(self, x1, y1, x2, y2, color='white'):
        """Draw a line using Bresenham's line algorithm"""
        char = self.line_char
        
        # Bresenham's line algorithm
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        
        # Determine direction of line
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        
        err = dx - dy
        
        x, y = x1, y1
        
        while True:
            self.set_pixel(y, x, char, color)
            
            if x == x2 and y == y2:
                break
                
            e2 = 2 * err
            
            if e2 > -dy:
                err -= dy
                x += sx
                
            if e2 < dx:
                err += dx
                y += sy
    
    def square(self, x, y, size, filled=True, color='white'):
        """Draw a square - shorthand for rect with equal width and height"""
        self.rect(x, y, size, size, filled, color)
    
    def arc(self, center_x, center_y, radius, start_angle, end_angle, color='white'):
        """Draw an arc from start_angle to end_angle (in radians)"""
        if radius <= 0:
            return
            
        char = self.arc_char
        
        # Normalize angles to 0-2π range
        start_angle = start_angle % (2 * math.pi)
        end_angle = end_angle % (2 * math.pi)
        
        # If end_angle < start_angle, we're wrapping around
        if end_angle < start_angle:
            end_angle += 2 * math.pi
        
        # Use circle algorithm but only draw points within angle range
        x = 0
        y = radius
        d = 1 - radius
        
        self._draw_arc_points(center_x, center_y, x, y, start_angle, end_angle, char, color)
        
        while x < y:
            if d < 0:
                d += 2 * x + 3
            else:
                d += 2 * (x - y) + 5
                y -= 1
            x += 1
            self._draw_arc_points(center_x, center_y, x, y, start_angle, end_angle, char, color)
    
    def _draw_arc_points(self, cx, cy, x, y, start_angle, end_angle, char, color):
        """Draw arc points only within the specified angle range"""
        points = [
            (cx + x, cy + y), (cx - x, cy + y),
            (cx + x, cy - y), (cx - x, cy - y),
            (cx + y, cy + x), (cx - y, cy + x),
            (cx + y, cy - x), (cx - y, cy - x)
        ]
        
        for px, py in points:
            # Calculate angle of this point
            dx = px - cx
            dy = py - cy
            angle = math.atan2(dy, dx)
            if angle < 0:
                angle += 2 * math.pi
            
            # Check if angle is within arc range (handle wraparound)
            if end_angle > 2 * math.pi:
                if angle >= start_angle or angle <= (end_angle - 2 * math.pi):
                    self.set_pixel(py, px, char, color)
            else:
                if start_angle <= angle <= end_angle:
                    self.set_pixel(py, px, char, color)
    
    def triangle(self, x1, y1, x2, y2, x3, y3, filled=True, color='white'):
        """Draw a triangle with three points"""
        if filled:
            # Fill triangle using scanline algorithm
            self._fill_triangle(x1, y1, x2, y2, x3, y3, color)
        else:
            # Draw triangle outline using lines
            self.line(x1, y1, x2, y2, color)
            self.line(x2, y2, x3, y3, color)
            self.line(x3, y3, x1, y1, color)
    
    def _fill_triangle(self, x1, y1, x2, y2, x3, y3, color):
        """Fill triangle using scanline algorithm"""
        char = self.triangle_char
        
        # Sort vertices by y coordinate
        vertices = [(x1, y1), (x2, y2), (x3, y3)]
        vertices.sort(key=lambda v: v[1])
        (x1, y1), (x2, y2), (x3, y3) = vertices
        
        # Handle degenerate triangles
        if y1 == y3:
            return
        
        # Scanline fill
        for y in range(int(y1), int(y3) + 1):
            # Find intersection points with triangle edges
            intersections = []
            
            # Check edge 1-2
            if y1 != y2 and y1 <= y <= y2:
                t = (y - y1) / (y2 - y1)
                x = x1 + t * (x2 - x1)
                intersections.append(x)
            
            # Check edge 2-3
            if y2 != y3 and y2 <= y <= y3:
                t = (y - y2) / (y3 - y2)
                x = x2 + t * (x3 - x2)
                intersections.append(x)
            
            # Check edge 1-3
            if y1 != y3 and y1 <= y <= y3:
                t = (y - y1) / (y3 - y1)
                x = x1 + t * (x3 - x1)
                intersections.append(x)
            
            # Fill between intersection points
            if len(intersections) >= 2:
                intersections.sort()
                start_x = int(intersections[0])
                end_x = int(intersections[-1])
                for x in range(start_x, end_x + 1):
                    self.set_pixel(y, x, char, color)
    
    def ellipse(self, center_x, center_y, width, height, filled=True, color='white'):
        """Draw an ellipse using the midpoint ellipse algorithm"""
        if width <= 0 or height <= 0:
            return
            
        a = width // 2  # Semi-major axis
        b = height // 2  # Semi-minor axis
        
        if a == 0 or b == 0:
            return
            
        char = self.ellipse_fill_char if filled else self.ellipse_stroke_char
        
        # Handle circle case
        if a == b:
            self.circle(center_x, center_y, a, filled, color)
            return
        
        # Midpoint ellipse algorithm
        x = 0
        y = b
        
        # Region 1
        d1 = b * b - a * a * b + 0.25 * a * a
        dx = 2 * b * b * x
        dy = 2 * a * a * y
        
        while dx < dy:
            self._draw_ellipse_points(center_x, center_y, x, y, char, color, filled)
            
            if d1 < 0:
                x += 1
                dx += 2 * b * b
                d1 += dx + b * b
            else:
                x += 1
                y -= 1
                dx += 2 * b * b
                dy -= 2 * a * a
                d1 += dx - dy + b * b
        
        # Region 2
        d2 = b * b * (x + 0.5) * (x + 0.5) + a * a * (y - 1) * (y - 1) - a * a * b * b
        
        while y >= 0:
            self._draw_ellipse_points(center_x, center_y, x, y, char, color, filled)
            
            if d2 > 0:
                y -= 1
                dy -= 2 * a * a
                d2 += a * a - dy
            else:
                x += 1
                y -= 1
                dx += 2 * b * b
                dy -= 2 * a * a
                d2 += dx - dy + a * a
    
    def _draw_ellipse_points(self, cx, cy, x, y, char, color, filled):
        """Draw the 4 symmetric points of an ellipse"""
        if filled:
            # Fill horizontal lines for filled ellipse
            for py in [cy + y, cy - y]:
                for px in range(cx - x, cx + x + 1):
                    self.set_pixel(py, px, char, color)
        else:
            # Just draw the outline points
            points = [(cx + x, cy + y), (cx - x, cy + y), (cx + x, cy - y), (cx - x, cy - y)]
            for px, py in points:
                self.set_pixel(py, px, char, color)

    def clear(self):
        for r in range(self.rows):
            for c in range(self.cols):
                self.canvas[r][c] = self.blank
        # Don't print anything when clearing - let the IDE handle display

if __name__ == "__main__":
    rows = 50
    cols = 150
    canvas = Canvas(rows, cols)
    
    # Demo: showcase all drawing functions
    while True:
        canvas.clear()
        
        # Draw some filled rectangles and squares
        for i in range(4):
            x = randint(5, cols - 25)
            y = randint(3, rows - 10)
            width = randint(8, 20)
            height = randint(4, 8)
            colors = ['red', 'green', 'blue', 'magenta', 'cyan', 'yellow']
            color = colors[randint(0, len(colors) - 1)]
            canvas.rect(x, y, width, height, filled=True, color=color)
        
        # Draw some squares
        for i in range(3):
            x = randint(5, cols - 20)
            y = randint(3, rows - 15)
            size = randint(6, 12)
            colors = ['white', 'yellow', 'cyan']
            color = colors[randint(0, len(colors) - 1)]
            canvas.square(x, y, size, filled=randint(0, 1) == 1, color=color)
        
        # Draw some ellipses
        for i in range(4):
            x = randint(15, cols - 15)
            y = randint(8, rows - 8)
            width = randint(12, 24)
            height = randint(6, 12)
            colors = ['magenta', 'cyan', 'yellow', 'green']
            color = colors[randint(0, len(colors) - 1)]
            canvas.ellipse(x, y, width, height, filled=randint(0, 1) == 1, color=color)
        
        # Draw some triangles
        for i in range(3):
            x1 = randint(10, cols - 10)
            y1 = randint(5, rows - 5)
            x2 = randint(10, cols - 10)
            y2 = randint(5, rows - 5)
            x3 = randint(10, cols - 10)
            y3 = randint(5, rows - 5)
            colors = ['red', 'blue', 'green', 'yellow']
            color = colors[randint(0, len(colors) - 1)]
            canvas.triangle(x1, y1, x2, y2, x3, y3, filled=randint(0, 1) == 1, color=color)
        
        # Draw some arcs
        for i in range(2):
            x = randint(20, cols - 20)
            y = randint(10, rows - 10)
            radius = randint(5, 12)
            start_angle = randint(0, 360) * math.pi / 180
            arc_span = randint(60, 180) * math.pi / 180
            end_angle = start_angle + arc_span
            colors = ['white', 'yellow', 'red', 'cyan']
            color = colors[randint(0, len(colors) - 1)]
            canvas.arc(x, y, radius, start_angle, end_angle, color=color)
        
        # Draw some cubic Bezier curves
        for i in range(3):
            x1 = randint(10, cols - 10)
            y1 = randint(5, rows - 5)
            x2 = randint(10, cols - 10)
            y2 = randint(5, rows - 5)
            cx1 = randint(10, cols - 10)
            cy1 = randint(5, rows - 5)
            cx2 = randint(10, cols - 10)
            cy2 = randint(5, rows - 5)
            colors = ['magenta', 'cyan', 'yellow', 'green']
            color = colors[randint(0, len(colors) - 1)]
            canvas.bezier(x1, y1, cx1, cy1, cx2, cy2, x2, y2, color=color)
        
        # Draw some quadratic Bezier curves
        for i in range(2):
            x1 = randint(10, cols - 10)
            y1 = randint(5, rows - 5)
            x2 = randint(10, cols - 10)
            y2 = randint(5, rows - 5)
            cx = randint(10, cols - 10)
            cy = randint(5, rows - 5)
            colors = ['red', 'blue', 'white']
            color = colors[randint(0, len(colors) - 1)]
            canvas.bezier_quad(x1, y1, cx, cy, x2, y2, color=color)
        
        # Draw some Catmull-Rom curves
        for i in range(2):
            x1 = randint(20, cols - 20)
            y1 = randint(10, rows - 10)
            x2 = randint(20, cols - 20)
            y2 = randint(10, rows - 10)
            x3 = randint(20, cols - 20)
            y3 = randint(10, rows - 10)
            x4 = randint(20, cols - 20)
            y4 = randint(10, rows - 10)
            colors = ['green', 'blue', 'yellow']
            color = colors[randint(0, len(colors) - 1)]
            canvas.curve(x1, y1, x2, y2, x3, y3, x4, y4, color=color)
        
        # Draw a smooth multi-point curve
        points = []
        for i in range(6):
            x = randint(30, cols - 30)
            y = randint(15, rows - 15)
            points.append((x, y))
        canvas.curve_vertex(points, color='white', tension=0.3)
        
        # Draw some lines
        for i in range(6):
            x1 = randint(0, cols - 1)
            y1 = randint(0, rows - 1)
            x2 = randint(0, cols - 1)
            y2 = randint(0, rows - 1)
            colors = ['white', 'yellow', 'red', 'green', 'blue', 'magenta', 'cyan']
            color = colors[randint(0, len(colors) - 1)]
            canvas.line(x1, y1, x2, y2, color=color)
        
        # Draw some circles
        for i in range(3):
            x = randint(10, cols - 10)
            y = randint(5, rows - 5)
            radius = randint(3, 8)
            colors = ['yellow', 'red', 'green', 'blue', 'magenta', 'cyan']
            color = colors[randint(0, len(colors) - 1)]
            filled = randint(0, 1) == 1
            canvas.circle(x, y, radius, filled=filled, color=color)
        
        canvas.draw()
        time.sleep(1.0)

