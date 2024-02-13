import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED
from checkers.board import Board
from checkers.game import Game
pygame.font.init()

FPS = 60

FONT = pygame.font.SysFont("arial", 36)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

def get_rol_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def draw_text(color):
    text = FONT.render(f"{color} player wins!", 1, "white")
    WIN.blit(text, (50, 50))

    pygame.display.update()


def main():
    running = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while running:
        clock.tick(FPS)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_rol_col_from_mouse(pos)
                game.select(row, col)

        if game.winner() != None:
            if game.winner() == RED:
                draw_text("Red")
            else:
                draw_text("White")
            pygame.time.delay(5000)
            running = False
                
        game.update()

    pygame.quit()

main()