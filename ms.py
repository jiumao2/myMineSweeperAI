from PyQt5.QtWidgets import QApplication
import win32gui
import numpy as np
import Decision
import myIO
from pynput.mouse import Listener
from time import sleep
import win32api
import win32con
import pymem
import sys
import os
import hyperparams

def get_screenshot(title='Minesweeper Arbiter '):
    hwnd = win32gui.FindWindow(None, title)
    if hwnd == 0:
        print('You have not opened Minesweeper Arbiter!')
    app = QApplication(sys.argv)
    return hwnd


def get_position(hwnd):
    rect = win32gui.GetWindowRect(hwnd)
    return rect

toContinue = True

def on_click(x, y, button, pressed):
    if str(button) == 'Button.middle':
        global toContinue
        toContinue = False
        return False

def get_mine_field(width=30,height=16):
    # 0: 空
    # -1: 未占据
    # 1-8:雷数
    # 9: 旗
    # 10: 雷
    # 11: 命中的雷
    # 12: 标错的雷
    a = np.zeros((height,width))
    p_x = 0
    p_y = 0
    for j in range(0,width):
        for k in range(0,int(height/4)):
            temp = "{:#010X}".format(Game.read_uint(Game.base_address+0x19EA184+4*k+30*j))
            for i in range(3,-1,-1):
                a[p_x, p_y] = int('0x'+temp[2+2*i:2+2*(i+1)],16)
                p_x += 1
                if p_x >= height:
                    p_x = 0
                    p_y += 1  
    
    a = np.floor(0.0001+(a-7)/10)
    a[a==9] = -1
    a[a==15] = 9
    return a  

if hyperparams.mode == 'Beginner':
    width = 8
    height = 8
elif hyperparams.mode == 'Intermediate':
    width = 16
    height = 16
if hyperparams.mode == 'Expert':
    width = 30
    height = 16

os.system('start MineSweeper/ms_arbiter.exe')
myIO.reset()
sleep(1)
Game = pymem.Pymem("ms_arbiter.exe")
with Listener(on_click=on_click) as listener:
    while toContinue:
        hwnd = get_screenshot()
        rect = get_position(hwnd)
        mine_field = get_mine_field(width,height)
        res = Decision.next_move(mine_field, rect)
        if res == 0:
            myIO.reset()
        elif res == 2:
            sleep(0.01)
            myIO.space()
            sleep(0.01)
            hwnd2 = win32gui.FindWindow(None, 'Local High Scores')
            if hwnd2:
                win32gui.PostMessage(hwnd2, win32con.WM_CLOSE, 0, 0)
            myIO.reset()

    listener.join()