__author__ = 'flyee'


def print_instruction():
    print("Input following cell number to make your move:")
    print_board([3] * 9)


def print_board(board):
    print("The board look like this:\n")
    for i in range(3):
        for j in range(3):
            pos = i * 3 + j
            if board[pos] == 1:
                print(' X ', end='')
            elif board[pos] == 0:
                print(' O ', end='')
            elif board[pos] == -1:
                print(' ' * 3, end="")
            else:
                print(' {} '.format(pos), end='')
            if j != 2:
                print('|', end='')
        print()
        print("-" * 11 if i != 2 else "")


def get_input(turn):
    valid = False
    while not valid:
        user = int(input("Where would you like to place " + turn + " (1-9)? "))
        if 0 <= user < 9:
            return user
        else:
            print(user + " is not a valid move! Please try again.\n")
            print_instruction()


def check_win(board):
    win_cond = ((1, 2, 3), (4, 5, 6), (7, 8, 9), (1, 4, 7), (2, 5, 8), (3, 6, 9), (1, 5, 9), (3, 5, 7))
    for each in win_cond:
        try:
            if board[each[0] - 1] == board[each[1] - 1] and board[each[1] - 1] == board[each[2] - 1]:
                return board[each[0] - 1]
        except:
            pass

    return -1


def main():
    print_instruction()
    board = [-1] * 9
    win = False
    move = 1
    while (not win) and (move < 10):
        print_board(board)
        print("Turn number " + str(move))
        if move % 2 == 0:
            turn = 'X'
        else:
            turn = 'O'
        user = get_input(turn)
        while board[user] != -1:
            print("Invalid move! Cell already taken. Please try again.\n")
            user = get_input(turn)
        board[user] = 1 if turn == 'X' else 0
        winner = check_win(board)
        if winner != -1:
            win = True
            print_board(board)
            print("The winner is " + ('X' if winner == 1 else 'O') + " :)")
        elif move == 9:
            print_board(board)
            print("No winner :(")
        move += 1



if __name__ == '__main__':
    main()
