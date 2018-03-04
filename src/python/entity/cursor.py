from curses import *

class Cursor:

    def __init__(self, screen, BORDER_COLOR, text=""):
        self.text = text.split("\n")
        self.count = 0
        self.x = 0
        self.y = 0
        self.scroll_from_line = 0
        self.screen = screen

        height, width = screen.getmaxyx()
        self.screen_width = width - 1  # coordinate begin with 0, screen_width begin with 1
        self.screen_height = height - 1  # coordinate begin with 0, screen_height begin with 1
        self.BORDER_COLOR = BORDER_COLOR
        self._updateScreen()

    def moveRight(self):
        self._updateXY()
        if not self.atEndOfLine():
            self._move(self.x + 1, self.y)

    def moveLeft(self):
        self._updateXY()
        if self.x > 0:
            self._move(self.x - 1, self.y)

    def moveDown(self, call_from="keyboard"):
        self._updateXY()
        if self.canScrollDown() and self.atBottomOfScreen() and call_from != "newline_function":
            self.scroll_from_line += 1

        self._updateScreen()

        if not self.goBeyondTextLength() and not self.atBottomOfScreen():
            self._move(self.x, self.y + 1)
        self.moveToRightMost()

    def moveUp(self):
        self._updateXY()
        if self.scroll_from_line > 0 and self.y == 0:
            self.scroll_from_line -= 1
        self._updateScreen()
        if self.y > 0:
            self._move(self.x, self.y - 1)
            self.moveToRightMost()

    def newLine(self):
        self._updateXY()
        if self.atBottomOfScreen():
            self.scroll_from_line += 1
        if self.atEndOfLine():
            self.text.insert(self.y + self.scroll_from_line + 1, "")
        else:
            line = self.text[self.y]
            self.text[self.y] = line[:self.x]
            self.text.insert(self.y + self.scroll_from_line + 1, line[self.x:])

        self._updateScreen()
        self.moveDown("newline_function")
        self.moveToLeftMost()

    def writeChar(self, char):
        self._updateXY()
        if self.scroll_from_line == 0:
            self.text[self.y] = self._insert(char, self.text[self.y], self.x)
        elif self.scroll_from_line > 0 and not self.goBeyondScreenHeight():
            self.text[self.y + self.scroll_from_line] = self._insert(char, self.text[self.y + self.scroll_from_line], self.x)
        elif self.scroll_from_line > 0 and self.atBottomOfScreen():
            self.text[self.y + self.scroll_from_line] += chr(char)
        self._updateScreen()
        self.moveRight()

    def tab(self):
        self.writeChar(32)
        self.writeChar(32)
        self.writeChar(32)

    def delete(self):
        self._updateXY()
        if self.currentLineIsEmpty() and not self.atTopOfScreen():
            self.text.pop(self.y)
            self._updateScreen()
            self.moveUp()
            self.moveToRightMost()
        elif self.currentLineIsNotEmpty() and self.atEndOfLine():
            self.text[self.y] = self.text[self.y][:-1]
            self._updateScreen()
            self.moveLeft()
        elif self.atMiddleOfLine() and not self.atBeginOfLine():
            self.text[self.y] = self._removeChar(self.text[self.y], self.x - 1)
            self._updateScreen()
            self.moveLeft()
        elif self.atBeginOfLine() and not self.atTopOfScreen():
            index = len(self.text[self.y - 1])
            self.text[self.y - 1] += self.text.pop(self.y)
            self._updateScreen()
            self.moveUp()
            self._move(index, self.y)

    def moveToLeftMost(self):
        self._updateXY()
        self._move(0, self.y)

    def moveToRightMost(self):
        self._updateXY()
        self._move(len(self.text[self.y + self.scroll_from_line]), self.y)

    def moveToRightBottomMost(self):
        self._updateXY()
        if self.textLengthBiggerThanScreenHeight():
            self.scroll_from_line = self._getTextLength() - self.screen_height

        self._updateScreen()
        if not self.textLengthBiggerThanScreenHeight():
            self._move(0, self._getTextLength())
        else:
            self._move(0, self.screen_height)
        self.moveToRightMost()

    def moveToRightUpMost(self):
        self._updateXY()
        self.scroll_from_line = 0
        self._updateScreen()
        self._move(0 ,0)
        self.moveToRightMost()


    def getText(self):
        return "\n".join(self.text)

    def deleteWholeLine(self):
        self._updateXY()
        self.text[self.y] = self.text[self.y][self.x:]
        self._updateScreen()
        self.moveToLeftMost()

    def resizeTextBox(self):
        height, width = self.screen.getmaxyx()
        self.screen_height, self.screen_width = height - 1, width - 1
        if self.goBeyondScreenHeight():
            self.y = self.screen_height
            self.x = len(self.text[self.y])
        self._updateScreen()

    ### private function ###
    def _updateScreen(self):
        curs_set(0) # hide cursor, so user don't see it flash while updating screen

        # write ~ in the beginning of each row
        self.screen.clear()
        for y in range(len(self.text), self.screen_height):
            self.screen.addstr(y, 0, "~", color_pair(self.BORDER_COLOR))

        # input text to it
        begin = self.scroll_from_line
        end = self.scroll_from_line + self.screen_height + 1
        text_array = self.text[begin: end]

        text = "\n".join(text_array)
        self.screen.addstr(0, 0, text)
        self._move(self.x, self.y)
        self.screen.refresh()
        curs_set(1)

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

    def _debug(self, textToPrint):
        with open("debug.log", "a") as file:
            file.write(textToPrint)
            file.write("\n")

    def _getTextLength(self):
        return len(self.text) - 1 # len() is base 1, -1 to cast it to base 0, for consistent with other variables

    ### boolean functions ###
    def atMiddleOfLine(self):
        return self.x < len(self.text[self.y + self.scroll_from_line])

    def atEndOfLine(self):
        return self.x >= len(self.text[self.y])

    def atBeginOfLine(self):
        return self.x == 0

    def atBottomOfScreen(self):
        return self.screen_height == self.y

    def atTopOfScreen(self):
        return self.y == 0

    def currentLineIsEmpty(self):
        return len(self.text[self.y]) == 0

    def currentLineIsNotEmpty(self):
        return not self.currentLineIsEmpty()

    def scrolling(self):
        return self.scroll_from_line > 0

    def textLengthBiggerThanScreenHeight(self):
        return self._getTextLength() > self.screen_height

    def goBeyondScreenHeight(self):
        return self.y > self.screen_height

    def goBeyondTextLength(self):
        return self.y >= self._getTextLength()

    def canScrollDown(self):
        return self._getTextLength() > self.scroll_from_line + self.screen_height