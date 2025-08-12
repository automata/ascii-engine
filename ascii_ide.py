#!/usr/bin/env python3
"""
ASCII Engine IDE - A Processing-like IDE for ASCII art programming
Split-screen editor with live preview using curses
"""

import curses
import threading
import time
import sys
import os
import traceback
import importlib
import tempfile
from pathlib import Path
from ascii_engine.main import Canvas, COLORS

class CodeEditor:
    def __init__(self, stdscr, y, x, height, width):
        self.stdscr = stdscr
        self.y = y
        self.x = x
        self.height = height
        self.width = width
        self.lines = ["# ASCII Engine Sketch", "# Define your setup() and draw() functions", "", "def setup():", "    pass", "", "def draw():", "    # Your animation code here", "    pass"]
        self.cursor_y = 8
        self.cursor_x = 4
        self.scroll_y = 0
        self.current_file = None
        self.cursor_blink_counter = 0
        
        # Create a window for the editor
        self.win = curses.newwin(height, width, y, x)
        self.win.keypad(True)
        
        # Buffer tracking for efficient updates
        self.needs_redraw = True
        self.last_cursor_pos = (0, 0)
        
        # Initialize colors
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_WHITE)  # For cursor
        
    def draw_editor(self):
        # Update cursor blink counter
        self.cursor_blink_counter = (self.cursor_blink_counter + 1) % 10
        cursor_visible = self.cursor_blink_counter < 7  # Visible for 7/10 frames
        
        # Only redraw if needed or for cursor blinking
        current_cursor_pos = (self.cursor_y, self.cursor_x)
        if not self.needs_redraw and current_cursor_pos == self.last_cursor_pos and cursor_visible:
            return
            
        try:
            self.win.erase()
            self.win.border()
            
            # Title
            title = f" Code Editor {f'- {self.current_file}' if self.current_file else ''} "
            self.win.addstr(0, 2, title, curses.color_pair(2))
            
            # Line numbers and content
            visible_height = self.height - 2
            for i in range(visible_height):
                line_idx = self.scroll_y + i
                if line_idx >= len(self.lines):
                    break
                    
                y_pos = i + 1
                
                # Line number
                line_num = f"{line_idx + 1:3d} "
                self.win.addstr(y_pos, 1, line_num, curses.color_pair(3))
                
                # Line content with basic syntax highlighting
                line = self.lines[line_idx]
                if len(line) > self.width - 6:
                    line = line[:self.width - 9] + "..."
                    
                self.highlight_syntax(y_pos, 5, line, line_idx == self.cursor_y, cursor_visible)
                
            self.win.noutrefresh()  # Use noutrefresh for better performance
            self.needs_redraw = False
            self.last_cursor_pos = current_cursor_pos
            
        except curses.error:
            pass  # Ignore curses errors
        
    def highlight_syntax(self, y, x, line, is_cursor_line=False, cursor_visible=True):
        """Basic Python syntax highlighting with cursor support"""
        keywords = ['def', 'class', 'if', 'else', 'elif', 'for', 'while', 'return', 'import', 'from', 'pass']
        
        i = 0
        cursor_drawn = False
        
        while i < len(line) and x + i < self.width - 2:
            char = line[i]
            color = curses.color_pair(1)  # Default white
            
            # Check if this is the cursor position
            is_cursor_pos = is_cursor_line and i == self.cursor_x and cursor_visible
            
            # Comments
            if char == '#':
                remaining = line[i:]
                for j, ch in enumerate(remaining):
                    if x + i + j >= self.width - 2:
                        break
                    ch_color = curses.color_pair(6) if (is_cursor_line and i + j == self.cursor_x and cursor_visible) else curses.color_pair(4)
                    self.win.addstr(y, x + i + j, ch, ch_color)
                break
                
            # Strings
            elif char in ['"', "'"]:
                quote = char
                string_start = i
                i += 1
                while i < len(line) and line[i] != quote:
                    i += 1
                if i < len(line):
                    i += 1
                string_content = line[string_start:i]
                for j, ch in enumerate(string_content):
                    if x + string_start + j >= self.width - 2:
                        break
                    ch_color = curses.color_pair(6) if (is_cursor_line and string_start + j == self.cursor_x and cursor_visible) else curses.color_pair(4)
                    self.win.addstr(y, x + string_start + j, ch, ch_color)
                continue
                
            # Keywords
            elif char.isalpha() or char == '_':
                word_start = i
                while i < len(line) and (line[i].isalnum() or line[i] == '_'):
                    i += 1
                word = line[word_start:i]
                if word in keywords:
                    base_color = curses.color_pair(2)
                else:
                    base_color = curses.color_pair(1)
                    
                for j, ch in enumerate(word):
                    if x + word_start + j >= self.width - 2:
                        break
                    ch_color = curses.color_pair(6) if (is_cursor_line and word_start + j == self.cursor_x and cursor_visible) else base_color
                    self.win.addstr(y, x + word_start + j, ch, ch_color)
                continue
                
            # Numbers
            elif char.isdigit():
                num_start = i
                while i < len(line) and (line[i].isdigit() or line[i] == '.'):
                    i += 1
                number = line[num_start:i]
                for j, ch in enumerate(number):
                    if x + num_start + j >= self.width - 2:
                        break
                    ch_color = curses.color_pair(6) if (is_cursor_line and num_start + j == self.cursor_x and cursor_visible) else curses.color_pair(3)
                    self.win.addstr(y, x + num_start + j, ch, ch_color)
                continue
                
            # Regular characters
            else:
                if x + i < self.width - 2:
                    char_color = curses.color_pair(6) if is_cursor_pos else color
                    self.win.addstr(y, x + i, char, char_color)
                i += 1
                
        # Draw cursor at end of line if that's where it is
        if is_cursor_line and self.cursor_x >= len(line) and x + len(line) < self.width - 2 and cursor_visible:
            self.win.addstr(y, x + len(line), ' ', curses.color_pair(6))
                
    def handle_key(self, key):
        self.needs_redraw = True  # Mark that we need to redraw
        
        if key == curses.KEY_UP and self.cursor_y > 0:
            self.cursor_y -= 1
            self.cursor_x = min(self.cursor_x, len(self.lines[self.cursor_y]))
            self.adjust_scroll()
        elif key == curses.KEY_DOWN and self.cursor_y < len(self.lines) - 1:
            self.cursor_y += 1
            self.cursor_x = min(self.cursor_x, len(self.lines[self.cursor_y]))
            self.adjust_scroll()
        elif key == curses.KEY_LEFT and self.cursor_x > 0:
            self.cursor_x -= 1
        elif key == curses.KEY_RIGHT and self.cursor_x < len(self.lines[self.cursor_y]):
            self.cursor_x += 1
        elif key == curses.KEY_HOME:
            self.cursor_x = 0
        elif key == curses.KEY_END:
            self.cursor_x = len(self.lines[self.cursor_y])
        elif key == ord('\n') or key == curses.KEY_ENTER:
            self.insert_newline()
        elif key == curses.KEY_BACKSPACE or key == 127:
            self.handle_backspace()
        elif key == curses.KEY_DC:  # Delete
            self.handle_delete()
        elif 32 <= key <= 126:  # Printable characters
            self.insert_char(chr(key))
            
    def insert_char(self, char):
        line = self.lines[self.cursor_y]
        self.lines[self.cursor_y] = line[:self.cursor_x] + char + line[self.cursor_x:]
        self.cursor_x += 1
        
    def insert_newline(self):
        current_line = self.lines[self.cursor_y]
        left_part = current_line[:self.cursor_x]
        right_part = current_line[self.cursor_x:]
        
        self.lines[self.cursor_y] = left_part
        self.lines.insert(self.cursor_y + 1, right_part)
        
        self.cursor_y += 1
        self.cursor_x = 0
        self.adjust_scroll()
        
    def handle_backspace(self):
        if self.cursor_x > 0:
            line = self.lines[self.cursor_y]
            self.lines[self.cursor_y] = line[:self.cursor_x-1] + line[self.cursor_x:]
            self.cursor_x -= 1
        elif self.cursor_y > 0:
            # Join with previous line
            current_line = self.lines[self.cursor_y]
            previous_line = self.lines[self.cursor_y - 1]
            self.cursor_x = len(previous_line)
            self.lines[self.cursor_y - 1] = previous_line + current_line
            del self.lines[self.cursor_y]
            self.cursor_y -= 1
            self.adjust_scroll()
            
    def handle_delete(self):
        if self.cursor_x < len(self.lines[self.cursor_y]):
            line = self.lines[self.cursor_y]
            self.lines[self.cursor_y] = line[:self.cursor_x] + line[self.cursor_x+1:]
        elif self.cursor_y < len(self.lines) - 1:
            # Join with next line
            current_line = self.lines[self.cursor_y]
            next_line = self.lines[self.cursor_y + 1]
            self.lines[self.cursor_y] = current_line + next_line
            del self.lines[self.cursor_y + 1]
            
    def adjust_scroll(self):
        visible_height = self.height - 2
        if self.cursor_y < self.scroll_y:
            self.scroll_y = self.cursor_y
        elif self.cursor_y >= self.scroll_y + visible_height:
            self.scroll_y = self.cursor_y - visible_height + 1
            
    def get_code(self):
        return '\n'.join(self.lines)
        
    def save_file(self, filename):
        try:
            with open(filename, 'w') as f:
                f.write(self.get_code())
            self.current_file = os.path.basename(filename)
            return True
        except Exception as e:
            return False
            
    def load_file(self, filename):
        try:
            with open(filename, 'r') as f:
                content = f.read()
            self.lines = content.split('\n')
            self.cursor_y = 0
            self.cursor_x = 0
            self.scroll_y = 0
            self.current_file = os.path.basename(filename)
            return True
        except Exception as e:
            return False

