from termbox import BLACK, CYAN
import logging as log

log.basicConfig(filename='dev.log', level=log.DEBUG)


class ListMenu:
    def __init__(self, elements, grid_size, cursor=0, wrap=True):
        self.elements = elements
        self.size = len(elements)
        self.grid_size = grid_size
        self.window = (0, grid_size[1] - 1)

        self.cursor = cursor

        self.wrap = wrap
        log.debug(f"# elements: {self.size}")
        log.debug(f"window: {self.window}")

    @property
    def selected(self):
        return self.elements[self.cursor]

    def goto(self, line):

        def bound(pos, size):
            return 0 if pos < 0 else size - 1 if pos >= size else pos

        def wrap(pos, size):
            return pos % size

        if self.wrap:
            self.cursor = wrap(line, self.size)
        else:
            self.cursor = bound(line, self.size)

        if self.cursor < self.window[0]:
            self.window = (self.cursor, self.cursor + self.grid_size[1] - 1)
        elif self.cursor > self.window[1]:
            self.window = (self.cursor - self.grid_size[1] + 1, self.cursor)

        log.debug(f"goto: {self.cursor}")
        log.debug(f"window: {self.window}")

    def go(self, incr):
        self.goto(self.cursor + incr)

    def move_up(self):
        self.go(-1)

    def move_down(self):
        self.go(1)

    def grid(self):
        return self.color([[(ord(c), None, None)
                            for c in element.ljust(self.grid_size[0])]
                           for element in self.elements[self.window[0]:self.window[1] + 1]])

    def color(self, grid):
        relative_cursor = self.cursor - self.window[0]
        grid[relative_cursor] = [(char, BLACK, CYAN)
                                 for (char, _, _) in grid[relative_cursor]]

        return grid
