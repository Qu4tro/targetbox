from termbox import BLACK, CYAN, WHITE
import logging as log

log.basicConfig(filename='dev.log', level=log.DEBUG)


class ListMenu:
    def __init__(self, elements, cursor=0, wrap=True):
        self.elements = elements
        self.size = len(self.elements)
        self.window_size = None

        self.cursor = cursor

        self.wrap = wrap

    @property
    def selected(self):
        return self.elements[self.cursor]

    def goto(self, line):
        def bound(pos, size):
            return 0 if pos < 0 else size - 1 if pos >= size else pos

        def wrap(pos, size):
            return pos % size

        log.info(f"goto: {self.cursor} -> {line}")
        if self.wrap:
            self.cursor = wrap(line, self.size)
        else:
            self.cursor = bound(line, self.size)

        if self.cursor != line:
            if self.wrap:
                log.info(f"wrapped to {self.cursor}")
            else:
                log.info(f"bound to {self.cursor}")

    def go(self, incr):
        self.goto(self.cursor + incr)

    def move_up(self):
        self.go(-1)

    def move_down(self):
        self.go(1)

    def grid(self):
        if self.window_size is not None:
            (width, height) = self.window_size
        else:
            raise "sup"  # TODO

        # TODO
        def active_color(c):
            return c, BLACK, CYAN

        # TODO
        def normal_color(c):
            return c, WHITE, BLACK

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
