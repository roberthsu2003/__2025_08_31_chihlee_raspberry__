# main.py

import pygame
import sys
from settings import *
from ui import draw_main_menu, get_player_name, draw_game_over_screen
from game import Game
from player import ScoreManager

class App:
    """遊戲主應用程式類別，負責管理遊戲狀態和主迴圈。"""
    def __init__(self):
        """初始化應用程式，設定 Pygame、音效、畫面、時鐘和初始狀態。"""
        pygame.init()
        pygame.mixer.init() # 初始化音效混合器
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("繁體中文貪食蛇")
        self.clock = pygame.time.Clock()
        self.state = "MAIN_MENU"
        self.player_name = ""
        self.high_score = 0
        self.score_manager = ScoreManager("src/assets/scores.json")
        self.current_score = 0

        if SOUND_ENABLED:
            # 載入並播放背景音樂 - 注意：請將 'background.mp3' 替換為您自己的音樂檔案
            try:
                pygame.mixer.music.load("src/assets/background.mp3")
                pygame.mixer.music.play(-1)  # -1 表示無限循環
            except pygame.error as e:
                print(f"無法載入背景音樂：{e}")

    def run(self):
        """根據當前狀態執行對應的狀態處理函式，形成狀態機。"""
        while True:
            if self.state == "MAIN_MENU":
                self.main_menu_state()
            elif self.state == "GET_PLAYER_NAME":
                self.get_player_name_state()
            elif self.state == "PLAYING":
                self.playing_state()
            elif self.state == "GAME_OVER":
                self.game_over_state()

    def main_menu_state(self):
        """處理主選單狀態，等待玩家開始遊戲。"""
        if draw_main_menu(self.screen):
            self.state = "GET_PLAYER_NAME"

    def get_player_name_state(self):
        """處理玩家名稱輸入狀態。"""
        self.player_name = get_player_name(self.screen)
        # 這裡可以加入檢查玩家名稱是否重複的邏輯
        self.high_score = self.score_manager.get_high_score(self.player_name)
        self.state = "PLAYING"

    def playing_state(self):
        """處理遊戲進行中狀態。"""
        game = Game(self.screen, self.player_name, self.high_score)
        self.current_score = game.run()
        self.score_manager.update_score(self.player_name, self.current_score)
        self.state = "GAME_OVER"

    def game_over_state(self):
        """處理遊戲結束狀態，等待玩家選擇重新開始或離開。"""
        if draw_game_over_screen(self.screen, self.current_score):
            self.state = "PLAYING" # 重新開始
        else:
            pygame.quit()
            sys.exit()

if __name__ == '__main__':
    app = App()
    app.run()
