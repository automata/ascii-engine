#!/usr/bin/env python3
"""
ASCII Engine IDE Launcher
Provides better error handling and terminal compatibility
"""

import os
import sys
import curses

def check_terminal():
    """Check if terminal supports curses"""
    try:
        # Try to initialize curses
        stdscr = curses.initscr()
        curses.endwin()
        return True
    except:
        return False

def main():
    print("ASCII Engine IDE")
    print("================")
    
    # Check terminal compatibility
    if not check_terminal():
        print("❌ Error: Your terminal doesn't support curses")
        print("\nTry running in:")
        print("- Terminal.app (macOS)")
        print("- iTerm2 (macOS)")
        print("- gnome-terminal (Linux)")
        print("- xterm (Linux/Unix)")
        print("- Windows Terminal (Windows)")
        print("\nDo NOT run in:")
        print("- IDE output panels")
        print("- VS Code integrated terminal")
        print("- PyCharm terminal")
        return 1
    
    # Check terminal size
    try:
        rows, cols = os.popen('stty size', 'r').read().split()
        rows, cols = int(rows), int(cols)
        
        if rows < 24 or cols < 80:
            print(f"⚠️  Warning: Terminal size is {cols}x{rows}")
            print("   Recommended minimum: 80x24 characters")
            print("   For best experience: 120x40 characters")
            
            response = input("\nContinue anyway? (y/n): ")
            if response.lower() != 'y':
                return 0
    except:
        pass
    
    print("\n🚀 Starting ASCII Engine IDE...")
    print("   Use F5 to run code, Ctrl+Q to quit")
    print("   Press any key to continue...")
    input()
    
    # Import and run IDE
    try:
        from ascii_ide import main as ide_main
        ide_main()
    except KeyboardInterrupt:
        print("\n👋 IDE closed by user")
    except Exception as e:
        print(f"\n❌ Error starting IDE: {e}")
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(main())