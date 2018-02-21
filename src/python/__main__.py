import sys
from curses import *
import os
from subprocess import call
# from entity.cursor import Cursor
from .entity.cursor import Cursor


# add the word custom, so we will mistaken them with variable inside Curses library
TERMINAL_RESIZE_CODE = 410
KEY_ESCAPE_CODE = 27 # could be escape or CMD or ALT
KEY_DELETE_CODE = 127
KEY_ENTER_CODE = 10
KEY_TAB_CODE = 9
BORDER_COLOR = 1


def main(screen, file_path):
    setUpEnv()
    text = readFileIfExist(file_path)
    while 1:
        try:
            text = startEditing(screen, text)
            printQuitOptions(screen)
            char = screen.getch()
            if char == KEY_ENTER_CODE:
                with open(file_path, "w+") as file:
                    file.write(text)
                return 0
            elif char == KEY_F9:
                return 2
            else:
                pass
        except KeyboardInterrupt: # quit properly, when user press Ctrl + C
            return 1
        except:  # put it back, when done with development
            return -1


def setUpEnv():
    use_default_colors()
    init_pair(BORDER_COLOR, COLOR_MAGENTA, -1)

def readFileIfExist(file_path):
    text = ""
    if os.path.isfile(file_path):
        with open(file_path, "r") as file:
            text = file.read()
    return text


def startEditing(screen, text):
    cursor = Cursor(screen, BORDER_COLOR, text)
    while 1:
        char = screen.getch()
        if char == KEY_F1:
            break
        elif char == TERMINAL_RESIZE_CODE:
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
        elif char == KEY_DELETE_CODE:
            cursor.delete()
        elif char == 10 or char == 13 or char == KEY_ENTER:
            cursor.newLine()
        elif char == KEY_TAB_CODE:
            cursor.tab()
        elif char == KEY_ESCAPE_CODE:
            char = screen.getch()  # get the key pressed after cmd or alt
            if char == KEY_LEFT or char == 98: # 98 and 102 are left and right keys produced while pressing alt, on mac terminal
                cursor.moveToLeftMost()
            elif char == KEY_RIGHT or char == 102: # CMD + RIGHT
                cursor.moveToRightMost()
            elif char == KEY_DELETE_CODE: # CMD + DELETE
                cursor.deleteWholeLine()
            elif char == KEY_DOWN: # CMD + DOWN
                cursor.moveToRightBottomMost()
            elif char == KEY_UP:  # CMD + UP
                cursor.moveToRightUpMost()
            else:  # in case char user press ESC, it produce the same effec as CMD or ALT, but that's not what we want
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


def printExitMessage(exit_code):
    if exit_code == -1:
        call(["echo", "Shit just happen, sorry."])
    elif exit_code == 0:
        call(["echo", "saved !"])
    elif exit_code == 1:
        call(["echo", "Quit, safe and sound."])
    elif exit_code == -2:
        call(["echo", "you have to provide fileName for either create or edit."])
    elif exit_code == -2:
        call(["echo", "Quit without save."])

if __name__== "__main__":
    exit_code = -2
    if len(sys.argv) == 2:
        exit_code = wrapper(main, sys.argv[1])

    printExitMessage(exit_code)


# todo
# refactor