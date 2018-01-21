import pygame
import random
import sys
from pygame.locals import *
from itertools import product

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
RED = (234, 42, 42)
GREEN = (81, 255, 113)
BLUE = (42, 48, 234)
BLACK = (0, 0, 0)

# Screen size
SIZE = 600

# FPS
FPSclock = pygame.time.Clock()
FPS = 30

# Initialize surface
SURF = pygame.display.set_mode((SIZE, SIZE))

# Initialize fonts
main_font = pygame.font.SysFont('arial.tff', 50)
side_font = pygame.font.SysFont('arial.tff', 30)
game_font = pygame.font.SysFont('arial.tff', SIZE // 6)

def start_screen():
    """
    This is the screen that shows before starting the game.
    """

    Quit = False

    color1 = RED
    color2 = BLUE

    # Until the player presses any key...
    while not Quit:

        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                Quit = True

        SURF.fill(WHITE)

        color1, color2 = color2, color1

        name1Surface = main_font.render('TIC TAC TOE', True, color1)
        name1Rect = name1Surface.get_rect()
        name1Rect.center = (SIZE // 2 - 15, SIZE // 2 - 30)
        SURF.blit(name1Surface, name1Rect)

        name2Surface = main_font.render('TIC TAC TOE', True, color2)
        name2Rect = name2Surface.get_rect()
        name2Rect.center = (SIZE // 2 + 15, SIZE // 2)
        SURF.blit(name2Surface, name2Rect)

        keySurface = side_font.render('Click the mouse to start.', True, BLACK)
        keyRect = keySurface.get_rect()
        keyRect.center = (SIZE // 2, SIZE // 2 + 30)
        SURF.blit(keySurface, keyRect)

        pygame.time.delay(500)

        pygame.display.update()
        FPSclock.tick(FPS)

    # Clear screen
    SURF.fill(WHITE)
    pygame.display.update()


def main():
    """
    This is where the game happens.
    """

    # Initialize game surface
    GAME_x = SIZE // 5
    GAME_y = GAME_x
    GAME_size = SIZE // 5 * 3
    GAME = pygame.Surface((GAME_size, GAME_size))

    # Definition of Cell class and associated variables
    class Cell:

        def __init__(self, content, x, y, size):
            self.content = content
            self.x = x
            self.y = y
            self.size = size

    cell_size = GAME_size // 3
    cell_half = cell_size // 2
    middles = range(cell_half, GAME_size, cell_size)
    positions = product(middles, middles)

    def get_new_board():

        new_board = []

        for i, position in enumerate(positions):
            new_board.append(Cell('Empty{0}'.format(i), position[0], position[1], cell_size))

        return new_board

    def cell_at_mouse():

        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_x -= GAME_x
        mouse_y -= GAME_y

        for cell in board:
            if mouse_x in range(cell.x - cell_half, cell.x + cell_half + 1) and \
               mouse_y in range(cell.y - cell_half, cell.y + cell_half + 1) and \
               'Empty' in cell.content:
                    return cell

    def update_board_and_symbol():
        nonlocal symbol

        cell = cell_at_mouse()

        if cell:
            cell.content =  symbol
            symbol = symbols[(symbols.index(symbol) + 1) % 2]

    def highlight_cell():

        cell = cell_at_mouse()

        if cell:
            positionRect = pygame.Rect(0, 0, int(cell_size * 0.80), int(cell_size * 0.80))
            positionRect.center = (cell.x + 1, cell.y + 1)
            pygame.draw.rect(GAME, GREEN, positionRect, 5)

    def draw_cells():

        for cell in board:
            if cell.content == 'x':
                contentSurface = game_font.render('x', True, RED)
                contentRect = contentSurface.get_rect()
                contentRect.center = cell.x + 1, cell.y + 1
                GAME.blit(contentSurface, contentRect)
            elif cell.content == 'o':
                contentSurface = game_font.render('o', True, BLUE)
                contentRect = contentSurface.get_rect()
                contentRect.center = cell.x + 1, cell.y + 1
                GAME.blit(contentSurface, contentRect)

    def draw_grid():

        third = GAME_size // 3

        starts = (
        (third, 0),
        (third * 2, 0),
        (0, third),
        (0, third * 2))

        ends = (
        (third, third * 3),
        (third * 2, third * 3),
        (third * 3, third),
        (third * 3, third * 2))

        for i in range(len(starts)):
            start_x, start_y = starts[i][0], starts[i][1]
            end_x, end_y = ends[i][0], ends[i][1]
            pygame.draw.line(GAME, BLACK, (start_x, start_y), (end_x, end_y), grid_thickness)

    def check_for_winner():
        """
        Checks for a winner and returns the winning player's number or None.
        """

        winning_symbol = None

        winning_combinations = (
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6))

        start_cell = None
        end_cell = None

        for x, y, z in winning_combinations:
            if board[x].content == board[y].content == board[z].content:
                start_cell = board[x]
                end_cell = board[z]
                winning_symbol = board[x].content
                break

        if winning_symbol:

            while True:

                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        if event.key == K_y:
                            main()
                        elif event.key == K_n:
                            pygame.quit()
                            sys.exit()

                GAME.fill(WHITE)
                SURF.fill(WHITE)
                draw_grid()
                draw_cells()

                winnerSurface = main_font.render('{0} has won !'.format(winning_symbol.upper()), True, BLACK)
                winnerRect = winnerSurface.get_rect()
                winnerRect.center = SIZE // 2, GAME_y // 2
                SURF.blit(winnerSurface, winnerRect)

                againSurface = side_font.render('Play again ? (Y / N)', True, BLACK)
                againRect = againSurface.get_rect()
                againRect.center = SIZE // 2, SIZE - GAME_y // 2
                SURF.blit(againSurface, againRect)

                SURF.blit(GAME, (GAME_x, GAME_y))

                pygame.display.update()
                FPSclock.tick(FPS)

        else:
            return

    def check_for_full_board():
        """
        Checks to see if the board is full and ends the game if it is.
        """

        for cell in board:
            if 'Empty' in cell.content:
                return

        while True:

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_y:
                        main()
                    elif event.key == K_n:
                        pygame.quit()
                        sys.exit()

            GAME.fill(WHITE)
            SURF.fill(WHITE)
            draw_grid()
            draw_cells()

            winnerSurface = main_font.render("It's a tie !", True, BLACK)
            winnerRect = winnerSurface.get_rect()
            winnerRect.center = SIZE // 2, GAME_y // 2
            SURF.blit(winnerSurface, winnerRect)

            againSurface = side_font.render('Play again ? (Y / N)', True, BLACK)
            againRect = againSurface.get_rect()
            againRect.center = SIZE // 2, SIZE - GAME_y // 2
            SURF.blit(againSurface, againRect)

            SURF.blit(GAME, (GAME_x, GAME_y))

            pygame.display.update()
            FPSclock.tick(FPS)

        else:
            return

    def draw_mouse_as_symbol():
        """
        Blits the symbol of the current player at the mouse's current position.
        """

        mouse_x, mouse_y = pygame.mouse.get_pos()

        color = RED if symbol == 'x' else BLUE

        symbolSurface = main_font.render(symbol, True, color)
        symbolRect = symbolSurface.get_rect()
        symbolRect.center = (mouse_x, mouse_y)

        SURF.blit(symbolSurface, symbolRect)

    # Game start parameters
    symbols = ('x', 'o')
    symbol = random.choice(symbols)
    board = get_new_board()
    pygame.mouse.set_visible(False)
    grid_thickness = 10

    # Main game loop
    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                update_board_and_symbol()

        check_for_winner()
        check_for_full_board()

        GAME.fill(WHITE)
        SURF.fill(WHITE)

        draw_grid()
        highlight_cell()
        draw_cells()
        SURF.blit(GAME, (GAME_x, GAME_y))

        draw_mouse_as_symbol()

        pygame.display.update()
        FPSclock.tick(FPS)


if __name__ == '__main__':
    start_screen()
    main()