class LivePreview:
    def __init__(self, stdscr, y, x, height, width):
        self.stdscr = stdscr
        self.y = y
        self.x = x
        self.height = height
        self.width = width
        self.canvas = None
        self.running = False
        self.error_message = None
        self.fps = 5  # Reduce FPS to reduce flickering
        self.frame_count = 0
        
        # Create window for preview
        self.win = curses.newwin(height, width, y, x)
        
        # Canvas dimensions (accounting for border and title)
        self.canvas_height = height - 3
        self.canvas_width = width - 2
        
        # Buffer for current display content
        self.display_buffer = []
        self.needs_redraw = True
        
    def start_preview(self, code):
        self.running = True
        self.error_message = None
        
        # Create canvas
        self.canvas = Canvas(self.canvas_height, self.canvas_width)
        
        # Execute code in thread
        self.preview_thread = threading.Thread(target=self._run_preview, args=(code,))
        self.preview_thread.daemon = True
        self.preview_thread.start()
        
    def stop_preview(self):
        self.running = False
        
    def _run_preview(self, code):
        try:
            # Create execution namespace
            namespace = {
                'canvas': self.canvas,
                'Canvas': Canvas,
                'COLORS': COLORS,
                'randint': __import__('random').randint,
                'math': __import__('math'),
                'time': __import__('time')
            }
            
            # Execute user code
            exec(code, namespace)
            
            # Get setup and draw functions
            setup_func = namespace.get('setup')
            draw_func = namespace.get('draw')
            
            # Run setup once
            if setup_func and callable(setup_func):
                setup_func()
                
            # Animation loop
            while self.running:
                if draw_func and callable(draw_func):
                    self.canvas.clear()
                    draw_func()
                    self.frame_count += 1
                    self.needs_redraw = True
                    
                time.sleep(1.0 / self.fps)
                
        except Exception as e:
            self.error_message = f"Error: {str(e)}\n{traceback.format_exc()}"
            self.needs_redraw = True
            
    def draw_preview(self):
        # Only redraw if needed
        if not self.needs_redraw:
            return
            
        try:
            # Clear and redraw border
            self.win.erase()
            self.win.border()
            
            # Title
            title = f" Live Preview ({self.frame_count}) "
            self.win.addstr(0, 2, title, curses.color_pair(2))
            
            if self.error_message:
                # Show error message
                lines = self.error_message.split('\n')
                for i, line in enumerate(lines[:self.height - 3]):
                    if len(line) > self.width - 3:
                        line = line[:self.width - 6] + "..."
                    try:
                        self.win.addstr(i + 1, 1, line, curses.color_pair(5))
                    except:
                        pass
            elif self.canvas:
                # Render canvas content efficiently
                try:
                    for row in range(min(self.canvas_height, self.canvas.rows)):
                        canvas_line = ''.join(self.canvas.canvas[row])
                        # Strip ANSI codes for curses display
                        display_line = self._strip_ansi(canvas_line)
                        if len(display_line) > self.canvas_width:
                            display_line = display_line[:self.canvas_width]
                        if display_line.strip():  # Only draw non-empty lines
                            self.win.addstr(row + 1, 1, display_line)
                except curses.error:
                    pass  # Ignore cursor positioning errors
            else:
                # Show waiting message
                msg = "Press F5 to run code"
                if len(msg) < self.width - 2:
                    self.win.addstr(self.height // 2, (self.width - len(msg)) // 2, msg, curses.color_pair(3))
            
            self.win.noutrefresh()  # Use noutrefresh instead of refresh
            self.needs_redraw = False
            
        except curses.error:
            pass  # Ignore any curses errors
        
    def _strip_ansi(self, text):
        """Remove ANSI escape codes for curses display"""
        import re
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)

