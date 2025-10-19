

import pygame
import sys
from settings import *
from game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("俄羅斯方塊")
    clock = pygame.time.Clock()
    game = Game()
    font = pygame.font.Font("assets/wqy-zenhei.ttc", 24)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if not game.game_over:
                    if event.key == pygame.K_LEFT:
                        game.block_x -= 1
                        if game.check_collision(game.current_block.shape, game.block_x, game.block_y):
                            game.block_x += 1
                    if event.key == pygame.K_RIGHT:
                        game.block_x += 1
                        if game.check_collision(game.current_block.shape, game.block_x, game.block_y):
                            game.block_x -= 1
                    if event.key == pygame.K_DOWN:
                        game.block_y += 1
                        if game.check_collision(game.current_block.shape, game.block_x, game.block_y):
                            game.block_y -= 1
                    if event.key == pygame.K_UP:
                        game.current_block.rotate()
                        if game.check_collision(game.current_block.shape, game.block_x, game.block_y):
                            game.current_block.un_rotate()


        screen.fill(BLACK)
        if not game.game_over:
            game.run(clock)
        else:
            game_over_text = font.render("遊戲結束", True, WHITE)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))

        score_text = font.render(f"分數: {game.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        game.draw_grid(screen)
        game.draw(screen)
        game.draw_next_block(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
