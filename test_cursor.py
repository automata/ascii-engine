#!/usr/bin/env python3
"""
Simple test to verify cursor display in text editor
"""

import curses
import time

def test_cursor(stdscr):
    # Initialize colors
    curses.start_color()
    curses.use_default_colors()
    curses.curs_set(0)  # Hide default cursor
    
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Cursor
    
    stdscr.clear()
    
    # Test text with cursor at different positions
    test_line = "def draw():"
    cursor_positions = [0, 3, 4, 7, 10, 11]  # Various positions including end
    
    stdscr.addstr(1, 1, "Testing cursor display:", curses.color_pair(1))
    stdscr.addstr(2, 1, "Press any key to cycle through cursor positions", curses.color_pair(1))
    
    for i, cursor_pos in enumerate(cursor_positions):
        stdscr.addstr(4, 1, f"Cursor at position {cursor_pos}:", curses.color_pair(1))
        
        # Clear the line first
        stdscr.addstr(5, 1, " " * 20, curses.color_pair(1))
        
        # Draw text with cursor highlight
        for j, char in enumerate(test_line):
            if j == cursor_pos:
                stdscr.addstr(5, 1 + j, char, curses.color_pair(6))  # Highlighted cursor
            else:
                stdscr.addstr(5, 1 + j, char, curses.color_pair(1))
                
        # If cursor is at end of line
        if cursor_pos >= len(test_line):
            stdscr.addstr(5, 1 + len(test_line), ' ', curses.color_pair(6))
            
        stdscr.refresh()
        stdscr.getch()  # Wait for key press
        
    stdscr.addstr(7, 1, "Cursor test complete! Press any key to exit.", curses.color_pair(1))
    stdscr.refresh()
    stdscr.getch()

def main():
    try:
        curses.wrapper(test_cursor)
        print("✓ Cursor test completed successfully!")
    except Exception as e:
        print(f"✗ Cursor test failed: {e}")

if __name__ == "__main__":
    main()