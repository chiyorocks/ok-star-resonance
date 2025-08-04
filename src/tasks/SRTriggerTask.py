from ok import TriggerTask
import ctypes


class SRTriggerTask(TriggerTask):

    def click_foreground(self, rel_x, rel_y):
        self.mousedown_foreground(rel_x, rel_y)
        self.sleep(0.04)
        self.mouseup_foreground()

    def mousedown_foreground(self, rel_x, rel_y):
        hwnd = self.hwnd
        if(rel_x < 1 and rel_x > 0) and (rel_y < 1 and rel_y > 0):
            rel_x = int(hwnd.width * rel_x)
            rel_y = int(hwnd.height * rel_y)

        client_rect = (hwnd.x, hwnd.y, hwnd.x + hwnd.width, hwnd.y + hwnd.height)
        abs_x = client_rect[0] + rel_x
        abs_y = client_rect[1] + rel_y
        ctypes.windll.user32.SetCursorPos(abs_x, abs_y)
        ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)

    def mouseup_foreground(self):
        ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)



