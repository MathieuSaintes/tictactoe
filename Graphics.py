import itertools, random, pygame
from AI import *
pygame.init()

MEDIUM_FONT = pygame.font.Font(None, 30)
LARGE_FONT = pygame.font.Font(None, 60)

def blit_text(text, color, font, center):
    text_surface = font.render(text, True, color)
    DIS.blit(text_surface, text_surface.get_rect(center=center))

class Button(pygame.Rect):
    def __init__(self, content, color, font, bgcolor, width, height, center):
        self.content = content
        self.color = color
        self.font = font
        self.bgcolor = bgcolor
        super().__init__(0, 0, width, height)
        self.center = center
    def draw(self):
        DIS.fill(self.bgcolor, self)
        pygame.draw.rect(DIS, 'black', self, width=1)
        blit_text(self.content.upper(), self.color, self.font, self.center)


def draw_cell(action, color, sign):
    DRAWING_AREA.center = CELLS[action].center
    if sign == 'O':
        pygame.draw.ellipse(DIS, color, DRAWING_AREA, width=1)
    elif sign == 'X':
        pygame.draw.line(DIS, color, DRAWING_AREA.topleft, DRAWING_AREA.bottomright)
        pygame.draw.line(DIS, color, DRAWING_AREA.topright, DRAWING_AREA.bottomleft)


def select_button(buttons):
    DIS.fill('grey')
    for button in buttons:
        button.draw()
    pygame.display.update()
    while True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                if button.collidepoint(event.pos):
                    return button.content


def initialization():

    global player1, player2, pool, current, other, level

    # Choose sign and level
    HUMAN_SIGN = select_button(sign_buttons)
    AI_SIGN = {'X': 'O', 'O': 'X'}[HUMAN_SIGN]
    level = select_button(level_buttons)
    
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


###  Creation of the sign and level buttons  ###

signs = ('X', 'O')
sign_buttons = []
for i, sign in enumerate(signs):
    sign_buttons.append( Button(sign, 'black', LARGE_FONT, bgcolor='white', width=8*BLK, height=8*BLK, center=((1+2*i)*DIS_WIDTH//4 , DIS_WIDTH//2)) )

levels = ('easy', 'medium', 'hard')
level_buttons = []
for i, level in enumerate(levels):
    level_buttons.append( Button(level, 'black', MEDIUM_FONT, bgcolor='white', width=20*BLK, height=8*BLK, center=(DIS_WIDTH//2 , (i+1)*DIS_WIDTH//4)) )



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
            action_to_play = get_AI(current, other, pool, level)


    # Play the chosen action 
    current['played'].append(action_to_play)
    pool.remove(action_to_play)
    draw_cell(action_to_play, 'black', current['sign'])
    pygame.display.update()


    # If end of game
    if (winning_streak := test_win(current)) or len(pool) == 0:

        if winning_streak:

            if current['type'] == 'AI':
                message = 'Computer wins'
                color = 'red'
            else:
                message = 'You win!'
                color = 'green' 
            
            for action in winning_streak:
                draw_cell(action, color, current['sign'])

        elif len(pool) == 0:

            message = 'Draw'
            color = 'blue'

        blit_text(message, color, MEDIUM_FONT, center=DIS.get_rect().center)
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
    

