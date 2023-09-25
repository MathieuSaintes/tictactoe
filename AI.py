import itertools, random, copy

class Game:

    def __init__(self, current, other, pool):
        self.current = current
        self.other = other
        self.pool = pool
        self.winner = None

    def change_player(self):
        self.current, self.other = self.other, self.current



    def play(self, action):

        self.current['played'].append(action)
        self.pool.remove(action)

        if test_win(self.current):
            self.winner = self.current

        elif len(self.pool) == 0:
            self.winner = 'draw'

        self.change_player()



    def getrandom(self):
        return random.choice(self.pool)


    def getwinning(self, player):
        for action in self.pool:
            player['played'].append(action)
            if test_win(player):
                player['played'].pop()
                return action
            player['played'].pop()


    def getsmart(self, montecarlo=False):

        # the last action if only one remaining
        if len(self.pool) == 1:
            return self.pool[0]

        # otherwise the winning action if any
        if len(self.current['played']) >= 2 and (winning_action := self.getwinning(self.current)):
            return winning_action

        # otherwise the winning action of the other player if any
        if len(self.other['played']) >= 2 and (other_winning_action := self.getwinning(self.other)):
            return other_winning_action

        # Otherwise get random or montecarlo
        if montecarlo:
            return self.getmontecarlo()
        else:
            return self.getrandom()


    def getmontecarlo(self):

        highest = -1

        for action in self.pool:

            wins = 0 
            for _ in range(1000):

                new_game = copy.deepcopy(self)
                new_game.play(action)
                new_game.playout()

                if new_game.winner != 'draw' and new_game.winner['id'] == self.current['id']:
                    wins += 1

            print(action, wins)

            if wins > highest:
                highest = wins
                action_to_play = action

        return action_to_play



    def playout(self):
        while not self.winner:
            self.play(self.getsmart())





def test_win(player):
    for a,b,c in itertools.combinations(player['played'], 3):
        if (
                a[0] == b[0] == c[0] or 
                a[1] == b[1] == c[1] or
                (a[0] == a[1] and b[0] == b[1] and c[0] == c[1]) or
                (a[0] + a[1] == 2 and b[0] + b[1] == 2 and c[0] + c[1] == 2)
        ):
            return a,b,c
    return False


def get_AI(current, other, pool, level):
    game = Game(current, other, pool)
    if level == 'hard':
        return game.getsmart(montecarlo=True)
    elif level == 'medium':
        return game.getsmart(montecarlo=False)
    elif level == 'easy':
        return game.getrandom()

