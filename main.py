# Import packages
import pygame
from constants import PLAYER_NAMES, WINDOW_SIZE
from board import Board


def main():
        board = Board()

        pygame.init()
        screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("Checkers")
        clock = pygame.time.Clock()

        game_over = False

        print(f"{PLAYER_NAMES[board.current_player]}'s Turn")

        while not game_over:
            for event in pygame.event.get():
                # check for player pressing 'q' to quit the game
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    game_over = True
                    print("Game quit by player pressing 'q'.")

                if event.type == pygame.QUIT:
                    game_over = True
                    print("Game quit by player closing the window.")

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    board.handle_mouse_down(pygame.mouse.get_pos())

                elif event.type == pygame.MOUSEBUTTONUP:
                    board.handle_mouse_up(pygame.mouse.get_pos())

            game_over = game_over or board.game_over

            board.draw(screen)
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    main()
