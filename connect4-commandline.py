import numpy as np
import pygame
import sys

# numpy , pygame

ROW_COUNT = 12
COLUMN_COUNT = 8
PIECES = {"1": {"dot": (1, 2), "color": (1, 2)}, "2": {"dot": (2, 1), "color": (2, 1)},
          "3": {"dot": (2, 1), "color": (2, 1)}, "4": {"dot": (1, 2), "color": (1, 2)},
          "5": {"dot": (2, 1), "color": (1, 2)}, "6": {"dot": (1, 2), "color": (2, 1)},
          "7": {"dot": (1, 2), "color": (2, 1)},
          "8": {"dot": (2, 1), "color": (1, 2)}}  # dot->1:black,2:white; color->1:red, 2:white
DOT = "dot"
COLOR = "color"


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def drop_piece(dot_board, color_board, piece_pos, type, steps):
    coordinate= [coordinate_translation(piece_pos[0]), coordinate_translation(piece_pos[1])]
    dot_board[coordinate[0][0]][coordinate[0][1]] = PIECES[type][DOT][0]
    dot_board[coordinate[1][0]][coordinate[1][1]] = PIECES[type][DOT][1]
    color_board[coordinate[0][0]][coordinate[0][1]] = PIECES[type][COLOR][0]
    color_board[coordinate[1][0]][coordinate[1][1]] = PIECES[type][COLOR][1]
    steps[piece_pos]=


def get_piece_position(pos, type):
    if type == "1" or type == "3" or type == "5" or type == "7":
        return [pos, (chr(ord(pos[0]) + 1), pos[1])]
    elif type == "2" or type == "4" or type == "6" or type == "8":
        return [pos, (pos[0], str(int(pos[1]) + 1))]


def is_valid_location(board, pos, type):
    if type == "1" or type == "3" or type == "5" or type == "7":
        for tuple in pos:
            if tuple[0] < 'A' or tuple[0] > 'H' or int(tuple[1]) > 12 or int(tuple[1]) < 1:
                return False
            if board[int(tuple[1])][ord(tuple[0])-ord('A')] != 0:
                return False
            if int(tuple[1]) - 1 >= 1 and board[int(tuple[1]) - 2][ord(tuple[0])-ord('A')] == 0:
                return False
    elif type == "2" or type == "4" or type == "6" or type == "8":
        if pos[0][0] < 'A' or pos[0][0] > 'H' or int(pos[0][1]) > 12 or int(pos[0][1]) < 1:
            return False
        if board[int(pos[0][1])][ord(pos[0][0]) - ord('A')] != 0:
            return False
        if int(pos[0][1]) - 1 >= 1 and board[int(pos[0][1]) - 1][ord(pos[0][0]) - ord('A')] == 0:
            return False
    return True


def is_valid_piece(origin_pos, pos, steps):
    pass


def substitution(board, origin_pos, pos, type, steps):
    pass


def print_board(board):
    print(np.flip(board, 0))


def is_full_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[c][r] == 0:
                return False
    return True


def coordinate_translation(coordinate):
    return (int(coordinate[1])-1, ord(coordinate[0])-ord('A'))


def winning_move(board, piece):
    # Check vertical
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == board[r+1][c] and board[r+1][c] == board[r + 2][c] and board[r + 2][c] == board[r + 3][
                c] and board[r][c] != 0:
                return True

    # Check horizantal
    for c in range(ROW_COUNT):
        for r in range(COLUMN_COUNT - 3):
            if board[c][r] == board[c][r + 1] and board[c][r + 1] == board[c][r + 2] and board[c][r + 2] == board[c][
                r + 3] and board[c][r] != 0:
                return True

    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == board[r + 1][c + 1] and board[r + 1][c + 1] == board[r + 2][c + 2] and board[r + 2][
                c + 2] == board[r + 3][c + 3] and board[r][c] != 0:
                return True

    # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == board[r - 1][c + 1] and board[r - 1][c + 1] == board[r - 2][c + 2] and board[r - 2][
                c + 2] == board[r - 3][c + 3] and board[r][c] != 0:
                return True
    return False


dot_board = create_board()
color_board = create_board()
print(dot_board)
print(color_board)
game_over = False
turn = 0
recycle = False
steps = {}
player1 = input("Player 1 choose side: 1.dot; 2.color")
player2 = input("Player 2 choose side: 1.dot; 2.color")

while not game_over:

    # Ask for Player 1 Input
    if not recycle:
        if turn == 0:
            string = input("Player 1 turn: ")
        else:
            string = input("Player 2 turn: ")
    else:
        if turn == 0:
            string = input("Player 1 turn(recycle): ")
        else:
            string = input("Player 2 turn(recycle): ")
    string = string.split(" ")

    if len(string) == 4:
        pos = (string[2], string[3])
        type = string[1]

        piece_pos = get_piece_position(pos, type)

        if is_valid_location(dot_board, piece_pos, type):
            drop_piece(dot_board, color_board, piece_pos, type, steps)
        else:
            print("The operation is illegal")
            continue
    else:
        origin_pos = [(string[0], string[1]), (string[2], string[3])]
        type = string[4]
        pos = (string[5], string[6])
        if is_valid_piece(origin_pos, pos, steps):
            substitution(dot_board, origin_pos, pos, type, steps)
            substitution(color_board, origin_pos, pos, type, steps)

    dot_win = winning_move(dot_board, piece_pos)
    color_win = winning_move(color_board, piece_pos)
    if dot_win and color_win:
        if turn == 0:
            print("Player 1 Wins!")
        else:
            print("Player 2 Wins!")
        game_over = True
    elif dot_win:
        if player1 == "1":
            print("Player 1 Wins!")
        else:
            print("Player 2 Wins!")
        game_over = True
    elif color_win:
        if player1 == "2":
            print("Player 1 Wins!")
        else:
            print("Player 2 Wins!")
        game_over = True

    print_board(dot_board)
    print_board(color_board)
    if is_full_board(dot_board):
        recycle = True
    turn += 1
    turn = turn % 2
