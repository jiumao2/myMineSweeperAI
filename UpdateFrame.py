from PyQt5.QtWidgets import QApplication
import win32gui
import cv2
import sys
import numpy as np
from PatternRecognizing import PatternRecognizing
import Decision
import myMouse
from pynput.mouse import Listener
import time

width_block = 30
height_block = 16
x_left = 12
x_right = 493
y_left = 55
y_right = 312


def get_screenshot(title='Minesweeper Arbiter '):
    hwnd = win32gui.FindWindow(None, title)
    if hwnd == 0:
        print('You have not opened Minesweeper Arbiter!')
    app = QApplication(sys.argv)
    screen = QApplication.primaryScreen()
    img = screen.grabWindow(hwnd).toImage()
    img.save("screenshot.jpg")
    return hwnd


def get_position(hwnd):
    rect = win32gui.GetWindowRect(hwnd)
    return rect


def process_screenshot():
    img = cv2.imread("screenshot.jpg")
    if img.sum(axis=(0, 1, 2)) == 0:
        print('Wrong window o r you are not playing mine sweeper now!')
        return False

    x = np.linspace(x_left, x_right, width_block + 1)
    y = np.linspace(y_left, y_right, height_block + 1)

    mine_fields = np.zeros((height_block, width_block))

    for k in range(len(x) - 1):
        for j in range(len(y) - 1):
            temp = img[round(y[j] - 1):round(y[j + 1]), round(x[k] - 1):round(x[k + 1]), :]
            mine_fields[j, k] = PatternRecognizing(temp)
    return mine_fields


toContinue = True


def on_click(x, y, button, pressed):
    if str(button) == 'Button.middle':
        global toContinue
        toContinue = False
        return False


if __name__ == '__main__':
    with Listener(on_click=on_click) as listener:
        while toContinue:
            hwnd = get_screenshot()
            rect = get_position(hwnd)
            mine_field = process_screenshot()
            res = Decision.next_move(mine_field, rect)
            if res == 0:
                # time.sleep(5)
                myMouse.click(rect, 0, 0, 'restart')
            elif res == 2:
                myMouse.space()
                # myMouse.left_click(rect[0]+470, rect[1]-60)
                myMouse.left_click(rect[0]+700, rect[1]-90)

        listener.join()
