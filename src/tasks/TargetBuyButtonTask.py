import re

from src.tasks.SRTriggerTask import SRTriggerTask

class TargetBuyButtonTask(SRTriggerTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "自动将鼠标指向交易行购买按钮"
        self.description = "运行后会自动关闭"
        self.trigger_count = 0

    def run(self):
        if box:=self.ocr(0.92, 0.90, 0.96, 0.94, match='购买'):
            target = box[0].center()
            self.move(target[0], target[1])
            self.disable()
        return