# ASCII Engine

An ASCII/ANSI-based creative coding environment inspired by Processing. Create generative art, animations, and interactive visual experiences using ASCII characters and ANSI color codes directly in your terminal.

## Features

- Terminal-based canvas for pixel-level control
- Drawing primitives with ANSI color support
- Real-time animation loop (~10 FPS)
- Processing-like paradigm with Canvas class
- Cross-platform color rendering using ANSI escape codes
- Minimal dependencies (Python standard library only)

## Installation

No external dependencies required. Just clone and run:

```bash
git clone <repository-url>
cd ascii-engine
python ascii_engine/main.py
```

## Usage

Run the demo animation:

```bash
python ascii_engine/main.py
```

The current demo creates a generative animation with 100 random yellow circles per frame.

## Architecture

- **Canvas**: 50×150 character grid for drawing
- **Drawing Primitives**: Circle drawing with color support
- **Animation Loop**: Continuous clear/draw cycle
- **Color System**: ANSI escape codes for terminal colors

## Development

The engine is designed for extensibility. Future features could include:
- Additional drawing primitives (lines, rectangles, text)
- Input handling for interactivity
- Processing-style setup()/draw() pattern
- Configurable canvas dimensions

## Requirements

- Python 3.x
- Terminal with ANSI color support