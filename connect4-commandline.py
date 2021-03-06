import numpy as np
from sys import stdin

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


def to_string(piece_pos):
    return piece_pos[0][0] + piece_pos[0][1] + piece_pos[1][0] + piece_pos[1][1]


def drop_piece(dot_board, color_board, piece_pos, type, step_record, step_counter):
    coordinate = [coordinate_translation(piece_pos[0]), coordinate_translation(piece_pos[1])]
    dot_board[coordinate[0][0]][coordinate[0][1]] = PIECES[type][DOT][0]
    dot_board[coordinate[1][0]][coordinate[1][1]] = PIECES[type][DOT][1]
    color_board[coordinate[0][0]][coordinate[0][1]] = PIECES[type][COLOR][0]
    color_board[coordinate[1][0]][coordinate[1][1]] = PIECES[type][COLOR][1]
    step_record[to_string(piece_pos)] = str(step_counter) + "," + str(type)


def remove_piece(dot_board, color_board, piece_pos):
    coordinate = [coordinate_translation(piece_pos[0]), coordinate_translation(piece_pos[1])]
    dot_board[coordinate[0][0]][coordinate[0][1]] = 0
    dot_board[coordinate[1][0]][coordinate[1][1]] = 0
    color_board[coordinate[0][0]][coordinate[0][1]] = 0
    color_board[coordinate[1][0]][coordinate[1][1]] = 0


def get_piece_position(pos, type):
    if int(type) % 2 == 1:
        return [pos, (chr(ord(pos[0]) + 1), pos[1])]
    elif int(type) % 2 == 0:
        return [pos, (pos[0], str(int(pos[1]) + 1))]


def is_valid_location(board, pos, type):
    if int(type) % 2 == 1:
        for tuple in pos:
            if tuple[0] < 'A' or tuple[0] > 'H' or int(tuple[1]) > 12 or int(tuple[1]) < 1:
                return False
            if board[int(tuple[1]) - 1][ord(tuple[0]) - ord('A')] != 0:
                return False
            if int(tuple[1]) - 1 >= 1 and board[int(tuple[1]) - 2][ord(tuple[0]) - ord('A')] == 0:
                return False
    elif int(type) % 2 == 0:
        if pos[0][0] < 'A' or pos[0][0] > 'H' or pos[1][0] > 'H' or int(pos[0][1]) > 12 or int(pos[0][1]) < 1:
            return False
        if board[int(pos[0][1]) - 1][ord(pos[0][0]) - ord('A')] != 0:
            return False
        if int(pos[0][1]) - 1 >= 1 and board[int(pos[0][1]) - 2][ord(pos[0][0]) - ord('A')] == 0:
            return False
    return True


def is_recycle_legal(origin_pos, origin_pos_str, step_record, new_pos_str, new_type, step_counter):
    if piece_not_in_board(origin_pos_str, step_record):
        print("The piece is not in the board.")
        print("Please select a valid piece in the board to recycle.")
        return False

    origin_type = step_record.get(origin_pos_str).split(",")[1]
    origin_step_num = step_record.get(origin_pos_str).split(",")[0]
    if origin_step_num == str(step_counter - 1):
        print("You cannot recycle the piece which another player just put.")
        print("Please select a valid piece in the board to recycle.")
        return False

    # check if there is any piece on it.
    if int(origin_type) % 2 == 1:
        # 1,3,5,7
        coordinate = [get_upper_coordinate(origin_pos[0]), get_upper_coordinate(origin_pos[1])]
        if dot_board[coordinate[0][0]][coordinate[0][1]] != 0 or dot_board[coordinate[1][0]][coordinate[1][1]] != 0:
            print("you cannot recycle a card that has something on top of it.")
            return False


    elif int(origin_type) % 2 == 0:
        # 2,4,6,8
        coordinate = [get_upper_coordinate(origin_pos[0]), get_upper_coordinate(origin_pos[1])]
        if dot_board[coordinate[1][0]][coordinate[1][1]] != 0:
            print("you cannot recycle a card that has something on top of it.")
            return False

    if origin_pos_str == new_pos_str and origin_type == new_type:
        print("You cannot take one piece and put it back with no changes.")
        print("Please select a valid piece in the board to recycle.")
        return False
    return True


