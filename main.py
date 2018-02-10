from curses import *


TERMINAL_RESIZE_EVENT = 410
CUSTOM_KEY_ESCAPE = 27
CUSTOM_KEY_BACKSPACE = 127
CUSTOM_KEY_ENTER = 10
CUSTOM_KEY_TAB = 9
BORDER = 1


def main(screen):
    use_default_colors()
    init_pair(69, COLOR_MAGENTA, -1)
    startEditing(screen)


def startEditing(screen):
    cursor = Cursor(screen)
    while 1:
        char = screen.getch()
        if char == KEY_F1:
            break
        elif char == KEY_RIGHT:
            cursor.moveRight()
        elif char == KEY_LEFT:
            cursor.moveLeft()
        elif char == KEY_UP:
            cursor.moveUp()
        elif char == KEY_DOWN:
            cursor.moveDown()
        elif 31 < char < 127:
            cursor.writeChar(char)
        elif char == CUSTOM_KEY_BACKSPACE:
            cursor.delete()
        elif char == 10:
            cursor.newLine()
        elif char == CUSTOM_KEY_TAB:
            cursor.tab()
        else:
            cursor._writeString(str(char))


class Cursor:

    def __init__(self, screen, text=""):
        self.text = text.split("\n")
        self.x = 0
        self.y = 0
        self.screen = screen

        height, width = screen.getmaxyx()
        self.screen_width = width - 1  # coordinate begin with 0, screen_width begin with 1
        self.screen_height = height - 1  # coordinate begin with 0, screen_height begin with 1
        self._updateScreen()

    def moveRight(self):
        self._updateXY()
        if self.x < len(self.text[self.y]):
            self._move(self.x + 1, self.y)

    def moveLeft(self):
        self._updateXY()
        if self.x > 0:
            self._move(self.x - 1, self.y)

    def moveDown(self):
        self._updateXY()
        if self.y < len(self.text) - 1 and self.y < self.screen_height:
            self._move(self.x, self.y + 1)

    def moveUp(self):
        self._updateXY()
        if self.y > 0:
            self._move(self.x, self.y - 1)

    def newLine(self):
        self._updateXY()
        if self.x >= len(self.text[self.y]): # at tail of line
            self.text.insert(self.y + 1, "")
        else:
            line = self.text[self.y]
            self.text[self.y] = line[:self.x]
            self.text.insert(self.y + 1, line[self.x:])

        self._updateScreen()
        self.moveDown()
        self.moveToLeftMost()

    def writeChar(self, char):
        self._updateXY()
        self.text[self.y] = self._insert(char, self.text[self.y], self.x)

        self._updateScreen()
        self.moveRight()

    def tab(self):
        self.writeChar(32)
        self.writeChar(32)
        self.writeChar(32)

    def delete(self):
        self._updateXY()
        if len(self.text[self.y]) == 0 and self.y != 0: # at empyty line, self.y != 0
            self.text.pop(self.y)
            self._updateScreen()
            self.moveUp()
            self.moveToRightMost()
        elif len(self.text[self.y]) > 0 and len(self.text[self.y]) == self.x: # at tail of line, self.x > 0
            self.text[self.y] = self.text[self.y][:-1]
            self._updateScreen()
            self.moveLeft()
        elif self.x < len(self.text[self.y]) and self.x != 0: # at middle of line, self.x > 0
            self.text[self.y] = self._removeChar(self.text[self.y], self.x - 1)
            self._updateScreen()
            self.moveLeft()
        elif self.x == 0 and self.y != 0: # at beginning of line, self.y != 0
            index = len(self.text[self.y - 1])
            self.text[self.y - 1] += self.text.pop(self.y)
            self._updateScreen()
            self.moveUp()
            self._move(index, self.y - 1)

    def moveToLeftMost(self):
        self._updateXY()
        self._move(0, self.y)

    def moveToRightMost(self):
        self._updateXY()
        self._move(len(self.text[self.y]), self.y)

    ### private function ###
    def _updateScreen(self):
        # curs_set(0) # hide cursor, so user don't see it flash while updating screen

        # write ~ in the beginning of each row
        self.screen.clear()
        for y in range(len(self.text), self.screen_height):
            self.screen.addstr(y, 0, "~", color_pair(69))

        # input text to it
        text_array = self.text[0: self.screen_height + 1]

        text = "\n".join(text_array)
        self.screen.addstr(0, 0, text)
        self._move(self.x, self.y)
        self.screen.refresh()
        # curs_set(1)

    def _move(self, x, y):
        self.screen.move(y, x)

    def _writeString(self, str):
        self.screen.addstr(str)
        self.moveRight()

    def _updateXY(self):
        self.y, self.x = self.screen.getyx()

    def _insert(self, char, text, index):
        return text[:index] + chr(char) + text[index:]

    def _removeChar(self, text, index):
        return text[:index] + text[index + 1:]


if __name__== "__main__":
    wrapper(main)

# todo
# make it run on mac terminal
# refactor