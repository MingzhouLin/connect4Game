class Node:
    def __init__(self, dot_board, color_board, step, level_type, parent, grade):
        self.dot_board = dot_board
        self.color_board = color_board
        self.step = step
        self.level_type = level_type
        self.parent = parent
        self.children = []
        self.grade = grade

    def add_child(self, child):
        self.children.append(child)
