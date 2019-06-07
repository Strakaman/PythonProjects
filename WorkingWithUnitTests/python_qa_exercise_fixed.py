WIN_CONDITIONS = [ [0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [6,4,2]]

PLAYERS = ['X','O']

class TicTacToe:

    def __init__(self):
        self.board = [None,None,None,None,None,None,None,None,None]
        self.last_player = 'O'
        self.remaining_win_conditions = WIN_CONDITIONS.copy()

    def resolve_turn(self):
        self.print_board()

        if self.possible_winner() and self.winner():
            print('%s has won the game, congratulations!' % self.last_player)
        elif len(self.remaining_win_conditions) == 0:
            if None in self.board:
                print('Tie! There is no path to victory')
            else:
                print('Tie! The board is full')

    def move(self, square):
        if self.last_player == PLAYERS[1]:
            player = PLAYERS[0]
        else:
            player = PLAYERS[1]
        if square > 8 or square < 0:
            raise ValueError('Square outside bounds')
        elif self.board[square] is not None:
            raise ValueError('Not a valid square')

        self.board[square] = player
        self.last_player = player
        self.resolve_turn()

    def possible_winner(self):
        if self.board.count(PLAYERS[0]) > 2 or self.board.count(PLAYERS[1]) > 2:
            return True
        else:
            return False

    def winner(self):
        curr_win_conditions = self.remaining_win_conditions.copy()
        for win in self.remaining_win_conditions:
            values = []
            for square in win:
                values.append(self.board[square])
            if values.count(self.last_player) == 3:
                return True
            elif values.count(PLAYERS[0]) > 0 and values.count(PLAYERS[1]) > 0:
                curr_win_conditions.remove(win)
        self.remaining_win_conditions = curr_win_conditions

    def print_board(self):
        i = 0
        squares = []

        for square in self.board:
            if square is None:
                squares.append(str(i))
            else:
                squares.append(square)
            i += 1

        print('%s | %s | %s\n----------\n%s | %s | %s\n----------\n%s | %s | %s' % tuple(squares))
