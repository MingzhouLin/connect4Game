class Node:
    def __init__(self, id, dot_board, color_board, step, level, level_type, parent, grade, last_piece_type,step_record):
        self.id = id

        self.dot_board = dot_board
        self.color_board = color_board
        self.step = step
        self.level_type = level_type
        self.level = level
        self.parent = parent
        if parent is not None:
            self.parent_id = parent.id
        self.children = []
        self.grade = grade
        # next_move: record the optimal move for next level
        self.next_move = None
        self.step_record = step_record
        #record the last piece dropped from last level.

        self.last_piece_type = last_piece_type
        self.removed_piece = None
    def add_child(self, child):
        self.children.append(child)
