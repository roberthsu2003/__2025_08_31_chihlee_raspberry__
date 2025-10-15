# -*- coding: utf-8 -*-
import pygame
import sys
import re
import logging
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, BLACK, FPS, SNAKE_SIZE, FONT_PATH, FONT_SIZE_MEDIUM, WHITE, LEVEL_UP_SCORE, SPEED_INCREASE_PER_LEVEL, INITIAL_SNAKE_SPEED
from src.snake import Snake
from src.food import Food
from src.game_state import GameState
from src import scores

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(SCREEN_TITLE)
        self.clock = pygame.time.Clock()
        
        # 安全地載入字體，如果自訂字體載入失敗則使用系統預設字體
        try:
            self.font = pygame.font.Font(FONT_PATH, FONT_SIZE_MEDIUM)
        except (pygame.error, FileNotFoundError, OSError):
            logging.warning(f"無法載入自訂字體 {FONT_PATH}，使用系統預設字體")
            self.font = pygame.font.Font(None, FONT_SIZE_MEDIUM)

        self.player_name = self._get_player_name()
        self._reset_game()
        self.high_score_beaten_message_display_time = 0
        self.show_high_scores = False
        self.paused = False

    def _get_player_name(self):
        # Check if player name is already saved
        all_scores = scores.load_scores()
        if all_scores:
            # Assuming the last played player's name is the one to use
            # For simplicity, let's just pick the first one if any exist
            # A more robust solution would involve a dedicated player profile system
            return list(all_scores.keys())[0]
        
        # If no scores or player name, prompt for input
        input_box = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 20, 200, 40)
        color_inactive = WHITE
        color_active = (200, 200, 200)
        color = color_inactive
        active = False
        text = ''
        error_message = ''
        done = False

        # 使用安全的字體載入機制
        try:
            default_font = pygame.font.Font(FONT_PATH, FONT_SIZE_MEDIUM)
        except (pygame.error, FileNotFoundError, OSError):
            default_font = pygame.font.Font(None, FONT_SIZE_MEDIUM)

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._quit_game()
                if event.type == pygame.K_RETURN:
                    if active:
                        if 1 <= len(text) <= 10 and re.match("^[a-zA-Z0-9_\u4e00-\u9fa5]+$", text): # Allow Chinese characters
                            done = True
                        else:
                            error_message = "姓名長度需在1-10字元之間，且不能包含特殊符號。"
                    else:
                        error_message = "請點擊輸入框輸入姓名。"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = not active
                        error_message = '' # Clear error when activating input
                    else:
                        active = False
                    color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            if 1 <= len(text) <= 10 and re.match("^[a-zA-Z0-9_\u4e00-\u9fa5]+$", text):
                                done = True
                            else:
                                error_message = "姓名長度需在1-10字元之間，且不能包含特殊符號。"
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                            error_message = '' # Clear error on backspace
                        else:
                            if len(text) < 10: # Limit input length
                                text += event.unicode
                                error_message = '' # Clear error on valid input
                            else:
                                error_message = "姓名長度不能超過10個字元。"

            self.screen.fill(BLACK)
            prompt_text = default_font.render("請輸入您的姓名: ", True, WHITE)
            self.screen.blit(prompt_text, (input_box.x - prompt_text.get_width() - 10, input_box.y + 5))

            txt_surface = default_font.render(text, True, color)
            width = max(200, txt_surface.get_width()+10)
            input_box.w = width
            self.screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
            pygame.draw.rect(self.screen, color, input_box, 2)

            if error_message:
                error_text = default_font.render(error_message, True, (255, 0, 0)) # Red color for error
                error_rect = error_text.get_rect(center=(SCREEN_WIDTH // 2, input_box.y + input_box.h + 20))
                self.screen.blit(error_text, error_rect)

            pygame.display.flip()
            self.clock.tick(FPS)
        return text

    def _reset_game(self):
        self.snake = Snake()
        self.food = Food()
        self.game_state = GameState(score=0, level=1, snake=self.snake, food=self.food, game_over=False,
                                    current_player_name=self.player_name,
                                    current_player_high_score=scores.get_player_high_score(self.player_name))
        self.current_speed = INITIAL_SNAKE_SPEED

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit_game()
            elif event.type == pygame.KEYDOWN:
                if self.game_state.game_over:
                    if event.key == pygame.K_r:  # 'R' key to restart
                        self._reset_game()
                    elif event.key == pygame.K_q:  # 'Q' key to quit
                        self._quit_game()
                    elif event.key == pygame.K_h: # 'H' key to show high scores
                        self.show_high_scores = not self.show_high_scores
                else:
                    if event.key == pygame.K_p: # 'P' key to pause/unpause
                        self.paused = not self.paused
                    # Handle direction changes only if not game over and not paused
                    elif not self.paused and (event.key == pygame.K_UP or \
                       event.key == pygame.K_DOWN or \
                       event.key == pygame.K_LEFT or \
                       event.key == pygame.K_RIGHT):
                        self.snake.change_direction(event.key)
            elif event.type == pygame.WINDOWFOCUSLOST:
                self.paused = True
            elif event.type == pygame.WINDOWFOCUSGAINED:
                self.paused = False

    def _update_game_state(self):
        if self.game_state.game_over or self.paused:
            return

        self.snake.move()

        # Check if snake eats food
        if self.snake.get_head_position() == self.food.get_position():
            self.snake.grow()
            self.food.spawn_food()
            self.game_state.score += 1

            # Check for level up
            if self.game_state.score % LEVEL_UP_SCORE == 0:
                self.game_state.level += 1
                self.current_speed += SPEED_INCREASE_PER_LEVEL

            # Check if current score beats personal high score
            if self.game_state.score > self.game_state.current_player_high_score:
                self.high_score_beaten_message_display_time = pygame.time.get_ticks() + 2000 # Display for 2 seconds

        # Check for collision
        if self.snake.check_collision():
            self.game_state.game_over = True
            scores.save_scores(self.game_state.current_player_name, self.game_state.score)

    def _draw_elements(self):
        self.screen.fill(BLACK)

        if self.show_high_scores:
            self._draw_high_scores()
        elif self.game_state.game_over:
            self._draw_game_over_screen()
        else:
            self.snake.draw(self.screen)
            self.food.draw(self.screen)

            # Display score and level
            score_text = self.font.render(f"分數: {self.game_state.score}", True, WHITE)
            level_text = self.font.render(f"等級: {self.game_state.level}", True, WHITE)
            self.screen.blit(score_text, (10, 10))
            self.screen.blit(level_text, (SCREEN_WIDTH - level_text.get_width() - 10, 10))

            # Display player name and high score
            player_info_text = self.font.render(f"玩家: {self.game_state.current_player_name} 最高分: {self.game_state.current_player_high_score}", True, WHITE)
            self.screen.blit(player_info_text, (10, 50))

            # Display high score beaten message
            if pygame.time.get_ticks() < self.high_score_beaten_message_display_time:
                high_score_msg = self.font.render("新紀錄!", True, WHITE)
                msg_rect = high_score_msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
                self.screen.blit(high_score_msg, msg_rect)
            
            if self.paused:
                paused_text = self.font.render("暫停", True, WHITE)
                paused_rect = paused_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                self.screen.blit(paused_text, paused_rect)

        pygame.display.flip()

    def _draw_game_over_screen(self):
        game_over_text = self.font.render("遊戲結束! 按 'R' 重新開始, 'Q' 離開, 'H' 高分榜", True, WHITE)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        self.screen.blit(game_over_text, text_rect)

    def _draw_high_scores(self):
        self.screen.fill(BLACK)
        title_text = self.font.render("高分榜", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title_text, title_rect)

        all_high_scores = scores.get_all_high_scores()
        y_offset = 100
        for i, (name, score) in enumerate(all_high_scores):
            score_entry = self.font.render(f"{i+1}. {name}: {score}", True, WHITE)
            score_rect = score_entry.get_rect(center=(SCREEN_WIDTH // 2, y_offset + i * 40))
            self.screen.blit(score_entry, score_rect)
        
        back_text = self.font.render("按 'H' 返回遊戲", True, WHITE)
        back_rect = back_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(back_text, back_rect)

    def _quit_game(self):
        pygame.quit()
        sys.exit()

    def run_game(self):
        while True:
            try:
                self._handle_input()
                self._update_game_state()
                self._draw_elements()
                self.clock.tick(self.current_speed)
            except Exception as e:
                logging.error(f"遊戲運行時發生錯誤: {e}")
                self._quit_game()