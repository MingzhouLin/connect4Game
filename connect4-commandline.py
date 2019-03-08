import numpy as np
from treeBag.Node import Node
from treeBag.Tree import Tree
import copy
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
MIN = "min"
MAX = "max"

RECYCLE_TIME = 4

root_grade = 0
times_of_e = 0
level_2_content = "\n"


def resetTRACE_CONTENT():
    global root_grade
    global times_of_e
    global level_2_content

    root_grade = 0
    times_of_e = 0
    level_2_content = "\n"


def create_weight_board():
    b = list()
    for i in range(8):
        start_num = 10 * i + 1
        b.append(np.arange(start_num, start_num + 8))
    return b


WEIGHT_BOARD = create_weight_board()


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT), dtype=np.int)
    return board


def to_string(piece_pos):
    return piece_pos[0][0] + piece_pos[0][1] + piece_pos[1][0] + piece_pos[1][1]


def drop_piece(dot_board, color_board, piece_pos, type, step_record, step_number=None):
    coordinate = [coordinate_translation(piece_pos[0]), coordinate_translation(piece_pos[1])]
    dot_board[coordinate[0][0]][coordinate[0][1]] = PIECES[type][DOT][0]
    dot_board[coordinate[1][0]][coordinate[1][1]] = PIECES[type][DOT][1]
    color_board[coordinate[0][0]][coordinate[0][1]] = PIECES[type][COLOR][0]
    color_board[coordinate[1][0]][coordinate[1][1]] = PIECES[type][COLOR][1]
    if step_number is not None:
        step_record[to_string(piece_pos)] = str(step_number) + "," + str(type)


def remove_piece(dot_board, color_board, piece_pos):
    coordinate = [coordinate_translation(piece_pos[0]), coordinate_translation(piece_pos[1])]
    dot_board[coordinate[0][0]][coordinate[0][1]] = 0
    dot_board[coordinate[1][0]][coordinate[1][1]] = 0
    color_board[coordinate[0][0]][coordinate[0][1]] = 0
    color_board[coordinate[1][0]][coordinate[1][1]] = 0
    return dot_board, color_board


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
    if not check_upper_piece(origin_type, origin_pos):
        return False

    if origin_pos_str == new_pos_str and origin_type == new_type:
        print("You cannot take one piece and put it back with no changes.")
        print("Please select a valid piece in the board to recycle.")
        return False
    return True


def check_upper_piece(origin_type, origin_pos):
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
    return True


def piece_not_in_board(pos_str, step_record):
    if pos_str in step_record:
        return False
    else:
        return True


def print_board(board):
    print(np.flip(board, 0))


def coordinate_translation(coordinate):
    if type(coordinate[0]) is str:
        return (int(coordinate[1]) - 1, ord(coordinate[0]) - ord('A'))
    if type(coordinate[0]) is int:
        return (chr(ord('A') + coordinate[0]), str(coordinate[1] + 1))


def get_upper_coordinate(coordinate):
    return (int(coordinate[1]), ord(coordinate[0]) - ord('A'))


def heuristic_matrix_estimation(dot_board, color_board):
    clique = {"11": 0, "12": 0, "21": 0, "22": 0}
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT):
            if color_board[r][c] != 0:
                key = str(color_board[r][c]) + str(dot_board[r][c])
                clique[key] += WEIGHT_BOARD[r][c]
    grade = clique["22"] + 3 * clique["21"] - 2 * clique["11"] - 1.5 * clique["12"]
    return grade


def winning_move(board):
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


def is_game_over(dot_board, color_board, player1, player2):
    dot_win = winning_move(dot_board)
    color_win = winning_move(color_board)
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


def compute_best_step(dot_board, color_board, mode, current_step):
    global root_grade
    global times_of_e
    global level_2_content

    resetTRACE_CONTENT()
    tree = build_tree(dot_board, color_board, current_step)

    if mode is "1":
        res_node = minimax(tree)
    else:
        grade_of_root = alphabeta(tree.root, float('-inf'), float('+inf'), 3)
        for child in tree.root.children:
            if child.grade is grade_of_root:
                tree.root.next_move = child
                res_node = child
                break
    write_trace_file(times_of_e, root_grade, level_2_content)

    return tree


def get_next_ai_move_string(ai_next_piece):
    string = "0 " + ai_next_piece.last_piece_type + " " + ai_next_piece.step[0][0] \
             + " " + ai_next_piece.step[0][1]
    return string


