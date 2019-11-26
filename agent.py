import curses


class Direction:
    LEFT = (0, -1)
    RIGHT = (0, 1)
    UP = (-1, 0)
    DOWN = (1, 0)


def move(pos, direction):
    return (pos[0] + direction[0], pos[1] + direction[1])


class Agent:
    def __init__(self, char):
        self.char = char

    def get_move(self, observation):
        raise NotImplementedError()


class HumanAgent(Agent):
    def __init__(self, char):
        super().__init__(char)
        self.game_oracle = None

    def get_move(self, observation):
        screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        screen.keypad(True)

        # add stuff to the screen
        vertical_offset = 0
        if self.game_oracle != None:
            oracle_str = str(self.game_oracle)
            screen.addstr(0, 0, oracle_str)
            vertical_offset += oracle_str.count('\n') + 1

        screen.addstr(
            vertical_offset, 0,
            f"Observation of agent {self.char}: ")
        vertical_offset += 2

        observation_str = str(observation)
        screen.addstr(vertical_offset, 0, observation_str)
        vertical_offset += observation_str.count('\n') + 1

        screen.addstr(vertical_offset, 0, 'Use arrow keys to move... ')

        # ask for direction input
        direction = None
        try:
            while direction == None:
                ch = screen.getch()
                if ch == curses.KEY_UP:
                    direction = Direction.UP
                if ch == curses.KEY_DOWN:
                    direction = Direction.DOWN
                if ch == curses.KEY_LEFT:
                    direction = Direction.LEFT
                if ch == curses.KEY_RIGHT:
                    direction = Direction.RIGHT
        finally:
            curses.nocbreak()
            screen.keypad(0)
            curses.echo()
            curses.endwin()

        return direction
