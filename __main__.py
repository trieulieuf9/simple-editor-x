import sys
import os
import traceback
from src.properties import *
from src.utils import *
from subprocess import call
from src.entity.cursor import Cursor
from curses import *


def main(screen, file_path):
    setUpEnv()
    text = readFileIfExist(file_path)
    while 1:
        try:
            text = startEditing(screen, text)
            printQuitOptions(screen)
            char = screen.getch()
            if char == KEY_ENTER_CODE:
                writeToFile(file_path, text)
                return 3, None
            elif char == KEY_F9:
                return 2, None
            else:
                pass
        except KeyboardInterrupt: # quit properly, when user press Ctrl + C
            return 1, None
        except:
            error_msg = traceback.format_exc()
            return -1, error_msg


def setUpEnv():
    use_default_colors()
    init_pair(BORDER_COLOR, COLOR_MAGENTA, -1)


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


def printExitMessage(exit_code, error_msg):
    if exit_code == -1:
        printToTerminal("Shit just happen, sorry.")
        if error_msg:
            printToTerminal(error_msg)
    elif exit_code == 1:
        printToTerminal("Quit, safe and sound.")
    elif exit_code == 2:
        printToTerminal("Quit without save.")
    elif exit_code == 3:
        printToTerminal("saved !")
    elif exit_code == 4: # -version
        printToTerminal(VERSION)
    elif exit_code == 5: # -help
        printToTerminal("======================== Welcome to Simple Editor X ========================", "GREEN")
        printToTerminal("")
        printToTerminal("Arguments:")
        printToTerminal("   -version")
        printToTerminal("   -help")
        printToTerminal("   {file_name}, to start editing an existing or create a new file")
        printToTerminal("")
        printToTerminal("While using:")
        printToTerminal("   Press F1, then ENTER to save")
        printToTerminal("")


if __name__== "__main__":
    if len(sys.argv) != 2:
        printToTerminal("This application take exactly 1 argument")
    error_msg = ""
    exit_code = -1
    arg = sys.argv[1].lower()
    file_path = sys.argv[1]
    if arg == "-v" or arg == "-version":
        exit_code = 4
    elif arg == "-h" or arg == "-help":
        exit_code = 5
    else:
        exit_code, error_msg = wrapper(main, file_path)

    printExitMessage(exit_code, error_msg)
