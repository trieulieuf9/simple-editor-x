from subprocess import call
from os import remove
from curses import *
import sys


def testRunner(test_func, inputs):
    # I just copy code from curses.wrapper(), then insert fakeKeyboardInput before running the app.
    caller_function_name = sys._getframe().f_back.f_code.co_name
    file_path = "src/test/result/" + caller_function_name
    _deleteFile(file_path)
    try:
        stdscr = initscr()
        noecho()
        cbreak()
        stdscr.keypad(1)
        try:
            start_color()
        except:
            pass
        _fakeKeyboardInput(inputs)
        test_func(stdscr, file_path)
    finally:
        # Set everything back to normal
        if 'stdscr' in locals():
            stdscr.keypad(0)
            echo()
            nocbreak()
            endwin()
    _checkAndPrintTestResult(caller_function_name)


def _fakeKeyboardInput(input):
    keyboard_dict = {'F1': 265, 'F9': 273, 'CMD': 27, "ESCAPE": 27, "ALT": 27, "LEFT": 260, "RIGHT": 261, "UP": 259, "DOWN": 258,
            "DELETE": 127, "ENTER": 10}
    for command in reversed(input):
        if command in keyboard_dict.keys():
            ungetch(keyboard_dict.get(command))
        else:
            for char in reversed(command):
                ungetch(char)

def _deleteFile(file_path):
    try:
        remove(file_path)
    except:
        pass

def _checkAndPrintTestResult(function_name):
    if _isTestPass(function_name):
        _printToTerminal("Passed {}".format(function_name), "GREEN")
    else:
        _printToTerminal("Failed {}".format(function_name), "RED")

def _isTestPass(file_name):
    try:
        expected = open("src/test/expected/" + file_name, "r").read()
        result = open("src/test/result/" + file_name, "r").read()
        return result == expected
    except:
        return False

def _printToTerminal(message, color="NONE"):
    color_dict = {"RED": "\033[31m", "GREEN": "\033[32m", "RESET": "\033[0m", "NONE": ""}
    color_message = color_dict[color] + message + color_dict["RESET"]
    call(["echo", color_message])