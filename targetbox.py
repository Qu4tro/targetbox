#!/usr/bin/python
# -*- encoding: utf-8 -*-

import termbox
import sys
import random
import logging as log
import time

log.basicConfig(filename='dev.log',level=log.DEBUG)

header_color = lambda c: (c, termbox.BLACK, termbox.RED)
active_color = lambda c: (c, termbox.BLACK, termbox.CYAN)
normal_color = lambda c: (c, termbox.WHITE, termbox.BLACK)

def size(t):
    return (t.width(), t.height())

def draw(t, grid, full=True):
    if full:
        w, h = size(t)
        assert(len(grid) == h)
        for line in grid:
            assert(len(line) == w)

    for height, line in enumerate(grid):
        for width, cell in enumerate(line):
            char, fg, bg = cell
            if fg == None:
                fg = termbox.WHITE
            if bg == None:
                bg = termbox.BLACK
         
            t.change_cell(width, height, char, fg, bg)
    t.present()

def add_header(width, grid, msg, color):
    fmt_line = msg.ljust(width)
    gridline = [color(ord(fmt_line[i])) for i in range(width)]

    return [gridline] + grid

# def add_footer(grid):
#     fmt_line = self.elements[i].ljust(width)
#     gridline = [color(ord(fmt_line[i])) for i in range(width)]

class Menu:
    def __init__(self, elements, cursor=0):
        self.cursor = cursor
        self.elements = elements
        self.last = len(self.elements) - 1

    @property
    def selected(self):
        return self.elements[self.cursor]

    def bound(self):
        if self.cursor < 0:
            self.goto(0)
        if self.cursor >= len(self.elements):
            self.goto(self.last)

    def wrap(self):
        if self.cursor < 0:
            self.goto(self.last)
        if self.cursor >= len(self.elements):
            self.goto(0)

    def goto(self, line):
        log.info(f"go from {self.cursor} to {line}")
        self.cursor = line
        self.bound()

    def go(self, incr):
        self.goto(self.cursor + incr)
    def move_up(self):
        self.go(-1)
    def move_down(self):
        self.go(1)

    def grid(self, width, height):
        grid = []
        for i in range(height):
            color = active_color if i == self.cursor else normal_color

            if i < len(self.elements):
                fmt_line = self.elements[i].ljust(width)
                gridline = [color(ord(fmt_line[i])) for i in range(width)]
            else:
                gridline = [color(ord(" ")) for i in range(width)]

            grid.append(gridline)
        return grid


def defaultMouseHandler(event, menu):
    pass

def defaultKeyHandler(event, menu):
    (event_type, ch, key, mod, w, h, x, y) = event
    if event_type == termbox.EVENT_KEY:
        if key == termbox.KEY_ARROW_DOWN:
            menu.move_down()
        elif key == termbox.KEY_ARROW_UP:
            menu.move_up()
        elif key == termbox.KEY_HOME:
            menu.goto(0)
        elif key == termbox.KEY_END:
            menu.goto(menu.last)

        elif key == termbox.KEY_ENTER:
            return menu.selected
        elif key == termbox.KEY_ESC:
            sys.exit()
        else:
            log.debug("key not found")


def start(model, keyHandler=None, mouseHandler=None):
    with termbox.Termbox() as t:
        draw(t, model.grid(*size(t)))
        while True:
            event = t.poll_event()
            while event:
                (type, ch, key, mod, w, h, x, y) = event

                if type == termbox.EVENT_RESIZE:
                    log.debug("redraw")
                    draw(t, model.grid(*size(t)))

                if type == termbox.EVENT_KEY:
                    if not(keyHandler):
                        keyHandler = defaultKeyHandler
                    
                    out = keyHandler(event, model)
                    if out:
                        return out

                if type == termbox.EVENT_MOUSE:
                    if not(keyHandler):
                        mouseHandler = defaultMouseHandler
                    
                    out = mouseHandler(event, model)
                    if out:
                        return out

                if type == termbox.EVENT_MOUSE:
                    if mouseHandler:
                        mouseHandler(event, model)

                event = t.peek_event()

            draw(t, model.grid(*size(t)))

    return ""

def main():
    elements = [str(random.random()) for x in range(100)]
    menu = Menu(elements)
    print(start(menu))

if __name__ == "__main__":
    main()
