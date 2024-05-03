import os
import time
from random import randint

COLORS = {
  'black': '\u001b[30m',
  'yellow': '\u001b[33m'
}

class Canvas:
    def __init__(self, rows, cols):
        self.blank = '.'
        self.rows = rows
        self.cols = cols
        self.canvas = [[self.blank for c in range(cols)] for r in range(rows)]

    def draw(self):
        for r in range(self.rows):
            for c in range(self.cols):
                print(self.canvas[r][c], end='')
            print("")

    def circle(self, r, c):
        self.canvas[r][c] = f"{COLORS['yellow']}/{COLORS['black']}"

    def clear(self):
        for r in range(self.rows):
            for c in range(self.cols):
                self.canvas[r][c] = self.blank
        os.system("clear")

if __name__ == "__main__":
    rows = 50
    cols = 150
    c = Canvas(rows, cols)
    while True:
        c.clear()
        for j in range(100):
            c.circle(randint(0, rows-1), randint(0, cols-1))
        c.draw()
        time.sleep(0.1)

