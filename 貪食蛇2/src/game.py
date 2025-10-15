# game.py

import pygame
import random
import sys
from settings import *
from ui import draw_text

class Snake:
    """代表蛇的類別，處理蛇的移動、成長和方向改變。"""
    def __init__(self):
        """初始化蛇的身體、初始位置和方向。"""
        self.body = [(100, 100), (90, 100), (80, 100)]
        self.direction = "RIGHT"

    def move(self):
        """根據目前方向移動蛇的身體。"""
        head = self.body[0]
        x, y = head

        if self.direction == "UP":
            y -= 10
        elif self.direction == "DOWN":
            y += 10
        elif self.direction == "LEFT":
            x -= 10
        elif self.direction == "RIGHT":
            x += 10

        new_head = (x, y)
        self.body.insert(0, new_head)
        self.body.pop() # 移除最後一節，模擬移動

    def grow(self):
        """讓蛇的身體增長一節。"""
        self.body.append(self.body[-1])

    def change_direction(self, new_direction):
        """改變蛇的前進方向，但防止 180 度迴轉。"""
        if new_direction == "UP" and self.direction != "DOWN":
            self.direction = new_direction
        if new_direction == "DOWN" and self.direction != "UP":
            self.direction = new_direction
        if new_direction == "LEFT" and self.direction != "RIGHT":
            self.direction = new_direction
        if new_direction == "RIGHT" and self.direction != "LEFT":
            self.direction = new_direction

class Food:
    """代表食物的類別，處理食物的位置。"""
    def __init__(self):
        """初始化食物並隨機設定其位置。"""
        self.position = (0, 0)
        self.randomize_position()

    def randomize_position(self):
        """在螢幕範圍內隨機產生一個新的食物位置。"""
        x = random.randrange(0, SCREEN_WIDTH - 10, 10)
        y = random.randrange(0, SCREEN_HEIGHT - 10, 10)
        self.position = (x, y)

class Game:
    """代表一局遊戲的類別，管理遊戲的所有核心邏輯。"""
    def __init__(self, screen, player_name, high_score):
        """初始化一局新遊戲。"""
        self.screen = screen
        self.player_name = player_name
        self.high_score = high_score
        self.current_score = 0
        self.snake = Snake()
        self.food = Food()
        self.running = True
        self.clock = pygame.time.Clock()
        self.new_high_score_achieved = False

        self.eat_sound = None
        self.game_over_sound = None
        if SOUND_ENABLED:
            # 載入音效 - 注意：請將 'eat.wav' 和 'game_over.wav' 替換為您自己的音效檔案
            try:
                self.eat_sound = pygame.mixer.Sound("src/assets/eat.wav")
                self.game_over_sound = pygame.mixer.Sound("src/assets/game_over.wav")
            except pygame.error as e:
                print(f"無法載入音效檔案：{e}")

    def run(self):
        """管理「遊戲中」狀態的主迴圈，直到遊戲結束。"""
        while self.running:
            self._handle_input()
            self._update_logic()
            self._draw_elements()
            pygame.display.flip()
            self.clock.tick(15) # 遊戲速度
        return self.current_score

    def _handle_input(self):
        """處理遊戲中的玩家輸入（控制蛇的方向）。"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.change_direction("UP")
                elif event.key == pygame.K_DOWN:
                    self.snake.change_direction("DOWN")
                elif event.key == pygame.K_LEFT:
                    self.snake.change_direction("LEFT")
                elif event.key == pygame.K_RIGHT:
                    self.snake.change_direction("RIGHT")

    def _update_logic(self):
        """更新遊戲世界的狀態，包含移動、吃食物和碰撞偵測。"""
        self.snake.move()

        # 判斷是否吃到食物
        if self.snake.body[0] == self.food.position:
            self.snake.grow()
            self.food.randomize_position()
            self.current_score += 10
            if SOUND_ENABLED and self.eat_sound:
                self.eat_sound.play()
            # 檢查是否打破最高分紀錄
            if self.current_score > self.high_score and not self.new_high_score_achieved:
                self.new_high_score_achieved = True

        # 判斷是否撞到邊界
        head = self.snake.body[0]
        if head[0] < 0 or head[0] >= SCREEN_WIDTH or head[1] < 0 or head[1] >= SCREEN_HEIGHT:
            if SOUND_ENABLED and self.game_over_sound:
                self.game_over_sound.play()
            self.running = False

        # 判斷是否撞到自己
        if head in self.snake.body[1:]:
            if SOUND_ENABLED and self.game_over_sound:
                self.game_over_sound.play()
            self.running = False

    def _draw_elements(self):
        """將所有遊戲元素（背景、蛇、食物、分數）繪製到螢幕上。"""
        self.screen.fill(BLACK)
        # 繪製蛇
        for segment in self.snake.body:
            pygame.draw.rect(self.screen, GREEN, (segment[0], segment[1], 10, 10))
        # 繪製食物
        pygame.draw.rect(self.screen, RED, (self.food.position[0], self.food.position[1], 10, 10))
        # 繪製分數
        draw_text(self.screen, f"玩家: {self.player_name}", 22, 100, 10)
        draw_text(self.screen, f"最高分: {self.high_score}", 22, SCREEN_WIDTH / 2, 10)
        draw_text(self.screen, f"分數: {self.current_score}", 22, SCREEN_WIDTH - 100, 10)

        if self.new_high_score_achieved:
            draw_text(self.screen, "新高分！", 36, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
