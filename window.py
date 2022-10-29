import os
import win32con
from ctypes import windll, byref, c_ubyte
from ctypes.wintypes import RECT, HWND
import cv2
import numpy as np

from position import Position

WINDOW_NAME = "Guild Wars 2"

class Window:
    def __init__(self, name) -> None:
        self.hwnd: HWND = windll.user32.FindWindowW(None, name)
        windll.user32.SetProcessDPIAware()

    def get_rect(self):
        rect = RECT()
        windll.user32.GetWindowRect(self.hwnd, byref(rect))
        l, t, r, b = rect.left, rect.top, rect.right, rect.bottom

        return dict(
            left=rect.left, right=rect.right, top=rect.top, bottom=rect.bottom, 
        )

    def get_center_position(self) -> Position:
        rect = self.get_rect()
        center_x = rect['left'] + (rect['right'] - rect['left']) // 2
        center_y = rect['top'] + (rect['bottom'] - rect['top']) // 2
        return Position(center_x, center_y) 
        
    def get_window_size(self):
        rect = RECT()
        windll.user32.GetClientRect(self.hwnd, byref(rect))
        x, y, w, h = rect.left, rect.top, rect.right, rect.bottom

        return w, h

    def screenshot(self):
        w, h = self.get_window_size()

        dc = windll.user32.GetDC(self.hwnd)
        cdc = windll.gdi32.CreateCompatibleDC(dc)
        bitmap = windll.gdi32.CreateCompatibleBitmap(dc, w, h)
        windll.gdi32.SelectObject(cdc, bitmap)
        windll.gdi32.BitBlt(cdc, 0, 0, w, h, dc, 0, 0, win32con.SRCCOPY)

        total_bytes = w * h * 4
        buf = bytearray(total_bytes)
        byte_array = c_ubyte*total_bytes
        windll.gdi32.GetBitmapBits(bitmap, total_bytes, byte_array.from_buffer(buf))

        windll.gdi32.DeleteObject(bitmap)
        windll.gdi32.DeleteObject(cdc)
        windll.user32.ReleaseDC(self.hwnd, dc)

        img = np.frombuffer(buf, dtype=np.uint8).reshape(h, w, 4)
        return img
    
    def move(self, x: int, y: int) -> None:
        windll.user32.SetWindowPos(self.hwnd, 0, x, y, 0, 0, win32con.SWP_NOSIZE | win32con.SWP_NOZORDER)
    
    def resize(self, w: int, h: int) -> None:
        windll.user32.SetWindowPos(self.hwnd, 0, 0, 0, w, h, win32con.SWP_NOMOVE | win32con.SWP_NOZORDER)
    
    def resize_content(self, w: int, h: int) -> None:
        client_rect = RECT()
        windll.user32.GetClientRect(self.hwnd, byref(client_rect))

        dw = w - client_rect.right
        dh = h - client_rect.bottom

        window_rect = RECT()
        windll.user32.GetWindowRect(self.hwnd, byref(window_rect))

        cw = window_rect.right - window_rect.left
        ch = window_rect.bottom - window_rect.top

        self.resize(cw+dw, ch+dh)

    def lock(self):
        windll.user32.EnableWindow(self.hwnd, 0)
    def unlock(self):
        windll.user32.EnableWindow(self.hwnd, 1)

    def focus(self):
        windll.user32.SetForegroundWindow(self.hwnd)
        

if __name__ == "__main__":
    win = Window(WINDOW_NAME)
    win.resize_content(1280, 768)
    # win.unlock()
    img = win.screenshot()
    print('img', img)
    img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGBA2RGB)
    cv2.imshow("Capture Test", img)
    cv2.waitKey()
    dir = os.path.dirname(os.path.realpath(__file__))
    img_path = os.path.join(dir, 'test.png')
    cv2.imwrite(img_path, img)