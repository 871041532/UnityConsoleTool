#!/usr/bin/env python 
#encoding: utf-8
import ctypes
STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE= -11
STD_ERROR_HANDLE = -12
FOREGROUND_BLACK = 0x0
FOREGROUND_BLUE = 0x01 # text color contains blue.
FOREGROUND_GREEN= 0x02 # text color contains green.
FOREGROUND_RED = 0x04 # text color contains red.
FOREGROUND_YELLOW = 0x0e # yellow.
FOREGROUND_INTENSITY = 0x08 # text color is intensified.
BACKGROUND_BLUE = 0x10 # background color contains blue.
BACKGROUND_GREEN= 0x20 # background color contains green.
BACKGROUND_RED = 0x40 # background color contains red.
BACKGROUND_INTENSITY = 0x80 # background color is intensified.
class Color:
    ''' See http://msdn.microsoft.com/library/default.asp?url=/library/en-us/winprog/winprog/windows_api_reference.asp
    for information on Windows APIs. - www.jb51.net'''
    std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    def set_cmd_color(self, color, handle=std_out_handle):
        """(color) -> bit
        Example: set_cmd_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE | FOREGROUND_INTENSITY)
        """
        bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
        return bool

    def set_red(self):
        self.set_cmd_color(FOREGROUND_RED | FOREGROUND_INTENSITY)

    def set_yellow(self):
        self.set_cmd_color(FOREGROUND_YELLOW | FOREGROUND_INTENSITY)

    def set_white(self):
        self.reset_color()

    def print(self, strs):
        print (strs)

    def print_yellow(self, strs):
        self.set_cmd_color(FOREGROUND_YELLOW | FOREGROUND_INTENSITY)
        print (strs)
        self.reset_color()

    def print_red(self, print_text):
        self.set_cmd_color(FOREGROUND_RED | FOREGROUND_INTENSITY)
        print (print_text)
        self.reset_color()


    def reset_color(self):
        self.set_cmd_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)
    
    
    def print_green(self, print_text):
        self.set_cmd_color(FOREGROUND_GREEN | FOREGROUND_INTENSITY)
        print (print_text)
        self.reset_color()
   
    def print_blue_text(self, print_text):
        self.set_cmd_color(FOREGROUND_BLUE | FOREGROUND_INTENSITY)
        print (print_text)
        self.reset_color()
   
    def print_red_text_with_blue_bg(self, print_text):
        self.set_cmd_color(FOREGROUND_RED | FOREGROUND_INTENSITY| BACKGROUND_BLUE | BACKGROUND_INTENSITY)
        print (print_text)
        self.reset_color()   

if __name__ == "__main__":
    clr = Color()
    clr.print_red_text('red')
    clr.print_green_text('green')
    clr.print_blue_text('blue')
    clr.print_red_text_with_blue_bg('background')
    while True:
        pass