def piece_not_in_board(pos_str, step_record):
    if pos_str in step_record:
        return False
    else:
        return True


def print_board(board):
    print(np.flip(board, 0))


def coordinate_translation(coordinate):
    return (int(coordinate[1]) - 1, ord(coordinate[0]) - ord('A'))


def get_upper_coordinate(coordinate):
    return (int(coordinate[1]), ord(coordinate[0]) - ord('A'))


def winning_move(board, piece):
    # Check vertical
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == board[r + 1][c] and board[r + 1][c] == board[r + 2][c] and board[r + 2][c] == \
                    board[r + 3][
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


def is_game_over(dot_board, color_board, piece_pos, player1, player2):
    dot_win = winning_move(dot_board, piece_pos)
    color_win = winning_move(color_board, piece_pos)
    if dot_win and color_win:
        if turn == 0:
            if player1 == "1":
                print("Player 1 Wins with dot!")
            else:
                print("Player 1 Wins with color!")
        else:
            if player2 == "1":
                print("Player 2 Wins with dot!")
            else:
                print("Player 2 Wins with color!")
        return True
    elif dot_win:
        if player1 == "1":
            print("Player 1 Wins with dot!")
        else:
            print("Player 2 Wins with dot!")
        return True
    elif color_win:
        if player1 == "2":
            print("Player 1 Wins with color!")
        else:
            print("Player 2 Wins with color!")
        return True


dot_board = create_board()
color_board = create_board()
print(dot_board)
print(color_board)
game_over = False
turn = 0
recycle = False
step_counter = 1
step_record = dict()

player1 = input("Player 1 choose side: 1.dot; 2.color")
player2 = input("Player 2 choose side: 1.dot; 2.color")

while not game_over:
    if step_counter > 60:
        print("No player has won, game ends.")
        break
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
        if recycle is True:
            print("You have no card, please recycle a card from the board.")
            continue
        pos = (string[2], string[3])
        type = string[1]

        piece_pos = get_piece_position(pos, type)

        if is_valid_location(dot_board, piece_pos, type):
            drop_piece(dot_board, color_board, piece_pos, type, step_record, step_counter)
        else:
            print("The operation is illegal")
            print(string)
            continue
    else:
        if recycle is False:
            print("You still have piece, you cannot recycle a piece.")
            print("Please put a piece.")
            continue
        origin_pos = [(string[0], string[1]), (string[2], string[3])]
        origin_pos_str = to_string(origin_pos)
        new_type = string[4]
        new_pos_1st = (string[5], string[6])
        new_pos = get_piece_position(new_pos_1st, new_type)
        new_pos_str = to_string(new_pos)

        if not is_recycle_legal(origin_pos, origin_pos_str, step_record, new_pos_str, new_type, step_counter):
            continue

        fake_dot_board = dot_board
        fake_color_board = color_board
        remove_piece(fake_dot_board, fake_color_board, origin_pos)

        if is_valid_location(fake_dot_board, new_pos, new_type):
            remove_piece(dot_board, color_board, origin_pos)
            step_record.pop(origin_pos_str)
            drop_piece(dot_board, color_board, new_pos, new_type, step_record, step_counter)
        else:
            print("Please select a valid place on the board to recycle.")
            continue
    game_over = is_game_over(dot_board, color_board, piece_pos, player1, player2)
    print(string)
    print("Dot board    " + str(step_counter) + " round.   dot->1:black,2:white")
    print_board(dot_board)
    print("Color board    " + str(step_counter) + " round.   color->1:red, 2:white")
    print_board(color_board)

    if step_counter >= 24:
        recycle = True

    step_counter += 1
    turn += 1
    turn = turn % 2
