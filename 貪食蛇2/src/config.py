import os
import pygame

# 遊戲視窗設定
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "貪食蛇"

# 顏色定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 蛇的設定
SNAKE_SIZE = 20
INITIAL_SNAKE_LENGTH = 3
INITIAL_SNAKE_SPEED = 10  # 初始速度，每秒移動的方塊數

# 食物的設定
FOOD_SIZE = 20

# 遊戲設定
FPS = 15  # 遊戲幀率
LEVEL_UP_SCORE = 10 # 每得到 10 分，等級提升一級
SPEED_INCREASE_PER_LEVEL = 1 # 每級加快 1 單位速度

# 字體設定
_current_dir = os.path.dirname(__file__)
FONT_PATH = os.path.join(_current_dir, "assets", "fonts", "Noto_Sans_TC", "static", "NotoSansTC-Regular.ttf")
FONT_SIZE_SMALL = 24
FONT_SIZE_MEDIUM = 36
FONT_SIZE_LARGE = 48