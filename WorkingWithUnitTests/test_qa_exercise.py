import unittest
import sys
import io
from python_qa_exercise import TicTacToe
from python_qa_exercise import PLAYERS
from python_qa_exercise import WIN_CONDITIONS

BLANK_BOARD = '0 | 1 | 2\n----------\n3 | 4 | 5\n----------\n6 | 7 | 8\n'
EXPECTED_EMPTY_BOARD = [None] * 9
EXPECTED_PLAYERS = ['X','O']
EXPECTED_LAST_PLAYER = PLAYERS[1]
EXPECTED_WIN_CONDITIONS = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [6, 4, 2]]

class TestTTT(unittest.TestCase):
    '''Tests for TicTacToe class in python_qa_exercise.py'''

    '''Used to capture data that would be printed to console.'''
    def setup_print_test(self):
        self.capturedOutput = io.StringIO()
        sys.stdout = self.capturedOutput  # and redirect stdout.

    '''Uses before every test to guarantee state'''
    def reset_game(self):
        self.TTT = TicTacToe()

    def test_constructor(self):
        self.reset_game()
        self.assertCountEqual(WIN_CONDITIONS, EXPECTED_WIN_CONDITIONS, msg="Expected there to be 8 specific win conditions.")
        self.assertListEqual(self.TTT.board, EXPECTED_EMPTY_BOARD,msg="Expected empty board after initialization.")
        self.assertListEqual(PLAYERS, EXPECTED_PLAYERS, msg="Expected only Player1=X and Player2=O")
        self.assertEqual(self.TTT.last_player, EXPECTED_LAST_PLAYER, msg="Expected last player to be player 2.")

    def test_move(self):
        self.reset_game()
        '''Check out of bounds >'''
        self.assertRaises(ValueError, self.TTT.move, 9)

        self.reset_game()
        '''Check out of bounds <'''
        self.assertRaises(ValueError, self.TTT.move, -1)

        self.reset_game()
        self.TTT.board[1] = PLAYERS[1]
        '''Player 2 move to an already taken spot'''
        self.assertRaises(ValueError, self.TTT.move, 1)

        self.reset_game()
        '''Player 1 move to an already taken spot'''
        self.TTT.board[1] = PLAYERS[0]
        self.assertRaises(ValueError, self.TTT.move, 1)

        for player in PLAYERS:
            for i in range(9):
                self.reset_game()
                if player == PLAYERS[0]:
                    self.TTT.last_player = PLAYERS[1]
                else:
                    self.TTT.last_player = PLAYERS[0]
                self.TTT.move(i)
                test_list = [None,None,None,None,None,None,None,None,None]
                test_list[i] = player
                '''Board state check after player move is registered'''
                self.assertListEqual(self.TTT.board, test_list, msg="boards should be equal: " + str(test_list) + "\n" + str(self.TTT.board))
                '''Check that last player is updated to the player that just went.'''
                self.assertEqual(self.TTT.last_player,player,msg="Last player was not updated after the player moved.")

    def test_possible_winner(self):
        self.reset_game()
        self.assertFalse(self.TTT.possible_winner(),msg="No one should have won yet.")

        for player in PLAYERS:
            self.reset_game()
            for i in range(0,5,2):
                self.TTT.board[i] = player
            '''Test that if player has gone at least 3 times, they can win'''
            self.assertTrue(self.TTT.possible_winner(),msg="Player " + player + " should be a possible winner: " + str(self.TTT.board))

        for player in PLAYERS:
            self.reset_game()
            for i in range(0, 5):
                self.TTT.board[i] = player
            '''Test that if player has gone more than 3 times, they can win'''
            self.assertTrue(self.TTT.possible_winner(),
                            msg="Player " + player + " should be a possible winner: " + str(self.TTT.board))

        self.reset_game()
        for player in PLAYERS:
            for i in range(0,3,2):
                self.TTT.board[i] = player
            '''Test that no possible winner with one player only having gone twice'''
            self.assertFalse(self.TTT.possible_winner(),msg="There should be no possible winners: " + str(self.TTT.board))

    def test_print_board(self):
        self.reset_game()
        self.setup_print_test()
        self.TTT.print_board()
        '''Test that board can print empty spaces as expected'''
        self.assertEqual(self.capturedOutput.getvalue(), BLANK_BOARD,msg="Blank board print layout does not match expected layout.")

        for player in PLAYERS:
            self.reset_game()
            self.setup_print_test()
            for i in range(0, 9):
                self.TTT.board[i] = player
            self.TTT.print_board()
            '''Test that board is able to print characters that represent each player'''
            self.assertEqual(self.capturedOutput.getvalue(),
                             '%s | %s | %s\n----------\n%s | %s | %s\n----------\n%s | %s | %s\n' % ((player,)*9)) #generate tuple with same character

        sys.stdout = sys.__stdout__  # Reset redirect.

    def test_winner(self):
        for player in PLAYERS:
            for wc in WIN_CONDITIONS:
                self.reset_game()
                self.TTT.last_player = player
                for i in range(9):
                    if i in wc:
                        self.TTT.board[i] = player
                '''Test if win condition is recognized'''
                self.assertTrue(self.TTT.winner(), msg="Winner should be detected in this scenario:\n"+ str(self.TTT.board))

        '''Test that a few non win scenarios return false'''
        self.reset_game()
        self.TTT.board = [PLAYERS[0],PLAYERS[1],PLAYERS[0],PLAYERS[1],PLAYERS[1],PLAYERS[0],None,PLAYERS[0],PLAYERS[1]]
        '''One false scenario'''
        self.assertFalse(self.TTT.winner(),msg="No winner should be possible.\n" + str(self.TTT.board))

        self.reset_game()
        self.TTT.board = [None,None,PLAYERS[0],PLAYERS[1],PLAYERS[1],PLAYERS[0],None,PLAYERS[0],PLAYERS[1]]
        '''False scenario 1'''
        self.assertFalse(self.TTT.winner(),msg="No winner should be possible.\n" + str(self.TTT.board))

        self.reset_game()
        self.TTT.board = [None,None,PLAYERS[0],None,None,PLAYERS[0],None,PLAYERS[1],PLAYERS[1]]
        '''False scenario 2'''
        self.assertFalse(self.TTT.winner(),msg="No winner should be possible.\n" + str(self.TTT.board))

        self.reset_game()
        self.TTT.board = [PLAYERS[0],None,None,None,None,None,None,None,None]
        '''Test that no win conditions have been removed'''
        self.TTT.winner()
        self.assertCountEqual(self.TTT.remaining_win_conditions, EXPECTED_WIN_CONDITIONS,
                              msg="No win conditions should have been removed based on the board state:\n" + str(self.TTT.board))

        for wc in EXPECTED_WIN_CONDITIONS:
            self.reset_game()
            self.TTT.board[wc[0]] = PLAYERS[0]
            self.TTT.board[wc[1]] = PLAYERS[1]
            self.TTT.board[wc[2]] = PLAYERS[0]
            test_remaining_condititons_list = WIN_CONDITIONS.copy()
            test_remaining_condititons_list.remove(wc)
            self.assertFalse(self.TTT.winner(), msg="No winner should be possible.\n" + str(self.TTT.board))
            '''Test if correct win condition is removed when condition is no longer met'''
            self.assertCountEqual(self.TTT.remaining_win_conditions, test_remaining_condititons_list,
                                  msg="Specific win condition was not removed as expected: " + str(wc))

        self.reset_game()
        self.TTT.board = [PLAYERS[0], PLAYERS[1], PLAYERS[0], PLAYERS[1], None, PLAYERS[0], PLAYERS[1], PLAYERS[0],
                          PLAYERS[1]]
        '''False scenario 3'''
        self.assertFalse(self.TTT.winner(), msg="No winner should be possible.\n" + str(self.TTT.board))
        '''Verify all possible win conditions have been removed'''
        self.assertCountEqual(self.TTT.remaining_win_conditions, [],
                              msg="There should be no more remaining win conditions \n" + str(
                                  self.TTT.remaining_win_conditions))

    def test_resolve_turn(self):
        self.reset_game()
        self.setup_print_test()
        self.TTT.resolve_turn()
        output = self.capturedOutput.getvalue()
        remaining_output = output.replace(BLANK_BOARD,"") #use string replace as resolve turn prints board
        '''Test that nothing is printed if the game is not finished'''
        self.assertEqual(remaining_output,"",msg="No end of game text should have been printed as game should not be over:\n" + str(self.TTT.board))

        for player in PLAYERS:
            self.setup_print_test()
            for i in range(0, 9):
                self.TTT.board[i] = player
            self.TTT.last_player = player
            self.TTT.resolve_turn()
            output = self.capturedOutput.getvalue()
            #print ("Captured:\n\n" + output)
            remaining_output = output.replace('%s | %s | %s\n----------\n%s | %s | %s\n----------\n%s | %s | %s\n' % ((player,)*9),"") #use string replace as resolve turn prints board
            '''Test that appropriate player wins string is printed under a guaranteed win situation'''
            self.assertEqual(remaining_output,'%s has won the game, congratulations!\n' % player,
                             msg="Specific player expected to have won game based on board state:\n"+str(self.TTT.board))

        self.reset_game()
        self.setup_print_test()
        self.TTT.remaining_win_conditions = []
        self.TTT.resolve_turn()
        output = self.capturedOutput.getvalue()
        remaining_output = output.replace(BLANK_BOARD, "")  # use string replace as resolve turn prints board
        '''Test that the game is recognized as a tie if there are no win conditions'''
        self.assertEqual(remaining_output,"Tie! There is no path to victory\n",
                         msg="Tie expected due to lack of win conditions.")


        self.reset_game()
        self.setup_print_test()
        self.TTT.remaining_win_conditions = []
        self.TTT.board = [PLAYERS[0],PLAYERS[1],PLAYERS[0],PLAYERS[1],PLAYERS[1],PLAYERS[0],None,PLAYERS[0],PLAYERS[1]]
        self.TTT.resolve_turn()
        output = self.capturedOutput.getvalue()
        remaining_output = output.replace('{0} | {1} | {0}\n----------\n{1} | {1} | {0}\n----------\n6 | {0} | {1}\n'.format(PLAYERS[0],PLAYERS[1]), "")  # use string replace as resolve turn prints board
        '''Test that the game is recognized as a tie if there are no win conditions but still remaining moves.'''
        self.assertEqual(remaining_output,"Tie! There is no path to victory\n",msg="Tie expected due to lack of win conditions.")

        self.reset_game()
        self.setup_print_test()
        self.TTT.remaining_win_conditions = []
        self.TTT.board = [PLAYERS[0],PLAYERS[1],PLAYERS[0],PLAYERS[1],PLAYERS[0],PLAYERS[1],PLAYERS[0],PLAYERS[1],PLAYERS[0]]
        self.TTT.resolve_turn()
        output = self.capturedOutput.getvalue()
        remaining_output = output.replace('{0} | {1} | {0}\n----------\n{1} | {0} | {1}\n----------\n{0} | {1} | {0}\n'.format(PLAYERS[0],PLAYERS[1]), "")  # use string replace as resolve turn prints board
        '''Test that the game is recognized as a tie if there are no more places to go'''
        self.assertEqual(remaining_output,"Tie! The board is full\n",msg="Tie expected due to lack of open spaces.")

        sys.stdout = sys.__stdout__  # Reset redirect.

if __name__ == '__main__':
    unittest.main()