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


class Screen(object):
    """
    The screen will be the object that will abstract over the physical representation of this menu. 
    """

    def __init__(self, terminal):

        self.terminal = terminal

        self.startY = 0
        self.endY = self.terminal.height()

        self.lines = []

        self.toUpdate = None


    def update(self):
        if toUpdate is None:
            draw_screen()
        else:
            for line in toUpdate:
                self.draw_line(line, present=False)

        self.terminal.present()

    def draw_line(self, n, present=False):
        """
        Draw the nth line
        """

        if n >= len(self.lines):
            log.warning("Don't have line number {}".format(n))
            return

        if not(self.startY < n < self.endY):
            log.warning(("Can't draw this line, because it isn't within the borders of the screen\nstartX = {}; endY = {}; lineNumber = {}; line = \n{}".format(self.startY, self.endY, n, self.lines[n])))
            return


        line = self.lines[n]
        for x, char in enumerate(line.chars):
            relative_y = line.absolute_y - self.startY
            line.interface.terminal.change_cell(x, relative_y, char, line.fg, line.bg)

        if present:
            self.terminal.present()

    def draw_screen(self, present=False):
        """
        Draw the visible screen
        """
        for line_number in range(self.startY, self.endY):
            self.draw_line(line_number, present=False)

        if present:
            self.terminal.present()

    def scrollup(self, n=1):
        self.startY -= n
        self.endY   -= n
        self.draw_screen()

    def scrolldown(self, n=1):
        self.startY += n
        self.endY   += n
        self.draw_screen()

        

class Line(object):

    def __init__(self, interface, content, y):

        log.info("Line being created.")

        self.interface = interface

        self.content = str(content)
        self.absolute_y = y

        self.relative_y = y # To be deprecated soon enough

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
        content setter does 2 things:
            * Keeps the value given with the self.original var
            * Format the string
        """
        self.original = value
        self.format_string()

    def format_string(self):
        """
        This function should format the input string in anyway you need
        and in the end update the self.chars to ASCCI so it's ready for consumption by change_cell
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
        

class SelectableLine(Line):

    def __init__(self, *args, **kwargs):
        super(SelectableLine, self).__init__(*args, **kwargs)
        self.selected = False

    def select(self):
        log.info("Line being selected!")
        self.selected = True
        self.fg = self.interface.colorscheme.selected_fg
        self.bg = self.interface.colorscheme.selected_bg

    def unselect(self):
        log.info("Line being unselected!")
        self.selected = False
        self.fg = self.interface.colorscheme.default_fg
        self.bg = self.interface.colorscheme.default_bg

class Menu(object):

    def __init__(self, interface, elements):
        log.info("Menu being created.")
        self.interface = interface

        self.elements = elements
        self.create_lines()

        self.position = 0

        self.startY = 0
        self.endY = self.interface.terminal.height()

    def create_lines(self):
        self.lines = []
        for absolute_y, element in enumerate(self.elements):
            self.lines.append(SelectableLine(self.interface, element, absolute_y))

    
    def up(self):
        self.goto(self.position - 1)

    def down(self):
        self.goto(self.position + 1)

    def goto(self, y):
        old_y = self.position
        margin = 0 # TODO: Implement optional margin

        if (y == old_y): # Nothing to be done
            return

        elif (y > old_y): # It went down

            # Check if it reached over the limit 
            maxLimit = len(self.lines) - 1
            if y > maxLimit:
                self.goto(maxLimit) # Keep it there
                # self.goto(0) # Wrap around


            # Check if we need to scroll
            if y > self.endY:
                # Scroll enough
                diff = y - self.endY
                self.interface.screen.scrolldown(diff)


        elif (y < old_y): # It went up

            # Check if it reached below the limit 
            minLimit = 0
            if y < minLimit:
                self.goto(minLimit) # Keep it there
                # self.goto(maxLimit) # Wrap around

            # Check if we need to scroll
            if y < self.startY:
                # Scroll enough
                diff = y - self.endY
                self.interface.screen.scrollup(diff)

        # Finally select the new line.
        # This will also take care of unselecting the other line.
        self.select_line(y)


    def select_line(self, n):

        self.lines[self.position].unselect()
        self.lines[n].select()

        self.interface.screen.draw_line(self.position, present=False)
        self.interface.screen.draw_line(n, present=False)

        self.interface.terminal.present()

        self.position = n

    def get_selected(self):
        return self.lines[self.position].content

class Interface(object):

    def __init__(self, terminal, colorscheme=default_colorscheme):
        self.terminal = terminal
        self.colorscheme = colorscheme
        self.menu = Menu(self, list(map(str, range(190))))
        self.screen = Screen(terminal)
        self.screen.lines = self.menu.lines

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
        # self.draw()
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
                # self.draw()
                event = self.terminal.peek_event()

    # def draw(self):
    #     self.menu.draw()


def main():
    with termbox.Termbox() as t:
        i = Interface(t)
        i.run()
        

if __name__ == '__main__':
    main()
