class Node:
    def __init__(self, id, dot_board, color_board, step, level_type, parent, grade):
        self.id = id
        self.dot_board = dot_board
        self.color_board = color_board
        self.step = step
        self.level_type = level_type
        self.parent = parent
        if parent is not None:
            self.parent_id = parent.id
        self.children = []
        self.grade = grade

    def add_child(self, child):
        self.children.append(child)
