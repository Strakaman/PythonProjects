from python_qa_exercise_fixed import TicTacToe
from python_qa_exercise_fixed import PLAYERS
while True:
    currGame = TicTacToe()
    print("\n\n\nNew Game:")
    currGame.print_board()
    while True:
        currPlayer = PLAYERS[0]
        if currGame.last_player == PLAYERS[0]:
            currPlayer = PLAYERS[1]
        print("It's player " + currPlayer + 's turn.')
        try:
            location = int(input("Choose a spot: "))
            currGame.move(location)
        except ValueError:
            print("Bad input try again.")
            continue
        if currGame.winner() or currGame.remaining_win_conditions == []:
            break

