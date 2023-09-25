import itertools, random, pygame
from AI import *
pygame.init()

class Button(pygame.Rect):
    def __init__(self, text, color, width, height, bgcolor, center):
        super().__init__(0, 0, width, height)
        self.text = text
        self.center = center
        self.text = LARGE_FONT.render(text, True, color)
        self.bgcolor = bgcolor

    def draw(self):
        DIS.fill(self.bgcolor, self)
        pygame.draw.rect(DIS, 'black', self, width=1)
        DIS.blit(self.text, self.text.get_rect(center=self.center))


def draw_cell(action, color, sign):
    DRAWING_AREA.center = CELLS[action].center
    if sign == 'O':
        pygame.draw.ellipse(DIS, color, DRAWING_AREA, width=1)
    elif sign == 'X':
        pygame.draw.line(DIS, color, DRAWING_AREA.topleft, DRAWING_AREA.bottomright)
        pygame.draw.line(DIS, color, DRAWING_AREA.topright, DRAWING_AREA.bottomleft)


def initialization():

    global player1, player2, pool, current, other

    # Choose Symbol
    DIS.fill('grey')
    X_button.draw()
    O_button.draw()
    pygame.display.update()
    while True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN and X_button.collidepoint(event.pos):
            HUMAN_SIGN = 'X'
            AI_SIGN = 'O'
            break
        elif event.type == pygame.MOUSEBUTTONDOWN and O_button.collidepoint(event.pos):
            HUMAN_SIGN = 'O'
            AI_SIGN = 'X'
            break

    # Initialize Variables
    player1 = { 'id': 1, 
                'sign': AI_SIGN, 
                'type': 'AI', 
                'level': 'hard',
                'played': []        }
    player2 = { 'id': 2, 
                'sign': HUMAN_SIGN, 
                'type': 'human',
                'played': []        }
    current, other = random.sample([player1, player2], k=2)
    pool = list(itertools.product(range(3), repeat=2))

    # Draw initial Board
    DIS.fill('grey')
    DIS.fill('white', BOARD)
    for cell in CELLS.values():
        pygame.draw.rect(DIS, 'black', cell, width=1)
    pygame.display.update()



FONT = pygame.font.Font(None, 30)
LARGE_FONT = pygame.font.Font(None, 60)
def display_message(message, color):
    message_surface = FONT.render(message, True, color)
    message_rectangle = message_surface.get_rect()
    message_rectangle.center = DIS.get_rect().center
    DIS.blit(message_surface, message_rectangle)


# Dimensions
BLK = 10
CELL_WIDTH = 10 * BLK
BOARD_WIDTH = 3 * CELL_WIDTH
EXT_BD = 1 * BLK

# Setup of the display surface
DIS_WIDTH = BOARD_WIDTH + 2 * EXT_BD
DIS = pygame.display.set_mode((DIS_WIDTH, DIS_WIDTH))
pygame.display.set_caption('Mathieu\'s Tic-Tac-Toe')

# Setup of the game board and the 9 cells
BOARD = pygame.Rect(EXT_BD, EXT_BD, BOARD_WIDTH, BOARD_WIDTH)
CELLS = {}
for x,y in itertools.product(range(3), repeat=2):
    CELLS[x,y] = pygame.Rect(EXT_BD + x * CELL_WIDTH, EXT_BD + y * CELL_WIDTH, CELL_WIDTH, CELL_WIDTH)

# The drawing area will be moved around to draw the signs
INT_BD = 1 * BLK
DRAWING_AREA = pygame.Rect(0, 0, CELL_WIDTH - 2 * INT_BD, CELL_WIDTH - 2 * INT_BD)

# Setup of the 2 buttons
X_button = Button('X', 'black', 8*BLK, 8*BLK, 'white', pygame.Rect((0, 0, DIS_WIDTH//2, DIS_WIDTH)).center)
O_button = Button('O', 'black', 8*BLK, 8*BLK, 'white', pygame.Rect((DIS_WIDTH//2, 0, DIS_WIDTH//2, DIS_WIDTH)).center)

# Setup of the game clock and game speed
FPS = 10
clock = pygame.time.Clock()


initialization()

# Main game loop
while True:

    # Get new action, either from human player, or from AI program
    
    if current['type'] == 'human':
        # Event handling loop for human to choose next action
        action_to_play = None
        while not action_to_play:
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and BOARD.collidepoint(event.pos):
                for action in pool:
                    if CELLS[action].collidepoint(event.pos):
                        action_to_play = action
                        break
    
    elif current['type'] == 'AI':
            action_to_play = get_AI(current, other, pool, 'hard')


    # Play the chosen action 
    current['played'].append(action_to_play)
    pool.remove(action_to_play)
    draw_cell(action_to_play, 'black', current['sign'])
    pygame.display.update()


    # If end of game
    if (winning_streak := test_win(current)) or len(pool) == 0:

        if winning_streak:

            print('winning_streak:', winning_streak)

            if current['type'] == 'AI':
                message = 'Computer wins'
                color = 'red'
            else:
                message = 'You win!'
                color = 'green' 
            display_message(message, color)
            
            for action in winning_streak:
                draw_cell(action, color, current['sign'])


        elif len(pool) == 0:
            print('draw')
            display_message('Draw', 'blue')

        clock.tick(FPS) #needs to be added before the display.update for the update to appear on the screen
        pygame.display.update()

        # End or Restart game
        while True:
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                quit()
            elif event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                initialization()
                break


    # If game is not finished yet
    else:

        current, other = other, current
        pygame.event.clear()
        clock.tick(FPS)
    

