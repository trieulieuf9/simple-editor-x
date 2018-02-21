from ..python.__main__ import *
from .utils.utils import *


def test1():
    keyboardInput = ["trieulieuf9", "ENTER", "is the best", "F1", "ENTER"]
    function_name = sys._getframe().f_code.co_name
    deleteFile("src/test/result/" + function_name)

    testRunner(main, keyboardInput, "src/test/result/" + function_name)
    checkAndPrintTestResult(function_name)



if __name__== "__main__":
    test1()


# todo:
# modify wrapper, run test from here
# make it output files, then check contain of files with existing files
# can be check with diff !!