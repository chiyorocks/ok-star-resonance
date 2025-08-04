import time

from src.tasks.SRTriggerTask import SRTriggerTask

class FishingTask(SRTriggerTask):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "自动钓鱼"
        self.description = "与钓鱼点交互后自动钓鱼"
        self.trigger_count = 0
        # "溜鱼"小游戏的状态变量
        self.pos = 0
        self.last_update_time = None
        self.key_a_pressed = False
        self.key_d_pressed = False
        
    def run(self):
        """
        钓鱼任务的主执行循环。
        根据当前的游戏状态调用对应的处理函数。
        """
        if self._handle_minigame():
            return
        if self._handle_start_and_rod_change():
            return
        if self._handle_hook_fish():
            return
        if self._handle_continue_fishing():
            return

    def _handle_start_and_rod_change(self) -> bool:
        """检查初始的钓鱼界面，以便抛竿或更换损坏的鱼竿。"""
        if self.ocr(0.56, 0.91, 0.60, 0.96, match='等级'):
            # 检查鱼竿是否损坏
            if self.ocr(0.90, 0.92, 0.96, 0.96, match='添加鱼竿'):
                self.log_info('更换鱼竿', notify=False)
                self.send_key('m')
                self.sleep(0.5)
                use_boxes = self.ocr(box=None, match="使用", log=False, threshold=0.8)
                if use_boxes:
                    self.log_info('点击使用鱼竿', notify=False)
                    center = use_boxes[0].center()
                    self.click_foreground(center[0] / self.width, center[1] / self.height)
                else:
                    self.log_info('没有鱼竿了', notify=True)
                    raise Exception("没有鱼竿了,需要实现买鱼竿")
            else:
                self.log_info('抛竿', notify=False)
                self.click_foreground(0.5, 0.5)
            return True
        return False

    def _handle_hook_fish(self) -> bool:
        """检查鱼上钩的提示，并点击开始收线。"""
        if self.find_one("hint_fishing_click", threshold=0.5):
            self.log_info('鱼上钩了', notify=False)
            self.click_foreground(0.5, 0.5)
            return True
        return False

    def _handle_continue_fishing(self) -> bool:
        """捕获鱼后，检查“继续钓鱼”按钮。"""
        if self.ocr(0.79, 0.88, 0.87, 0.93, match='继续钓鱼'):
            self.log_info('点击继续钓鱼', notify=False)
            self.click_foreground(0.82, 0.90)
            return True
        return False

    def _handle_minigame(self) -> bool:
        """管理收线和溜鱼"""
        # 如果“鱼线张力”文本可见，则需要收线。
        if self.ocr(0.54, 0.77, 0.62, 0.81, match='鱼线张力'):
            self.mousedown_foreground(0.5, 0.5)
            # 获取鱼的实际位置
            hook_box = self.find_one("box_hook", threshold=0.6)
            if hook_box:
                fish_pos_from_game = hook_box.center()[0] / self.width - 0.5
            self._play_the_fish(fish_pos_from_game)
            return True
        elif self.last_update_time:
            # 如果小游戏未激活，确保松开鼠标和按键。
            self.mouseup_foreground()
            self._reset_minigame_state()
        return False

    def _play_the_fish(self, fish_pos: float):
        """
        处理溜鱼。
        
        :param fish_pos: 鱼的当前位置，范围从 -0.9 到 0.9。
        """
        delta_time = self._update_time()
        
        normalized_fish_pos = min(max(fish_pos / 0.9, -1.0), 1.0)

        self._update_rod_position(delta_time)
        self._update_key_presses(normalized_fish_pos)

    def _update_time(self) -> float:
        """计算并返回自上次更新以来的时间差（delta_time）。"""
        current_time = time.time()
        if self.last_update_time is None:
            self.last_update_time = current_time
        delta_time = current_time - self.last_update_time
        self.last_update_time = current_time
        return delta_time

    def _update_key_presses(self, normalized_fish_pos: float):
        """根据鱼的位置决定按下或释放哪个按键。"""
        if normalized_fish_pos < self.pos:
            # 鱼在竿左边，竿在屏幕右边松开D键
            if self.pos > 0 and self.key_d_pressed:
                self.keyup('d'); self.key_d_pressed = False
            # 鱼在竿左边，竿在屏幕左边按下A键
            if self.pos <= 0 and self.key_d_pressed:
                self.keydown('a'); self.key_a_pressed = True
        else: 
            # 鱼在竿右边，竿在屏幕左边松开A键
            if self.pos < 0 and self.key_a_pressed:
                self.keyup('a'); self.key_a_pressed = False
            # 鱼在竿右边，竿在屏幕右边按下D键
            if self.pos >= 0 and self.key_a_pressed:
                self.keydown('d'); self.key_d_pressed = True

    def _update_rod_position(self, delta_time: float):
        """更新鱼竿的位置。"""
        # 未按任何键时，向中心点漂移
        if not self.key_a_pressed and not self.key_d_pressed:
            if self.pos > 0: self.pos -= 1.0 * delta_time
            elif self.pos < 0: self.pos += 1.0 * delta_time
        
        # 当按下 'A' 键且 pos < 0 时，向 -1 移动
        if self.key_a_pressed and self.pos < 0:
            self.pos -= 0.5 * delta_time
            
        # 当按下 'D' 键且 pos > 0 时，向 1 移动
        if self.key_d_pressed and self.pos > 0:
            self.pos += 0.5 * delta_time
            
        # 将位置限制在 [-1, 1] 的范围内
        self.pos = min(max(self.pos, -1.0), 1.0)
    
    def _reset_minigame_state(self):
        """在拉鱼结束时重置溜鱼状态。"""
        if self.key_a_pressed:
            self.keyup('a')
            self.key_a_pressed = False
        if self.key_d_pressed:
            self.keyup('d')
            self.key_d_pressed = False
        self.last_update_time = None