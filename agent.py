import curses
import arena
from direction import Direction, opposite, move
from observation import Observation
import random
import minimax
from pprint import pformat


class Agent:
    def __init__(self, char):
        self.char = char
        self.is_god = False

    def get_move(self, observable, self_agent_type):
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

    def get_move(self, observable):
        self.go_up = not self.go_up
        return Direction.UP if self.go_up else Direction.DOWN


class RandomAgent(Agent):
    def __init__(self, char):
        super().__init__(char)

    def get_move(self, observable, self_agent_type):
        possible_dir = []
        self_pos = observable.pos[self_agent_type]

        for direction in Direction.ALL_DIRS:
            newpos = move(self_pos, direction)
            if observable.is_within_bounds(*newpos) and\
                    newpos not in observable.trail[self_agent_type]:
                possible_dir.append(direction)

        if len(possible_dir) == 0:
            return Direction.UP
        return random.choice(possible_dir)


class HumanAgent(Agent):
    def __init__(self, char):
        super().__init__(char)

    def get_move(self, observable, self_agent_type):
        observation_str = str(observable)
        print(observation_str)

        # agent_list = []
        # for ch in observable.agent_pos:
        #     if ch != self.char:
        #         agent_list.append(ch)
        # agent_list.append(self.char)

        # for direction in Direction.ALL_DIRS:
        #     # print(Direction.tostring(direction))

        #     arena_copy = observable.get_full_arena_copy()
        #     arena_copy.move_agent(self.char, direction)
        #     factors = minimax.minimax(
        #         agent_list, 0,
        #         arena_copy, minimax.eval_naive_builder,
        #         1
        #     )

        # factors_str = pformat(factors, 2)
        # print(factors_str)

        print('Use arrow keys to move... ')

        direction = None
        while direction == None:
            ch = input()
            if ch == 'w':
                direction = Direction.UP
            if ch == 's':
                direction = Direction.DOWN
            if ch == 'a':
                direction = Direction.LEFT
            if ch == 'd':
                direction = Direction.RIGHT

        return direction
