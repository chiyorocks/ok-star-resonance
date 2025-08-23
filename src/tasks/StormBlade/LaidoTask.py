from src.tasks.SRTriggerTask import SRTriggerTask
import re

class LaidoTask(SRTriggerTask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = '太刀自动化'
        self.description = '太刀自动卡刀宏'

    def run(self):
        if self._handle_blade_intention_detection():
            return

    def _handle_blade_intention_detection(self) -> bool:
        is_full_blade_intention = self.ocr(0.56, 0.75, 0.61, 0.79, match=re.compile('100.*100'))
        if is_full_blade_intention:
            return True
        else:
            return False

    def _handle_thunder_seal_detection(self) -> int:
        self.find_feature()