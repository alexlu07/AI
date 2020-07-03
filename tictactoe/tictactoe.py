"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    num_x = sum(l.count(X) for l in board)
    num_o = sum(l.count(O) for l in board)

    if num_x - num_o == 1:
        return O
    elif num_x - num_o == 0:
        return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    results = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                results.append([i, j])

    return results

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board_copy = copy.deepcopy(board)
    if board_copy[action[0]][action[1]] == EMPTY:
        board_copy[action[0]][action[1]] = player(board)
        return board_copy
    else:
        raise Exception

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    def check_win(a, b, c):
        if win:
            return win
        if a == b and b == c:
            return a
        else:
            return None

    win = None
    if board[1][1] != EMPTY:
        win = check_win(board[1][1], board[0][1], board[2][1])
        win = check_win(board[1][1], board[1][0], board[1][2])
        win = check_win(board[1][1], board[0][2], board[2][0])
        win = check_win(board[1][1], board[0][0], board[2][2])
        if win:
            return win
    if board[0][0] != EMPTY:
        win = check_win(board[0][0], board[0][1], board[0][2])
        win = check_win(board[0][0], board[1][0], board[2][0])
        if win:
            return win
    if board[2][2] != EMPTY:
        win = check_win(board[2][2], board[2][1], board[2][0])
        win = check_win(board[2][2], board[1][2], board[0][2])
        if win:
            return win
    return win


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True
    for i in board:
        for j in i:
            if j == EMPTY:
                return False
    return True



def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    if win == O:
        return -1
    return 0


def minimax(board, depth=0):
    """
    Returns the optimal action for the current player on the board.
    """
    if depth == 1: print(depth)
    if terminal(board):
        return utility(board)

    if player(board) == X:
        best_value = [-100, None]
        if board == initial_state():
            value = [minimax(result(board, [0, 0]), depth + 1), [0, 0]]
            best_value = max(best_value, value, key=lambda x: x[0])
        else:
            for action in actions(board):
                value = [minimax(result(board, action), depth + 1), action]
                best_value = max(best_value, value, key=lambda x: x[0])

        if depth == 0:
            return best_value[1]
        return best_value[0]

    if player(board) == O:
        best_value = [100, None]
        for action in actions(board):
            value = [minimax(result(board, action), depth + 1), action]
            best_value = min(best_value, value, key=lambda x: x[0])

        if depth == 0:
            return best_value[1]
        return best_value[0]
