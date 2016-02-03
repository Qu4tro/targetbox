import termbox
import time
import random
import sys
from collections import namedtuple

import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)
log.disabled = 1

space = ord(u' ')

Colorscheme = namedtuple("Colorscheme", ['default_fg', 'default_bg',
                                         'selected_fg', 'selected_bg',
                                         'header_fg', 'header_bg'])

default_colorscheme = Colorscheme(termbox.WHITE, termbox.BLACK,
                                  termbox.BLACK, termbox.CYAN,
                                  termbox.BLACK, termbox.RED)

class Line(object):

    def __init__(self, interface, content, y):

        log.info("Line being created.")

        self.interface = interface

        self.content = str(content)
        self.y = y

        self.virtual_y = y

        self.fg = self.interface.colorscheme.default_fg
        self.bg = self.interface.colorscheme.default_bg


    @property
    def content(self):
        """
        Return the unmodified value.
        """
        return self.original

    @content.setter
    def content(self, value):
        """
        content setter does 3 things:
            * Keeps the value given with the self.original var
            * Strip extra-chars and pad the string when needed
            * Put it ready to being consumed by the change_cell 
                function by converting everything to ASCII
        """
        t_width = self.interface.terminal.width()

        self.original = value
        self.format_string()

    def format_string(self):
        """
        This function should format the input string in anyway you need
        and in the end update the self.chars to 
        In this case it strips any chars that can't be displayed and pad it.
        """
        # TODO: Padding here is a obvious hack.
        # Right now with this padding thing, it's obvious to me that this whole thing is a hack.
        # I should have an abstraction to an absolute line in the screen.
        t_width = self.interface.terminal.width()

        # Strip extra chars
        self.formatted_string = self.original[:t_width]
        # Fill spaces if line doesn't fill width
        self.formatted_string += ' ' * (t_width - len(self.formatted_string))

        # Ascii values
        self.chars = [ord(char) for char in self.formatted_string]
        

    def shift(self, n):
        """
        This simple function will shift the virtual_y (the "display" line) by a distance of n
        """
        log.debug("Shifting from line {} to line {} with n = {}.", self.virtual_y, self.virtual_y + n, n)
        self.virtual_y += n

    def draw(self, present=True):

        log.debug("Line being drawn!")

        for x, char in enumerate(self.chars):
            self.interface.terminal.change_cell(x, self.virtual_y, char, self.fg, self.bg)

        if present:
            self.interface.terminal.present()

class SelectableLine(Line):

    def __init__(self, *args, **kwargs):
        super(SelectableLine, self).__init__(*args, **kwargs)
        self.selected = False

    def select(self):
        log.info("Line being selected!")
        self.selected = True
        self.fg = self.interface.colorscheme.selected_fg
        self.bg = self.interface.colorscheme.selected_bg
        self.draw()

    def unselect(self):
        log.info("Line being unselected!")
        self.selected = False
        self.fg = self.interface.colorscheme.default_fg
        self.bg = self.interface.colorscheme.default_bg
        self.draw()

class Menu(object):

    def __init__(self, interface, elements):
        self.interface = interface

        self.elements = elements
        self.create_lines()

        self.selected = 0

        self.startY = 0
        self.endY = self.interface.terminal.height

        self.lines[self.selected].select()

    def create_lines(self):
        self.lines = []
        for y, element in enumerate(self.elements):
            self.lines.append(SelectableLine(self.interface, element, y))

    def draw(self, present=True):
        for line in self.lines:
            if self.interface.terminal.height >= line.virtual_y >= 0:
                line.draw(present=False)

        if present:
            self.interface.terminal.present()

    def up(self):
        self.goto(self.selected - 1)

    def down(self):
        self.goto(self.selected + 1)

    def scrollup(self, n=1):
        for line in self.lines:
            line.virtual_y -= n
        self.startY -= n
        self.endY -= n

    def scrolldown(self, n=1):
        for line in self.lines:
            line.virtual_y += n
        self.startY += n
        self.endY += n

    def goto(self, y):
        old_y = self.selected
        terminal_height = self.interface.terminal.height
        margin = 0 # TODO: Implement optional margin

        if (y == old_y): # Nothing to be done
            return

        elif (y > old_y): # It went down

            # Check if it reached over the limit 
            if y > len(self.lines):
                self.goto(0) # Wrap around

            # Check if we need to scroll
            if y > self.endY:
                diff = y - self.endY
                self.scrolldown(diff)


        elif (y < old_y): # It went up

            # Check if it reached below the limit 
            if y < 0:
                self.goto(len(self.lines)) # Wrap around

            # Check if we need to scroll
            if y < self.startY:
                diff = y - self.endY
                self.scrollup(diff)

        self.selected = y
        self.lines[self.selected].select()

        self.lines[old_y].unselect()

    def get_selected(self):
        return self.lines[selected].element

class Interface(object):

    def __init__(self, terminal, colorscheme=default_colorscheme):
        self.terminal = terminal
        self.colorscheme = colorscheme
        self.menu = Menu(self, list(map(str, range(190))))

    def resize(self):
        pass

    def keystroke(self, mod, key):
        if key == termbox.KEY_ESC:
            sys.exit()

        if key == termbox.KEY_ARROW_UP:
            self.menu.up()

        if key == termbox.KEY_ARROW_DOWN:
            self.menu.down()


    def run(self):
        self.draw()
        while True:
            event = self.terminal.poll_event()
            while event:
                (event_type, ch, key, mod, w, h, x, y) = event
                if event_type == termbox.EVENT_KEY:
                    self.keystroke(mod, key)
                if event_type == termbox.EVENT_MOUSE:
                    pass
                if event_type == termbox.EVENT_RESIZE:
                    self.resize()
                self.draw()
                event = self.terminal.peek_event()

    def draw(self):
        self.menu.draw()


def main():
    with termbox.Termbox() as t:
        i = Interface(t)
        i.run()
        

if __name__ == '__main__':
    main()