class ASCIIEngineIDE:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        
        # Initialize curses
        curses.curs_set(0)  # Hide default cursor, we'll draw our own
        curses.start_color()
        curses.use_default_colors()
        stdscr.keypad(True)
        stdscr.timeout(100)
        
        # Calculate split layout
        editor_width = int(self.width * 0.6)
        preview_width = self.width - editor_width
        
        # Create components
        self.editor = CodeEditor(stdscr, 0, 0, self.height - 2, editor_width)
        self.preview = LivePreview(stdscr, 0, editor_width, self.height - 2, preview_width)
        
        # Status bar
        self.status_y = self.height - 2
        
        self.running = True
        
    def draw_status_bar(self):
        try:
            status_line = " F5: Run | Ctrl+S: Save | Ctrl+O: Open | Ctrl+Q: Quit "
            self.stdscr.addstr(self.status_y, 0, status_line.ljust(self.width), curses.color_pair(2))
            self.stdscr.addstr(self.status_y + 1, 0, f" Cursor: {self.editor.cursor_y+1}:{self.editor.cursor_x+1} ".ljust(self.width))
            self.stdscr.noutrefresh()  # Use noutrefresh for better performance
        except curses.error:
            pass
        
    def handle_shortcuts(self, key):
        if key == 5:  # Ctrl+E (run code)
            code = self.editor.get_code()
            self.preview.stop_preview()
            self.preview.start_preview(code)
        elif key == 19:  # Ctrl+S (save)
            self.save_dialog()
        elif key == 15:  # Ctrl+O (open)
            self.open_dialog()
        elif key == 17:  # Ctrl+Q (quit)
            self.running = False
        elif key == 27:  # ESC (quit)
            self.running = False
        elif key == curses.KEY_F5:  # F5 (run)
            code = self.editor.get_code()
            self.preview.stop_preview()
            self.preview.start_preview(code)
            
    def save_dialog(self):
        # Simple save - in a full implementation this would show a file dialog
        filename = f"sketch_{int(time.time())}.py"
        if self.editor.save_file(filename):
            # Show save success briefly
            pass
            
    def open_dialog(self):
        # Simple implementation - would show file browser in full version
        pass
        
    def run(self):
        # Initialize curses settings for better performance
        curses.curs_set(1)
        self.stdscr.nodelay(1)  # Non-blocking input
        self.stdscr.timeout(50)  # 50ms timeout for getch
        
        last_update = time.time()
        
        while self.running:
            try:
                current_time = time.time()
                
                # Handle input
                key = self.stdscr.getch()
                
                if key == -1:  # No key pressed
                    # Update display periodically for cursor blinking
                    if current_time - last_update > 0.1:  # 100ms
                        self.editor.needs_redraw = True  # Force redraw for cursor blink
                        self.update_display()
                        last_update = current_time
                elif key in [5, 19, 15, 17, 27, curses.KEY_F5]:  # Shortcuts
                    self.handle_shortcuts(key)
                    self.update_display()
                    last_update = current_time
                else:
                    self.editor.handle_key(key)
                    self.update_display()
                    last_update = current_time
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                # In a real implementation, log this error
                pass
                
        self.preview.stop_preview()
        
    def update_display(self):
        """Update display using double buffering"""
        try:
            # Update components
            self.editor.draw_editor()
            self.preview.draw_preview()
            self.draw_status_bar()
            
            # Refresh all windows at once (double buffering)
            curses.doupdate()
            
        except curses.error:
            pass

def main():
    def run_ide(stdscr):
        ide = ASCIIEngineIDE(stdscr)
        ide.run()
        
    curses.wrapper(run_ide)

if __name__ == "__main__":
    main()