import os
import sys

# Add parent directory to path to import ascii_engine
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from ascii_engine.main import Canvas

def mandelbrot(c_real, c_imag, max_iter=100):
    """Calculate mandelbrot iteration count for complex number c"""
    z_real, z_imag = 0.0, 0.0
    
    for i in range(max_iter):
        # z = z^2 + c
        z_real_new = z_real * z_real - z_imag * z_imag + c_real
        z_imag_new = 2 * z_real * z_imag + c_imag
        
        z_real, z_imag = z_real_new, z_imag_new
        
        # Check if magnitude exceeds escape radius
        if z_real * z_real + z_imag * z_imag > 4.0:
            return i
    
    return max_iter

def get_mandelbrot_color(iterations, max_iter):
    """Map iteration count to color"""
    if iterations == max_iter:
        return 'black'
    
    # Create color gradient based on iteration count
    ratio = iterations / max_iter
    
    if ratio < 0.16:
        return 'blue'
    elif ratio < 0.33:
        return 'cyan'  
    elif ratio < 0.5:
        return 'green'
    elif ratio < 0.66:
        return 'yellow'
    elif ratio < 0.83:
        return 'red'
    else:
        return 'magenta'

if __name__ == "__main__":
    # Canvas dimensions
    rows = 50
    cols = 150
    canvas = Canvas(rows, cols)
    
    # Mandelbrot parameters
    x_min, x_max = -2.5, 1.0
    y_min, y_max = -1.25, 1.25
    max_iterations = 50
    
    # Calculate step sizes
    x_step = (x_max - x_min) / cols
    y_step = (y_max - y_min) / rows
    
    print("Generating Mandelbrot fractal...")
    print(f"Resolution: {cols}x{rows}")
    print(f"Complex plane: [{x_min}, {x_max}] x [{y_min}i, {y_max}i]")
    print(f"Max iterations: {max_iterations}")
    print("\nPress Ctrl+C to exit\n")
    
    # Generate the fractal
    for row in range(rows):
        for col in range(cols):
            # Map pixel coordinates to complex plane
            c_real = x_min + col * x_step
            c_imag = y_max - row * y_step  # Flip y-axis
            
            # Calculate mandelbrot iterations
            iterations = mandelbrot(c_real, c_imag, max_iterations)
            
            # Get color based on iterations
            color = get_mandelbrot_color(iterations, max_iterations)
            
            # Set pixel with appropriate character
            if iterations == max_iterations:
                # Points in the set (black)
                canvas.set_pixel(row, col, '█', color)
            else:
                # Points outside the set (colored by iteration count)
                canvas.set_pixel(row, col, '▓', color)
    
    # Display the fractal
    canvas.draw()
    
    print("\nMandelbrot fractal generated successfully!")