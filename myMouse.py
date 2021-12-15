from time import sleep
import win32api
import win32con

def space():
    win32api.keybd_event(32, 0, 0, 0)
    win32api.keybd_event(32, 0, win32con.KEYEVENTF_KEYUP, 0)
    sleep(0.1)

def left_click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    win32api.SetCursorPos((1, 1))
    sleep(0.01)


def right_click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y, 0, 0)
    win32api.SetCursorPos((1, 1))
    sleep(0.01)


def double_click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y, 0, 0)
    win32api.SetCursorPos((1, 1))
    sleep(0.01)


def click(rect, block_row=0, block_col=0, type='left_click'):
    block_length = 24
    offset_x = 30
    offset_y = 165

    print(str(block_row),str(block_col),type)
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


if __name__ == '__main__':
    import UpdateFrame
    import time

    hwnd = UpdateFrame.get_screenshot()
    rect = UpdateFrame.get_position(hwnd)
    time.sleep(3)
    click(rect, 0, 0, 'left_click')
    time.sleep(1)
    click(rect, 15, 29, 'left_click')
    time.sleep(1)
    click(rect, 0, 0, 'restart')