def build_tree(dot_board, color_board, current_step):
    node_id = 0
    root_grade = 0
    root = Node(node_id, dot_board, color_board, None, 1, MAX, None, root_grade, None)
    node_id += 1
    tree = Tree(root)
    tree.level[1] = [root]
    # could set a cut-off to set the leaf level
    node_id, tree = extend_tree(tree, 1, MIN, node_id, current_step)
    node_id, tree = extend_tree(tree, 2, MAX, node_id, current_step+1)
    return tree


def write_trace_file(times_of_e, root_grade, level_2_content):
    content = str(times_of_e) + "\n" + str(root_grade) + "\n" + level_2_content
    file = open('TraceOut.txt', 'a')
    file.write(content)
    file.close()


def minimax(tree):
    # trace parameters
    global root_grade
    global times_of_e
    global level_2_content

    tree_depth = len(tree.level)

    for i in range(tree_depth, 0, -1):
        for n in tree.level[i]:

            if len(n.children) is 0:
                n.grade = heuristic_matrix_estimation(n.dot_board, n.color_board)
                times_of_e = times_of_e + 1
                continue

            opt_value = 0.0
            option = n.level_type

            if n.level_type is MAX:
                opt_value = float('-inf')  #
            else:
                opt_value = float('inf')  #
            for child in n.children:
                if option is MAX:
                    if child.grade > opt_value:
                        opt_value = child.grade
                        n.next_move = child

                else:
                    if child.grade < opt_value:
                        opt_value = child.grade
                        n.next_move = child
            n.grade = opt_value
            if n.level_type is MIN:
                level_2_content = level_2_content + str(n.grade) + "\n"
    root_grade = tree.root.grade

    return tree.root.next_move


def alphabeta(node, alpha, beta, depth):
    global root_grade
    global times_of_e
    global level_2_content
    if node.level == depth:
        node.grade = heuristic_matrix_estimation(node.dot_board, node.color_board)
        times_of_e = times_of_e + 1
        return node.grade
    else:
        if node.level_type is MAX:
            for child in node.children:
                alpha = max(alpha, alphabeta(child, alpha, beta, depth))
                if alpha >= beta:
                    node.grade = alpha
                    return alpha
            node.grade = alpha
            return alpha

        else:
            for child in node.children:
                beta = min(beta, alphabeta(child, alpha, beta, depth))
                if beta <= alpha:
                    node.grade = beta
                    level_2_content = level_2_content + str(node.grade) + "\n"
                    return beta
            node.grade = beta
            level_2_content = level_2_content + str(node.grade) + "\n"
            return beta


def extend_tree(tree, level, role, node_id, current_step):
    tree.level[level + 1] = []
    for parent_node in tree.level[level]:
        for r in range(ROW_COUNT):
            for c in range(COLUMN_COUNT):
                if current_step < 24:
                    if (parent_node.dot_board[r][c] == 0 and r == 0) or (
                            parent_node.dot_board[r - 1][c] != 0 and parent_node.dot_board[r][c] == 0):
                        for i in range(1, 9):
                            type = str(i)
                            next_step = get_piece_position(coordinate_translation((c, r)), type)
                            if is_valid_location(dot_board, next_step, type):
                                tmp_dot_board = copy.deepcopy(parent_node.dot_board)
                                tmp_color_board = copy.deepcopy(parent_node.color_board)
                                drop_piece(tmp_dot_board, tmp_color_board, next_step, type, step_record, None)

                                # tmp_grade = heuristic_matrix_estimation(tmp_dot_board, tmp_color_board)
                                # calculate the grad later in minimax or alpha-beta

                                tmp_grade = 0
                                node = Node(node_id, tmp_dot_board, tmp_color_board, next_step, level + 1, role,
                                            parent_node,
                                            tmp_grade, type)
                                node_id += 1
                                parent_node.add_child(node)
                                tree.level[level + 1].append(node)
                else:
                    for board in get_all_possible_remove_pieces(step_record):
                        if (board[0][r][c] == 0 and r == 0) or (
                                board[0][r - 1][c] != 0 and board[0][r][c] == 0):
                            for i in range(1, 9):
                                type = str(i)
                                next_step = get_piece_position(coordinate_translation((c, r)), type)
                                next_step_str = next_step[0][0] + next_step[0][1] + next_step[1][0] + next_step[1][1]
                                if is_valid_location(board[0], next_step, type) and (
                                        (next_step_str not in step_record) or
                                        step_record[next_step_str].split(",")[1] != type):
                                    tmp_dot_board = board[0]
                                    tmp_color_board = board[1]
                                    drop_piece(tmp_dot_board, tmp_color_board, next_step, type, step_record, None)

                                    # tmp_grade = heuristic_matrix_estimation(tmp_dot_board, tmp_color_board)
                                    # calculate the grad later in minimax or alpha-beta

                                    tmp_grade = 0
                                    node = Node(node_id, tmp_dot_board, tmp_color_board, next_step, level + 1, role,
                                                parent_node,
                                                tmp_grade, type)
                                    node_id += 1
                                    parent_node.add_child(node)
                                    tree.level[level + 1].append(node)
    return node_id, tree


