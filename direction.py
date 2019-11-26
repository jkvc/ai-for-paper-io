class Direction:
    LEFT = (0, -1)
    RIGHT = (0, 1)
    UP = (-1, 0)
    DOWN = (1, 0)
    ALL_DIRS = [LEFT, RIGHT, UP, DOWN]


def move(pos, direction):
    return (pos[0] + direction[0], pos[1] + direction[1])
