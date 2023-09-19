import itertools, random, pygame, copy
pygame.init()

class Game:

    def __init__(self):
        self.player1 = {    'id': 1, 
                            'sign': AI_SIGN, 
                            'type': 'AI', 
                            'level': 'hard',
                            'played': []            }
        self.player2 = {    'id': 2, 
                            'sign': HUMAN_SIGN, 
                            'type': 'human',
                            'played': []             }
        self.players = (self.player1, self.player2)
        self.current = random.choice(self.players)
        if self.current == self.player2:
            self.other = self.player1
        else:
            self.other = self.player2
        self.pool = list(itertools.product(range(3),repeat=2))
        self.winner = None
        self.winning_streak = None


    def wins(self, player):
        for a,b,c in itertools.combinations(player['played'], 3):
            if (
                    a[0] == b[0] == c[0] or 
                    a[1] == b[1] == c[1] or
                    (a[0] == a[1] and b[0] == b[1] and c[0] == c[1]) or
                    (a[0] + a[1] == 2 and b[0] + b[1] == 2 and c[0] + c[1] == 2)
            ):
                self.winning_streak = a,b,c
                return True
        return False


    def change_player(self):
        self.current, self.other = self.other, self.current


    def play(self, action):
    
        self.current['played'].append(action)
        self.pool.remove(action)

        if self.wins(self.current):
            self.winner = self.current

        elif len(self.pool) == 0:
            self.winner = 'draw'

        self.change_player()


    def unplay(self, action):
        if self.winner:
            self.winner = None
        self.change_player()
        self.pool.append(self.current['played'].pop()) 


    def playrandom(self):
        self.play(random.choice(self.pool))


    def playsmart(self, montecarlo=False):
        
        # Play the last action if only one remaining
        if len(self.pool) == 1:
            return self.play(self.pool[0])

        # Play the winning action if possible
        if len(self.current['played']) >= 2:
            for action in self.pool.copy():
                self.play(action)
                if self.winner:
                    return
                else:
                    self.unplay(action)

        # Avoid loosing otherwise if any
        if len(self.other['played']) >= 2:
            self.change_player()
            for action in self.pool.copy():
                self.play(action)
                if self.winner:
                    self.unplay(action)
                    self.change_player()
                    self.play(action)
                    return
                self.unplay(action)
            self.change_player()

        # Otherwise play random or montecarlo
        if montecarlo:
            self.playmontecarlo()
        else:
            self.playrandom()


    def playout(self):
        while not self.winner:
            action = self.playsmart()


    def copy(self):
        return copy.deepcopy(self)


    def playmontecarlo(self):

        highest = 0

        for action in self.pool:

            wins = 0 
            for _ in range(1000):

                new_game = self.copy()
                new_game.play(action)
                new_game.playout()

                if new_game.winner != 'draw' and new_game.winner['id'] == self.current['id']:
                    wins += 1

            print(action, wins)

            if wins > highest:
                highest = wins
                action_to_play = action

        self.play(action_to_play)



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



def getselected(pos):
    for i, action in enumerate(GAME.pool):
        if CELLS[action].collidepoint(pos):
            return action


def draw_board():

    DIS.fill('grey')
    DIS.fill('white', BOARD)

    for cell in CELLS.values():
        pygame.draw.rect(DIS, 'black', cell, width=1)

    for player in GAME.players:
        for action in player['played']:
            draw_cell(action, 'black', player['sign'])

    pygame.display.update()


def draw_cell(action, color, sign):
    DRAWING_AREA.center = CELLS[action].center
    if sign == 'O':
        pygame.draw.ellipse(DIS, color, DRAWING_AREA, width=1)
    elif sign == 'X':
        pygame.draw.line(DIS, color, DRAWING_AREA.topleft, DRAWING_AREA.bottomright)
        pygame.draw.line(DIS, color, DRAWING_AREA.topright, DRAWING_AREA.bottomleft)


def draw_win():

    if GAME.winner == 'draw':
        display_message('Draw', 'blue')

    else:
    
        if GAME.winner['type'] == 'AI':
            message = 'Computer wins'
            color = 'red'
        
        else:
            message = 'You win!'
            color = 'green'
        
        display_message(message, color)
        
        for action in GAME.winning_streak:
            draw_cell(action, color, GAME.winner['sign'])

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

# Game Initialization
GAME = Game()
draw_board()

# Main game loop
while True:

    if GAME.winner:

        draw_win()

        while True:
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                quit()
            elif event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                GAME = Game()
                draw_board()
                break


    # Choose next action (action)

    if  GAME.current['type'] == 'human':
        # Event handling loop for human to choose next action
        while True:
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and (action := getselected(event.pos)):
                GAME.play(action)
                break

    else:
        GAME.playsmart(montecarlo=True)


    # 
    draw_board()
    pygame.event.clear()

    for player in GAME.players:
        print(player['sign'], player['played'])
    print('pool', GAME.pool)
    print()

    clock.tick(FPS)
    

