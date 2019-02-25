class Node:
    def __init__(self, id, dot_board, color_board, step, level_type, parent, grade, is_leaf, last_piece_pos, last_piece_type):
        self.id = id

        self.dot_board = dot_board
        self.color_board = color_board
        self.step = step
        self.level_type = level_type
        self.parent = parent
        self.is_leaf = is_leaf
        if parent is not None:
            self.parent_id = parent.id
        self.children = []
        self.grade = grade
        # next_move: record the optimal move for next level
        self.next_move = None
        #record the last piece dropped from last level.
        self.last_piece_pos = last_piece_pos
        self.last_piece_type = last_piece_type
    def add_child(self, child):
        self.children.append(child)
