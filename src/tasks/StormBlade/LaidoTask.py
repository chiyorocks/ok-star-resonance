import numpy as np

from src.tasks.SRTriggerTask import SRTriggerTask
import re

class LaidoTask(SRTriggerTask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = '太刀自动化'
        self.description = '太刀自动卡刀宏'

    def run(self):
        # if self._handle_blade_intention_detection():
        #     return
        if self._handle_thunder_seal_detection() > 0:
            return

    def _handle_blade_intention_detection(self) -> bool:
        is_full_blade_intention = self.ocr(0.56, 0.75, 0.61, 0.79, match=re.compile('100.*100'))
        if is_full_blade_intention:
            return True
        else:
            return False

    def _handle_thunder_seal_detection(self) -> int:
        y, x, d = self.frame.shape
        target_x3 = int(x * 0.592) + 1
        target_y3 = int(y * 0.812) + 1
        color3 = self.frame[target_y3, target_x3]
        if not (color3 < 110).all():
            target_x6 = int(x * 0.620) + 1
            target_y6 = int(y * 0.812) + 1
            color6 = self.frame[target_y6, target_x6]
            if not (color6 < 110).all():
                return 6
            else:
                return 3
        else:
            return 0

