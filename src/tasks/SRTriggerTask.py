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
        mouse.press(Button.left)
        self.is_mouse_down = True

    def my_mouse_up(self):
        if not self.is_mouse_down:
            return
        mouse.release(Button.left)
        self.is_mouse_down = False

    def my_mouse_switch(self):
        if self.is_mouse_down:
            self.my_mouse_up()
        else:
            self.my_mouse_down()

