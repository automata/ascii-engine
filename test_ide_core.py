#!/usr/bin/env python3
"""
Test script for ASCII Engine IDE core functionality
Tests the code execution and canvas integration without curses
"""

import sys
import os
import tempfile
import time
sys.path.append('.')

from ascii_engine.main import Canvas, COLORS

def test_code_execution():
    print("Testing code execution system...")
    
    # Create test canvas
    canvas = Canvas(20, 60)
    
    # Test code with setup and draw functions
    test_code = """
import math

angle = 0

def setup():
    global angle
    angle = 0

def draw():
    global angle
    
    # Draw a simple rotating line
    center_x = canvas.cols // 2
    center_y = canvas.rows // 2
    
    end_x = int(center_x + 15 * math.cos(angle))
    end_y = int(center_y + 8 * math.sin(angle))
    
    canvas.line(center_x, center_y, end_x, end_y, color='yellow')
    
    angle += 0.2
"""
    
    try:
        # Create execution namespace
        namespace = {
            'canvas': canvas,
            'Canvas': Canvas,
            'COLORS': COLORS,
            'math': __import__('math'),
            'time': __import__('time')
        }
        
        # Execute user code
        exec(test_code, namespace)
        
        # Get setup and draw functions
        setup_func = namespace.get('setup')
        draw_func = namespace.get('draw')
        
        print(f"✓ Code compiled successfully")
        print(f"✓ Found setup function: {setup_func is not None}")
        print(f"✓ Found draw function: {draw_func is not None}")
        
        # Run setup
        if setup_func:
            setup_func()
            print("✓ Setup function executed")
            
        # Run a few draw frames
        if draw_func:
            for frame in range(3):
                canvas.clear()
                draw_func()
                print(f"✓ Draw function executed (frame {frame + 1})")
                
        return True
        
    except Exception as e:
        print(f"✗ Code execution failed: {e}")
        return False

def test_syntax_highlighting_keywords():
    """Test that we can identify Python keywords for syntax highlighting"""
    print("\nTesting syntax highlighting keyword detection...")
    
    keywords = ['def', 'class', 'if', 'else', 'elif', 'for', 'while', 'return', 'import', 'from', 'pass']
    test_line = "def draw(): if True: return canvas.circle(x, y, r)"
    
    found_keywords = []
    for keyword in keywords:
        if keyword in test_line:
            found_keywords.append(keyword)
            
    print(f"✓ Found keywords in test line: {found_keywords}")
    return len(found_keywords) > 0

def test_file_operations():
    """Test file save and load operations"""
    print("\nTesting file operations...")
    
    test_content = """# Test sketch
def setup():
    pass
    
def draw():
    canvas.circle(25, 10, 5, color='red')
"""
    
    try:
        # Test save
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(test_content)
            temp_file = f.name
            
        print(f"✓ File saved to {temp_file}")
        
        # Test load
        with open(temp_file, 'r') as f:
            loaded_content = f.read()
            
        print(f"✓ File loaded successfully")
        print(f"✓ Content matches: {test_content == loaded_content}")
        
        # Cleanup
        os.unlink(temp_file)
        
        return test_content == loaded_content
        
    except Exception as e:
        print(f"✗ File operations failed: {e}")
        return False

def test_example_sketches():
    """Test that our new example sketches can be executed"""
    print("\nTesting new example sketches...")
    
    examples_dir = "examples"
    if not os.path.exists(examples_dir):
        print(f"✗ Examples directory not found")
        return False
        
    # Test only our new example files
    test_files = ['bouncing_ball.py', 'sine_wave.py', 'spiral.py', 'simple_shapes.py']
    
    canvas = Canvas(20, 60)
    success_count = 0
    total_count = len(test_files)
    
    for filename in test_files:
        filepath = os.path.join(examples_dir, filename)
        if not os.path.exists(filepath):
            print(f"✗ {filename} not found")
            continue
            
        try:
            with open(filepath, 'r') as f:
                code = f.read()
                    
            # Create execution namespace
            namespace = {
                'canvas': canvas,
                'Canvas': Canvas,
                'COLORS': COLORS,
                'randint': __import__('random').randint,
                'math': __import__('math'),
                'time': __import__('time')
            }
            
            # Execute code
            exec(code, namespace)
            
            # Test functions exist
            setup_func = namespace.get('setup')
            draw_func = namespace.get('draw')
            
            if setup_func:
                setup_func()
            if draw_func:
                canvas.clear()
                draw_func()
                
            print(f"✓ {filename} executed successfully")
            success_count += 1
            
        except Exception as e:
            print(f"✗ {filename} failed: {e}")
                
    print(f"\nExample sketches: {success_count}/{total_count} successful")
    return success_count == total_count

def main():
    print("=== ASCII Engine IDE Core Functionality Tests ===\n")
    
    tests = [
        test_code_execution,
        test_syntax_highlighting_keywords, 
        test_file_operations,
        test_example_sketches
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
        
    print(f"=== Test Results: {passed}/{total} tests passed ===")
    
    if passed == total:
        print("🎉 All core functionality tests passed!")
        print("\nTo run the IDE, use: python ascii_ide.py")
        print("Note: Requires a terminal that supports curses")
    else:
        print("❌ Some tests failed")
        
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)