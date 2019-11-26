import curses
import arena
from direction import Direction
from observation import Observation
import random


class Agent:
    def __init__(self, char):
        self.char = char

    def get_move(self, observation):
        raise NotImplementedError()

    @staticmethod
    def get_trail_char(agent_char):
        return agent_char.lower() + '*'

    @staticmethod
    def get_territory_char(agent_char):
        return agent_char.lower()


class StationaryAgent(Agent):
    def __init__(self, char):
        super().__init__(char)
        self.go_up = False

    def get_move(self, observation):
        self.go_up = not self.go_up
        return Direction.UP if self.go_up else Direction.DOWN


class RandomAgent(Agent):
    def __init__(self, char):
        super().__init__(char)

    def get_move(self, observation):
        possible_dir = []
        for direction in Direction.ALL_DIRS:
            if observation.content[direction] not in \
                    [Agent.get_trail_char(self.char), arena.Arena.WALL_CHAR]:
                possible_dir.append(direction)
        if len(possible_dir) == 0:
            return Direction.UP
        return random.choice(possible_dir)


class HumanAgent(Agent):
    def __init__(self, char):
        super().__init__(char)
        self.game_oracle = None

    def get_move(self, observation):
        screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        screen.keypad(True)
        screen.clear()

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
