# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an ASCII/ANSI-based creative coding environment inspired by Processing. It provides a terminal-based canvas for creating generative art, animations, and interactive visual experiences using ASCII characters and ANSI color codes.

## Project Structure

- `ascii_engine/main.py` - Main application file containing the Canvas class and animation loop

## Core Architecture

The engine follows a Processing-like paradigm with a `Canvas` class as the core drawing surface:
- **Canvas Management**: 2D grid representation of the terminal display for pixel-level control
- **Drawing Primitives**: Methods for drawing shapes (currently circles) with ANSI color support
- **Animation Loop**: Continuous clear/draw cycle for real-time animations
- **Color System**: ANSI escape code integration for terminal-based color rendering
- **Frame Management**: Uses `os.system("clear")` for frame-by-frame animation

## Running the Application

To run the creative coding environment:
```bash
python ascii_engine/main.py
```

The current demo creates a generative animation with 100 random yellow circles per frame, running at ~10 FPS.

## Development Notes

- Minimal Python project using only standard library for maximum portability
- Terminal-based rendering using ANSI escape codes for cross-platform color support
- Canvas dimensions: 50 rows × 150 columns (configurable in main.py:33-34)
- Extensible architecture designed for adding new drawing primitives and creative coding features
- Future expansion could include: lines, rectangles, text rendering, input handling, and Processing-style setup()/draw() pattern