def get_all_possible_remove_pieces(step_record):
    boards = list()
    for step in step_record.items():
        keys = list(step_record.keys())
        if step[0] != keys[len(keys) - 1]:
            origin_type = step[1].split(",")[1]
            origin_position = [(step[0][0], step[0][1]), (step[0][2], step[0][3])]
            if check_upper_piece(origin_type, origin_position):
                temp_dot_board = copy.deepcopy(dot_board)
                temp_color_board = copy.deepcopy(color_board)
                boards.append(remove_piece(temp_dot_board, temp_color_board, origin_position))
    return boards


def update_record():
    remove_record = ""
    for step in step_record.keys():
        if dot_board[int(step[1]) - 1][ord(step[0]) - ord('A')] == 0 or dot_board[int(step[3]) - 1][
            ord(step[2]) - ord('A')] == 0:
            remove_record = step
    if remove_record != "":
        step_record.pop(remove_record)


dot_board = create_board()
color_board = create_board()
print(dot_board)
print(color_board)
game_over = False
turn = 0
recycle = False
step_counter = 1
step_record = dict()

ai_mode = input("Please input AI mode. 1. minimax  2. alpha-beta")
player1 = input("If AI plays as player1: 1.yes; 2.no")
player1 = int(player1)
side1 = input("Player 1 choose side: 1.dot; 2.color")
if side1 == 1:
    side2 = 2
    print("Player2 is on color side")
else:
    side2 = 1
    print("Player2 is on dot side")

while not game_over:
    if step_counter > 60:
        print("No player has won, game ends.")
        break
    # Ask for Player 1 Input
    if not recycle:
        if (turn == 0 and player1 == 2) or (turn == 1 and player1 == 1):
            string = input("Human turn: ")
        else:
            tree = compute_best_step(dot_board, color_board, ai_mode, step_counter)
            dot_board = tree.root.next_move.dot_board
            color_board = tree.root.next_move.color_board

            # tree.root.next_move.step
            step_record[to_string(tree.root.next_move.step)] = str(step_counter) + "," + str(
                tree.root.next_move.last_piece_type)
    else:
        if (turn == 0 and player1 == 2) or (turn == 1 and player1 == 1):
            string = input("Player 1 turn(recycle): ")
        else:
            tree = compute_best_step(dot_board, color_board, ai_mode, step_counter)
            dot_board = tree.root.next_move.dot_board
            color_board = tree.root.next_move.color_board
            step_record[to_string(tree.root.next_move.step)] = str(step_counter) + "," + str(
                tree.root.next_move.last_piece_type)
            update_record()
            # origin_pos_str = to_string(origin_pos)
    if (turn == 0 and player1 == 2) or (turn == 1 and player1 == 1):
        if string != "":
            string = string.split(" ")
            if len(string) == 4:
                if recycle is True:
                    print("You have no card, please recycle a card from the board.")
                    continue
                pos = (string[2], string[3])
                module = string[1]

                piece_pos = get_piece_position(pos, module)

                if is_valid_location(dot_board, piece_pos, module):
                    drop_piece(dot_board, color_board, piece_pos, module, step_record, step_counter)
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

                fake_dot_board = copy.deepcopy(dot_board)
                fake_color_board = copy.deepcopy(color_board)
                fake_dot_board, fake_color_board = remove_piece(fake_dot_board, fake_color_board, origin_pos)

                if is_valid_location(fake_dot_board, new_pos, new_type):
                    remove_piece(dot_board, color_board, origin_pos)
                    step_record.pop(origin_pos_str)
                    drop_piece(dot_board, color_board, new_pos, new_type, step_record, step_counter)
                else:
                    print("Please select a valid place on the board to recycle.")
                    continue
    game_over = is_game_over(dot_board, color_board, side1, side2)
    # print(string)
    print("Dot board    " + str(step_counter) + " round.   dot->1:black,2:white")
    print_board(dot_board)
    print("Color board    " + str(step_counter) + " round.   color->1:red, 2:white")
    print_board(color_board)

    if step_counter >= RECYCLE_TIME:
        recycle = True

    print(step_record)
    step_counter += 1
    turn += 1
    turn = turn % 2
