from time import sleep
import win32api
import win32con
import win32gui
import win32print
import hyperparams as p

wide_real = win32print.GetDeviceCaps(win32gui.GetDC(0), win32con.DESKTOPHORZRES)
wide_screen = win32api.GetSystemMetrics(0)
proportion = wide_real/wide_screen

block_length = round(16*proportion)
offset_x = round(20*proportion)
offset_y = round(110*proportion)

def space():
    win32api.keybd_event(32, 0, 0, 0)
    win32api.keybd_event(32, 0, win32con.KEYEVENTF_KEYUP, 0)
    
    
def reset():
    if p.mode == 'Beginner':
        win32api.keybd_event(49, 0, 0, 0)
        win32api.keybd_event(49, 0, win32con.KEYEVENTF_KEYUP, 0)
    elif p.mode == 'Intermediate':
        win32api.keybd_event(50, 0, 0, 0)
        win32api.keybd_event(50, 0, win32con.KEYEVENTF_KEYUP, 0)
    elif p.mode == 'Expert':
        win32api.keybd_event(51, 0, 0, 0)
        win32api.keybd_event(51, 0, win32con.KEYEVENTF_KEYUP, 0)

def left_click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    win32api.SetCursorPos((1, 1))
    sleep(p.delay_click)


def right_click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y, 0, 0)
    win32api.SetCursorPos((1, 1))
    sleep(p.delay_click)


def double_click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y, 0, 0)
    win32api.SetCursorPos((1, 1))
    sleep(p.delay_click)


def click(rect, block_row=0, block_col=0, type='left_click'):
    if type == 'restart':
        left_click(rect[0] + 250, rect[1] + 110)
    elif type == 'left_click':
        left_click(rect[0] + offset_x + block_length * block_col, rect[1] + offset_y + block_length * block_row)
    elif type == 'right_click':
        right_click(rect[0] + offset_x + block_length * block_col, rect[1] + offset_y + block_length * block_row)
    elif type == 'double_click':
        double_click(rect[0] + offset_x + block_length * block_col, rect[1] + offset_y + block_length * block_row)
    else:
        print('Wrong type!')
