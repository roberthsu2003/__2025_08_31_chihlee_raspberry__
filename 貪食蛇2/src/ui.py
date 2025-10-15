# ui.py

import pygame
import sys
from settings import WHITE, BLACK, SCREEN_WIDTH, SCREEN_HEIGHT

def draw_text(screen, text, size, x, y, color=WHITE):
    """在指定位置繪製文字的輔助函式。"""
    text = str(text) # 確保傳入的是字串
    try:
        # 使用文泉驛正黑字型，它對中英文的支援都很好
        font = pygame.font.Font("src/wqy-zenhei.ttc", size)
    except FileNotFoundError:
        print(f"警告：找不到字型檔案 src/wqy-zenhei.ttc，請確認它位於 src/ 目錄下。")
        print("退回使用預設字型。")
        font = pygame.font.Font(None, size)

    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

def get_player_name(screen):
    """顯示一個畫面讓玩家輸入名稱，返回輸入的名稱。"""
    input_box = pygame.Rect(SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 - 20, 200, 40)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        if text.strip(): # 確保名稱不為空
                            done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill(BLACK)
        draw_text(screen, "請輸入您的名稱：", 32, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 80)
        
        # 繪製輸入框
        pygame.draw.rect(screen, color, input_box, 2)
        # 繪製輸入的文字
        draw_text(screen, text, 32, input_box.centerx, input_box.y + 5)

        pygame.display.flip()

    return text.strip()

def draw_main_menu(screen):
    """繪製主選單，等待玩家開始遊戲。如果玩家開始，返回 True。"""
    waiting = True
    while waiting:
        screen.fill(BLACK)
        draw_text(screen, "貪食蛇", 64, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
        draw_text(screen, "按 Enter 鍵開始遊戲", 22, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
                    return True
    return False

def draw_game_over_screen(screen, final_score):
    """顯示遊戲結束畫面，返回 True 表示重新開始，False 表示結束。"""
    waiting = True
    while waiting:
        screen.fill(BLACK)
        draw_text(screen, "遊戲結束", 64, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
        draw_text(screen, f"最終分數: {final_score}", 32, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        draw_text(screen, "按 R 重新開始，按 Q 離開", 22, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True  # 重新開始
                if event.key == pygame.K_q:
                    return False # 結束
