from ok import TriggerTask

from pynput.mouse import Button, Controller
mouse = Controller()


class SRTriggerTask(TriggerTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_mouse_down = False

    def my_mouse_down(self):
        if self.is_mouse_down:
            return
        self.is_mouse_down = True
        mouse.press(Button.left)

    def my_mouse_up(self):
        if not self.is_mouse_down:
            return
        self.is_mouse_down = False
        mouse.release(Button.left)

    def my_mouse_switch(self):
        if self.is_mouse_down:
            self.my_mouse_up()
        else:
            self.my_mouse_down()

