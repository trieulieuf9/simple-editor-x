from curses import *
import curses.textpad
from subprocess import call


# add the word custom, so we will mistaken them with variable inside Curses library
CUSTOM_KEY_ESCAPE = 27
CUSTOM_KEY_BACKSPACE = 127
CUSTOM_KEY_ENTER = 10

def main(screen):
    # setting up the screen
    use_default_colors()

    # get screen sizes
    # width = call(["tput", "cols"])
    # height1 = call(["tput", "lines"])
    width = 262
    height = 17

    # create border
    init_pair(99, COLOR_BLUE, -1)
    for y in range(height - 1):
        screen.addstr(y, 0, "~", color_pair(99))
        screen.refresh()
    screen._move(0, 0)

    # begin your code here
    cursor = Cursor(screen, width, height)

    count = 0
    while 1:
        char = screen.getch()
        if char == KEY_F1 or char == CUSTOM_KEY_ESCAPE:
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
        else:
            cursor.writeString(str(char))

    endwin()


class Cursor:

    def __init__(self, screen, screen_width, screen_height):
        self.count = 0
        self.x = 0
        self.y = 0
        self.depth = 0
        self.screen = screen
        self.screen_width = screen_width - 1  # coordinate begin with 0
        self.screen_height = screen_height - 1  # coordinate begin with 0

    def moveRight(self):
        self.updateXY()
        if self.x < self.screen_width:
            self.moveAndRefresh(self.x + 1, self.y)

    def moveLeft(self):
        self.updateXY()
        if self.x > 0:
            self.moveAndRefresh(self.x - 1, self.y)

    def moveDown(self):
        self.updateXY()
        if self.y < self.depth:
            self.moveAndRefresh(self.x, self.y + 1)

    def moveUp(self):
        self.updateXY()
        if self.y > 0:
            self.moveAndRefresh(self.x, self.y - 1)

    def newLine(self):
        # when press enter, getch return 2 input char at the same time, but we want to execute it only one time
        # count is a catch for this problem
        self.count += 1
        if self.count == 2:
            self.depth += 1
            self.moveDown()
            self.moveToLeftMost()
            self.count = 0

    def writeChar(self, char):
        self.screen.addch(char)

    def delete(self):
        self.updateXY()
        if self.x == 0:
            self.depth -= 1
            self.moveUp()
            # to rightmost of text
        else:
            self.moveLeft()
            self.screen.delch()
            self.screen.refresh()


    ### private function ###
    def moveAndRefresh(self, x, y):
        self.screen._move(y, x)
        self.screen.refresh()

    def moveToLeftMost(self):
        self.updateXY()
        self.moveAndRefresh(0, self.y)
        pass

    def writeString(self, str):
        self.screen.addstr(str)
        self.moveRight()

    def updateXY(self):
        self.y, self.x = self.screen.getyx()

    # def moveRight(self):
    #     if self.x < self.screen_width:
    #         self.x += 1
    #         self.moveAndRefresh()
    #
    # def moveLeft(self):
    #     if self.x > 0:
    #         self.x -= 1
    #         self.moveAndRefresh()
    #
    # def moveDown(self):
    #     if self.y < self.depth:
    #         self.y += 1
    #         self.moveAndRefresh()
    #
    # def newLine(self):
    #     self.depth += 1
    #     self.moveDown()
    #     self.moveToLeftMost()
    #
    # def writeChar(self, char):
    #     self.screen.addch(char)
    #     self.moveRight()
    #
    # def delete(self):
    #     self.moveLeft()
    #     self.screen.delch()
    #     self.screen.refresh()
    #
    # ### private function ###
    # def moveAndRefresh(self):
    #     self.screen.move(self.y, self.x)
    #     self.screen.refresh()
    #
    # def moveToLeftMost(self):
    #     self.x = 0
    #     self.moveAndRefresh()
    #
    # def writeString(self, str):
    #     self.screen.addstr(str)
    #     self.moveRight()
    #
    # def updateXY(self):
    #     self.y, self.x = self.screen.getyx()



# todo:
# make a border for the screen DONE
# make cursor running around, and restrict the cursor to running out of this border DONE
# add text and manipulate text inside that screen
# extract text from it
# save
# quit
# profit



def addTextPadWindow(screen):
    screen.refresh()
    screen.keypad(1)  # enable keypad mode
    curses.noecho() # don't echo key strokes on the screen
    curses.cbreak() # read keystrokes instantly, without waiting for enter to ne pressed
    curses.flash()



    window = curses.newwin(10, 40, 3, 20) # height, width, begin_y, begin_x
    # window.border()

    window1 = curses.newwin(12, 42, 2, 19)  # height, width, begin_y, begin_x
    window1.border()
    text_box = curses.textpad.Textbox(window, insert_mode=True)
    text = text_box.edit()

    # screen.getch()
    # window.refresh()
    # window.getch()


# def terminate(key):
#     # printTerminalCommand(key)
#     if key == 265: # F1
#         return 7 # 7 is ctrl + G, default terminate command for keypad textbox we are using
#     elif key == 127: # delete
#         return 8 # special code to delete characters
#     return key


# def printTerminalCommand(key):
#     # if key == curses.ascii.DC3:
#     if key == 0x13:
#         call(["echo", "yeahhhhh"])
#     if key == None:
#         call(["echo", "null"])
#     else:
#         call(["echo", str(key)])


if __name__== "__main__":
    wrapper(main)