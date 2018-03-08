from subprocess import call
import os

def printToTerminal(message, color="NONE"):
    color_dict = {"RED": "\033[31m", "GREEN": "\033[32m", "RESET": "\033[0m", "NONE": ""}
    color_message = color_dict[color] + message + color_dict["RESET"]
    call(["echo", color_message])

def writeToFile(file_path, text):
    with open(file_path, "w+") as file:
        file.write(text)

def readFileIfExist(file_path):
    text = ""
    if os.path.isfile(file_path):
        with open(file_path, "r") as file:
            text = file.read()
    return text