import pygame
import sys
import random

# 初始化 Pygame
pygame.init()

# 遊戲視窗設定
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('貪食蛇')

# 顏色設定
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# 蛇的設定
SNAKE_BLOCK_SIZE = 20

# 遊戲時脈
clock = pygame.time.Clock()

def draw_snake(snake_body):
    """ 繪製蛇 """
    for block in snake_body:
        pygame.draw.rect(screen, GREEN, [block[0], block[1], SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE])

def main():
    """
    遊戲主迴圈
    """
    game_over = False

    # 蛇的初始位置與長度
    snake_body = [[100, 100], [80, 100], [60, 100]]
    # 蛇的初始方向
    direction = "RIGHT"
    change_to = direction

    # 食物的初始位置
    food_pos = [random.randrange(1, (SCREEN_WIDTH//SNAKE_BLOCK_SIZE)) * SNAKE_BLOCK_SIZE,
                random.randrange(1, (SCREEN_HEIGHT//SNAKE_BLOCK_SIZE)) * SNAKE_BLOCK_SIZE]

    # 分數
    score = 0
    font = pygame.font.SysFont('arial', 35)

    # 等級
    level = 1
    speed = 10

    while not game_over:
        # 事件處理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # 鍵盤事件
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = "UP"
                if event.key == pygame.K_DOWN:
                    change_to = "DOWN"
                if event.key == pygame.K_LEFT:
                    change_to = "LEFT"
                if event.key == pygame.K_RIGHT:
                    change_to = "RIGHT"

        # 防止蛇瞬間反向
        if change_to == "UP" and direction != "DOWN":
            direction = "UP"
        if change_to == "DOWN" and direction != "UP":
            direction = "DOWN"
        if change_to == "LEFT" and direction != "RIGHT":
            direction = "LEFT"
        if change_to == "RIGHT" and direction != "LEFT":
            direction = "RIGHT"

        # 移動蛇的身體
        if direction == "UP":
            snake_head = [snake_body[0][0], snake_body[0][1] - SNAKE_BLOCK_SIZE]
        if direction == "DOWN":
            snake_head = [snake_body[0][0], snake_body[0][1] + SNAKE_BLOCK_SIZE]
        if direction == "LEFT":
            snake_head = [snake_body[0][0] - SNAKE_BLOCK_SIZE, snake_body[0][1]]
        if direction == "RIGHT":
            snake_head = [snake_body[0][0] + SNAKE_BLOCK_SIZE, snake_body[0][1]]

        snake_body.insert(0, snake_head)

        # 判斷是否吃到食物
        if snake_head[0] == food_pos[0] and snake_head[1] == food_pos[1]:
            score += 10
            # 等級提升
            if score % 50 == 0:
                level += 1
                speed += 2 # 每50分速度加2
            food_pos = [random.randrange(1, (SCREEN_WIDTH//SNAKE_BLOCK_SIZE)) * SNAKE_BLOCK_SIZE,
                        random.randrange(1, (SCREEN_HEIGHT//SNAKE_BLOCK_SIZE)) * SNAKE_BLOCK_SIZE]
        else:
            snake_body.pop()

        # 畫面繪製
        screen.fill(BLACK) # 用黑色填滿背景
        draw_snake(snake_body)
        pygame.draw.rect(screen, RED, [food_pos[0], food_pos[1], SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE])

        # 顯示分數與等級
        score_text = font.render(f"Score: {score}  Level: {level}", True, WHITE)
        screen.blit(score_text, [10, 10])

        # 遊戲結束條件
        # 撞到牆
        if snake_head[0] < 0 or snake_head[0] > SCREEN_WIDTH - SNAKE_BLOCK_SIZE or snake_head[1] < 0 or snake_head[1] > SCREEN_HEIGHT - SNAKE_BLOCK_SIZE:
            game_over = True
        # 撞到自己
        for block in snake_body[1:]:
            if snake_head[0] == block[0] and snake_head[1] == block[1]:
                game_over = True

        # 更新顯示
        pygame.display.flip()

    # 控制遊戲更新速度
        clock.tick(speed)

    game_over_screen(score, level)


def game_over_screen(score, level):
    """ 遊戲結束畫面 """
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    main()

        # 畫面繪製
        screen.fill(BLACK)
        font = pygame.font.SysFont('arial', 50)
        game_over_text = font.render("Game Over", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH/2 - game_over_text.get_width()/2, SCREEN_HEIGHT/4))

        result_font = pygame.font.SysFont('arial', 35)
        score_text = result_font.render(f"Final Score: {score}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH/2 - score_text.get_width()/2, SCREEN_HEIGHT/2))
        level_text = result_font.render(f"Final Level: {level}", True, WHITE)
        screen.blit(level_text, (SCREEN_WIDTH/2 - level_text.get_width()/2, SCREEN_HEIGHT/2 + 50))

        instruction_font = pygame.font.SysFont('arial', 25)
        instruction_text = instruction_font.render("Press 'R' to Restart or 'Q' to Quit", True, WHITE)
        screen.blit(instruction_text, (SCREEN_WIDTH/2 - instruction_text.get_width()/2, SCREEN_HEIGHT*0.75))

        pygame.display.flip()
        clock.tick(15)


if __name__ == '__main__':
    main()
