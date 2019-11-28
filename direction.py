class Direction:
    LEFT = (0, -1)
    RIGHT = (0, 1)
    UP = (-1, 0)
    DOWN = (1, 0)
    ALL_DIRS = [LEFT, RIGHT, UP, DOWN]

    @staticmethod
    def tostring(direction):
        d = {
            Direction.LEFT: 'LEFT',
            Direction.RIGHT: 'RIGHT',
            Direction.UP: 'UP',
            Direction.DOWN: 'DOWN',
        }
        return d[direction]


def move(pos, direction):
    return (pos[0] + direction[0], pos[1] + direction[1])


def opposite(direction):
    d = {
        Direction.LEFT: Direction.RIGHT,
        Direction.RIGHT: Direction.LEFT,
        Direction.UP: Direction.DOWN,
        Direction.DOWN: Direction.UP
    }
    return d[direction]
