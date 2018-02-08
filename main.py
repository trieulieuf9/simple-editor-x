from curses import *
import sys
import os
from subprocess import call

# add the word custom, so we will mistaken them with variable inside Curses library
TERMINAL_RESIZE_EVENT = 410
CUSTOM_KEY_ESCAPE = 27
CUSTOM_KEY_BACKSPACE = 127
CUSTOM_KEY_ENTER = 10
CUSTOM_KEY_TAB = 9
BORDER = 1

def main(screen, file_path):
    with open("debug.log", 'w'):
        pass


    setUpEnv()
    text = readFileIfExist(file_path)
    while 1:
        try:
            text = startEditing(screen, text)
            printQuitOptions(screen)
            char = screen.getch()
            if char == CUSTOM_KEY_ENTER:
                with open(file_path, "w+") as file:
                    file.write(text)
                return 0
            elif char == KEY_F9:
                break
        except KeyboardInterrupt: # quit properly, when user press Ctrl + C
            return 1
        # except:  put it back, when done with development
        #     return -1

def setUpEnv():
    use_default_colors()
    init_pair(BORDER, COLOR_MAGENTA, -1)

def readFileIfExist(file_path):
    text = ""
    if os.path.isfile(file_path):
        with open(file_path, "r") as file:
            text = file.read()
    return text


def startEditing(screen, text):
    cursor = Cursor(screen, text)
    while 1:
        char = screen.getch()
        if char == KEY_F1:
            break
        elif char == TERMINAL_RESIZE_EVENT:
            cursor.resizeTextBox()
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
        elif char == 10 or char == 13 or char == KEY_ENTER:
            cursor.newLine()
        elif char == CUSTOM_KEY_TAB:
            cursor.tab()
        elif char == CUSTOM_KEY_ESCAPE:
            char = screen.getch()  # get the key pressed after cmd
            if char == KEY_LEFT:
                cursor.moveToLeftMost()
            elif char == KEY_RIGHT:
                cursor.moveToRightMost()
            elif char == 127: # delete key
                cursor.deleteWholeLine()
            elif char == KEY_DOWN: # CMD + DOWN
                cursor.moveToRightBottomMost()
            elif char == KEY_UP:  # CMD + UP
                cursor.moveToRightUpMost()
            else:  # in case char user press ESC
                ungetch(char)
        else:
            cursor._writeString(str(char))

    return cursor.getText()

def printQuitOptions(screen):
    height, width = screen.getmaxyx()
    screen.clear()
    y = int(height / 2.5)
    x = int(width / 2.5)
    screen.addstr(y, x, "Quit and Save (ENTER)")
    screen.addstr(y + 1, x, "Quit (F9)")
    screen.addstr(y + 2, x, "Go Back (Any Key)")
    screen.refresh()


class Cursor:

    def __init__(self, screen, text=""):
        self.text = text.split("\n")
        self.count = 0
        self.x = 0
        self.y = 0
        self.scroll_from_line = 0
        self.screen = screen

        height, width = screen.getmaxyx()
        self.screen_width = width - 1  # coordinate begin with 0, screen_width begin with 1
        self.screen_height = height - 1  # coordinate begin with 0, screen_height begin with 1
        self._updateScreen()

    def moveRight(self):
        self._updateXY()
        if self.x < len(self.text[self.y + self.scroll_from_line]):
            self._move(self.x + 1, self.y)

    def moveLeft(self):
        self._updateXY()
        if self.x > 0:
            self._move(self.x - 1, self.y)

    def moveDown(self, call_from="keyboard"):
        self._updateXY()
        if len(self.text) - 1 > self.scroll_from_line + self.screen_height and self.y == self.screen_height and call_from != "newline_function":
            self.scroll_from_line += 1

        self._updateScreen()

        if self.y < len(self.text) - 1 and self.y < self.screen_height:
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
        if self.screen_height < self.y + 1:
            self.scroll_from_line += 1

        if self.x >= len(self.text[self.y]):
            self.text.insert(self.y + self.scroll_from_line + 1, "")
        else:
            line = self.text[self.y]
            self.text[self.y] = line[:self.x]
            self.text.insert(self.y + self.scroll_from_line + 1, line[self.x:])

        self._updateScreen()
        self.moveDown("newline_function")
        self.moveToLeftMost()
        self._debug("self.y: {}, screen_height: {}, total_text_line: {}, line_writing_to: {}, scroll_from_line: {}, last_work: {}".format(self.y, self.screen_height, len(self.text), self.y + self.scroll_from_line - 1, self.scroll_from_line, self.text[-5:-1]))

    def writeChar(self, char):
        self._updateXY()
        if self.scroll_from_line == 0:
            self.text[self.y] = self._insert(char, self.text[self.y], self.x)
        elif self.scroll_from_line > 0 and self.y < self.screen_height:
            self.text[self.y + self.scroll_from_line] = self._insert(char, self.text[self.y + self.scroll_from_line], self.x)
        elif self.scroll_from_line > 0 and self.y == self.screen_height:
            self.text[self.y + self.scroll_from_line] += chr(char)
        self._updateScreen()
        self.moveRight()

        # self._debug("writeChar: self.y: {}, screen_height: {}, total_text_line: {}".format(self.y, self.screen_height, ))
        # self._debug("writeChar: {}".format(self.text))

    def tab(self):
        self.writeChar(32)
        self.writeChar(32)
        self.writeChar(32)

    def delete(self):
        self._updateXY()
        if len(self.text[self.y]) == 0 and self.y != 0:
            self.text.pop(self.y)
            self._updateScreen()
            self.moveUp()
            self.moveToRightMost()
        elif len(self.text[self.y]) > 0 and len(self.text[self.y]) == self.x:
            self.text[self.y] = self.text[self.y][:-1]
            self._updateScreen()
            self.moveLeft()
        elif self.x < len(self.text[self.y]) and self.x != 0:
            self.text[self.y] = self._removeChar(self.text[self.y], self.x - 1)
            self._updateScreen()
            self.moveLeft()
        elif self.x == 0 and self.y != 0:
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
        self._move(len(self.text[self.y + self.scroll_from_line]), self.y)
        self._debug("MoveToRightMost: ")


    #todo: refactor this shit
    def moveToRightBottomMost(self):
        self._updateXY()
        if (len(self.text) - 1 > self.screen_height):
            self.scroll_from_line = len(self.text) - 1 - self.screen_height
        self._updateScreen()
        if (len(self.text) - 1 <= self.screen_height):
            self._move(0, len(self.text) - 1)
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
        self.screen_height, self.screen_width = self.screen.getmaxyx()
        self._updateScreen()

    ### private function ###
    def _updateScreen(self):
        curs_set(0) # hide cursor, so user don't see it flash while updating screen

        # write ~ in the beginning of each row
        self.screen.clear()
        for y in range(len(self.text), self.screen_height):
            self.screen.addstr(y, 0, "~", color_pair(BORDER))

        # input text to it
        # if scroll_from_line()
        text_array = self.text[self.scroll_from_line: self.scroll_from_line + self.screen_height + 1]
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


if __name__== "__main__":
    if len(sys.argv) != 2:
        call(["echo", "no file path found"])
        sys.exit(99)

    exit_code = wrapper(main, sys.argv[1])

    if exit_code == -1:
        call(["echo", "Shit just happen, sorry."])
    elif exit_code == 0:
        call(["echo", "saved !"])
    elif exit_code == 1:
        call(["echo", "Quit, safe and sound."])


# todo
# scroll function when there are too much text

# make it run on mac terminal
# refactor