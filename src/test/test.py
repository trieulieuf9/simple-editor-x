from ..python.__main__ import *
from .utils.utils import *


def newLineTest():
    keyboardInput = ["trieulieuf9", "ENTER", "is the best", "F1", "ENTER"]
    function_name = sys._getframe().f_code.co_name
    deleteFile("src/test/result/" + function_name)

    testRunner(main, keyboardInput, "src/test/result/" + function_name)
    checkAndPrintTestResult(function_name)

def moveUpAndGoToRightMostTest():
    keyboardInput = ["random_text", "ENTER", "random_text1", "UP", "UP", " hello", "LEFT", "LEFT", "CMD", "RIGHT" , " world.", "F1", "ENTER"]
    function_name = sys._getframe().f_code.co_name
    deleteFile("src/test/result/" + function_name)

    testRunner(main, keyboardInput, "src/test/result/" + function_name)
    checkAndPrintTestResult(function_name)

def moveDownAndGoToLeftMostTest():
    keyboardInput = ["random_text", "ENTER", "random_text1", "DOWN", "DOWN", " world.", "CMD", "LEFT", "hello ", "F1", "ENTER"]
    function_name = sys._getframe().f_code.co_name
    deleteFile("src/test/result/" + function_name)

    testRunner(main, keyboardInput, "src/test/result/" + function_name)
    checkAndPrintTestResult(function_name)

def moveRightAndLeftTest():
    keyboardInput = ["random", "LEFT", "LEFT", "LEFT", "_", "RIGHT", "RIGHT", "RIGHT", "_text", "F1", "ENTER"]
    function_name = sys._getframe().f_code.co_name
    deleteFile("src/test/result/" + function_name)

    testRunner(main, keyboardInput, "src/test/result/" + function_name)
    checkAndPrintTestResult(function_name)

def deleteAtRightMostAndMiddleTest():
    keyboardInput = ["ran__dom__", "DELETE", "DELETE", "LEFT", "LEFT", "LEFT", "DELETE", "DELETE", "F1", "ENTER"]
    function_name = sys._getframe().f_code.co_name
    deleteFile("src/test/result/" + function_name)

    testRunner(main, keyboardInput, "src/test/result/" + function_name)
    checkAndPrintTestResult(function_name)

def deleteAtBeginningOfLineTest():
    keyboardInput = ["hello ", "ENTER", "world.", "CMD", "LEFT", "DELETE", "F1", "ENTER"]
    function_name = sys._getframe().f_code.co_name
    deleteFile("src/test/result/" + function_name)

    testRunner(main, keyboardInput, "src/test/result/" + function_name)
    checkAndPrintTestResult(function_name)

def deleteAtBeginningOfFirstLine():
    keyboardInput = ["I'm getting bored of saying hello world now.", "CMD", "LEFT", "DELETE", "F1", "ENTER"]
    function_name = sys._getframe().f_code.co_name
    deleteFile("src/test/result/" + function_name)

    testRunner(main, keyboardInput, "src/test/result/" + function_name)
    checkAndPrintTestResult(function_name)

def moveToRightUpMost():
    keyboardInput = ["hello", "ENTER", "line 2", "LEFT", "LEFT", "LEFT", "CMD", "UP", " world.", "F1", "ENTER"]
    function_name = sys._getframe().f_code.co_name
    deleteFile("src/test/result/" + function_name)

    testRunner(main, keyboardInput, "src/test/result/" + function_name)
    checkAndPrintTestResult(function_name)

def moveToRightBottomMost():
    keyboardInput = ["line 1", "ENTER", "line 2", "ENTER", "line 3", "UP", "UP", "UP", "CMD", "DOWN", " line 3", "F1", "ENTER"]
    function_name = sys._getframe().f_code.co_name
    deleteFile("src/test/result/" + function_name)

    testRunner(main, keyboardInput, "src/test/result/" + function_name)
    checkAndPrintTestResult(function_name)

def deleteWholeLine(): # wait
    keyboardInput = ["hello dude !!!", "CMD", "DELETE", "hello", "F1", "ENTER"]
    function_name = sys._getframe().f_code.co_name
    deleteFile("src/test/result/" + function_name)

    testRunner(main, keyboardInput, "src/test/result/" + function_name)
    checkAndPrintTestResult(function_name)


if __name__== "__main__":
    newLineTest()
    moveUpAndGoToRightMostTest()
    moveDownAndGoToLeftMostTest()
    moveRightAndLeftTest()
    deleteAtRightMostAndMiddleTest()
    deleteAtBeginningOfLineTest()
    deleteAtBeginningOfFirstLine()
    moveToRightUpMost()
    moveToRightBottomMost()
    deleteWholeLine()