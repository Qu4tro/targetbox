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
#     fmt_line = self.choices[i].ljust(width)
#     gridline = [color(ord(fmt_line[i])) for i in range(width)]

class Menu:
    def __init__(self, choices, active=0):
        self.active = active
        self.choices = choices
        self.last = len(self.choices) - 1

    def bound(self):
        if self.active < 0:
            self.goto(0)
        if self.active >= len(self.choices):
            self.goto(self.last)

    def wrap(self):
        if self.active < 0:
            self.goto(self.last)
        if self.active >= len(self.choices):
            self.goto(0)

    def goto(self, line):
        self.active = line
        self.bound()

    def go(self, incr):
        self.goto(self.active + incr)
    def move_up(self):
        self.go(-1)
    def move_down(self):
        self.go(1)

    def grid(self, width, height):
        grid = []
        for i in range(height):
            color = active_color if i == self.active else normal_color

            if i < len(self.choices):
                fmt_line = self.choices[i].ljust(width)
                gridline = [color(ord(fmt_line[i])) for i in range(width)]
            else:
                gridline = [color(ord(" ")) for i in range(width)]

            grid.append(gridline)
        return grid


def updateKeyEvent(event, menu):
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


def final_grid(t, menu):
    w, h = size(t)
    m = menu.grid(w, h - 1)
    mh = add_header(w, m, "Deus 4", header_color)

    return mh


def main():
    choices = [str(random.random()) for x in range(100)]
    with termbox.Termbox() as t:
        menu = Menu(choices)
        draw(t, final_grid(t, menu))
        i = 0
        while True:
            event = t.poll_event()
            while event:
                (type, ch, key, mod, w, h, x, y) = event

                if type == termbox.EVENT_RESIZE:
                    draw(t, final_grid(t, menu))

                if type == termbox.EVENT_KEY:
                    if key == termbox.KEY_ESC:
                        sys.exit()
                    updateKeyEvent(event, menu)

                if type == termbox.EVENT_MOUSE:
                    pass # TODO


                event = t.peek_event()

            draw(t, final_grid(t, menu))

if __name__ == "__main__":
    main()
