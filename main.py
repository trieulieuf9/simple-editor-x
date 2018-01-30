from curses import *
import sys
import os
from subprocess import call

# add the word custom, so we will mistaken them with variable inside Curses library
CUSTOM_KEY_ESCAPE = 27
CUSTOM_KEY_BACKSPACE = 127
CUSTOM_KEY_ENTER = 10
CUSTOM_KEY_TAB = 9
BORDER = 1

def main(screen):
    setUpEnv()
    # screen.keypad(0)
    height, width = screen.getmaxyx()
    file_path = sys.argv[1]

    text = readFileIfExist(file_path)
    while 1:
        try:
            text = startEditing(screen, width, height, text)
            printQuitOptions(screen, width, height)
            char = screen.getch()
            if char == CUSTOM_KEY_ENTER:
                with open(file_path, "w+") as file:
                    file.write(text)
                return 0
            elif char == KEY_F9:
                break
        except KeyboardInterrupt: # quit properly, when user press Ctrl + C
            return 1
        except:
            return -1

def setUpEnv():
    use_default_colors()
    init_pair(BORDER, COLOR_BLUE, -1)

def readFileIfExist(file_path):
    text = ""
    if os.path.isfile(file_path):
        with open(file_path, "r") as file:
            text = file.read()
    return text





def startEditing(screen, width, height, text):
    cursor = Cursor(screen, width, height, text)
    while 1:
        char = screen.getch()
        cursor._writeString(keyname(char))
        cursor._writeString(" ")
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
            else:  # in case char user press ESC
                ungetch(char)
        else:
            # cursor._writeString(str(char))
            cursor._writeString(keyname(char))

            # cursor._writeString(os.environ['TERM'])
    # return cursor.getText()
    return "hello"


def printQuitOptions(screen, width, height):
    screen.clear()
    y = int(height / 4)
    x = int(width / 4)
    screen.addstr(y, x, "Quit and Save (ENTER)")
    screen.addstr(y + 1, x, "Quit (F9)")
    screen.addstr(y + 2, x, "Go Back (Any Key)")
    screen.refresh()


class Cursor:

    def __init__(self, screen, screen_width, screen_height, text=""):
        self.text = text.split("\n")
        self.count = 0
        self.x = 0
        self.y = 0
        self.screen = screen
        self.screen_width = screen_width - 1  # coordinate begin with 0, screen_width begin with 1
        self.screen_height = screen_height - 1  # coordinate begin with 0, screen_height begin with 1
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
        if self.y < len(self.text) - 1:
            self._move(self.x, self.y + 1)
        elif self.y == len(self.text) - 1:
            self.moveToRightMost()

    def moveUp(self):
        self._updateXY()
        if self.y > 0:
            self._move(self.x, self.y - 1)

    def newLine(self):
        self._updateXY()
        if self.x >= len(self.text[self.y]):
            self.text.append("")
        else:
            line = self.text[self.y]
            self.text[self.y] = line[:self.x]
            self.text.insert(self.y + 1, line[self.x:])
        self._updateScreen()
        self.moveDown()
        self.moveToLeftMost()

    def writeChar(self, char):
        self._updateXY()
        if self.x >= len(self.text[self.y]): # cursor in the tail of text
            self.text[self.y] += chr(char)
        else: # cursor in middle of text
            self.text[self.y] = self._insert(char, self.text[self.y], self.x)
        self._updateScreen()
        self.moveRight()

    def tab(self):
        self.writeChar(32)
        self.writeChar(32)
        self.writeChar(32)

    def delete(self):
        self._updateXY()
        if len(self.text[self.y]) == 0 and self.y != 0:
            self.text.pop(self.y)
            self._updateScreen()
            # self.moveUp()
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
        self._move(len(self.text[self.y]), self.y)

    def getText(self):
        return "\n".join(self.text)

    ### private function ###
    def _updateScreen(self):
        # write ~ in the beginning of each row
        self.screen.clear()
        for y in range(len(self.text), self.screen_height - 1):
            self.screen.addstr(y, 0, "~", color_pair(BORDER))

        # input text to it
        text = "\n".join(self.text)
        self.screen.addstr(0, 0, text)
        self._move(self.x, self.y)
        self.screen.refresh()

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
    if len(sys.argv) != 2:
        call(["echo", "no file path found"])
        sys.exit(99)

    exit_code = wrapper(main)

    if exit_code == -1:
        call(["echo", "Shit just happen, sorry."])
    elif exit_code == 0:
        call(["echo", "saved !"])
    elif exit_code == 1:
        call(["echo", "Quit, safe and sound."])


# todo
# delete whole line of text with cmd + delete
# make it run on mac terminal
# responsive window, when terminal window resize, resize the text box as well
# scroll function when there are too much text
# refactor