import re
import time

from src.tasks.SRTriggerTask import SRTriggerTask


class GatherTask(SRTriggerTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "自动采集"
        self.description = "当屏幕上出现采集按钮后进行采集，注意调整角度使采集文字清晰可见"
        self.trigger_count = 0

        self.settings = [
            {'key': 'use_stamina', 'label': '使用专注采集', 'default': False}
        ]

        self.default_config.update({
            setting['label']: setting['default'] for setting in self.settings
        })

        self._settings_map = {s['key']: s for s in self.settings}

        self.last_run_time = 0
        self.run_interval = 0

    def run(self):
        lang = self.get_game_language()

        if time.time() - self.last_run_time < self.run_interval:
            return

        self.run_interval = 0

        self.last_run_time = time.time()

        if lang == 'chinese':
            pattern1 = re.compile('采集')
            pattern2_str = '专注'
        else:
            pattern1 = re.compile('Focused|Normal')
            pattern2_str = 'Focused'

        boxes = self.ocr(0.75, 0.5, 0.84, 0.61, match=pattern1)

        if not boxes:
            self.run_interval = 1
            return

        sorted_boxes = sorted(boxes, key=lambda b: b.center()[1])

        for i, box in enumerate(sorted_boxes):
            self.sleep(0.5)
            if self.get_config_value('use_stamina') and re.search(pattern2_str, box.name):
                self.send_key('f')
                self.run_interval = 5.5
                break
            elif not self.get_config_value('use_stamina') and not re.search(pattern2_str, box.name):
                self.send_key('f')
                self.run_interval = 5.5
                break
            else:
                self.scroll(self.width_of_screen(0.5), self.height_of_screen(0.5), 120)
        return