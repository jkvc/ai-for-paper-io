import curses
import arena
from direction import Direction, opposite, move
from observation import Observation
import random
import mini_expecti_max
from pprint import pprint


class Agent:
    def __init__(self, char, agent_type):
        self.char = char
        self.is_god = False
        self.agent_type = agent_type

    def get_move(self, observable):
        raise NotImplementedError()


class StationaryAgent(Agent):
    def __init__(self, char, agent_type):
        super().__init__(char, agent_type)
        self.go_up = False

    def get_move(self, observable):
        self.go_up = not self.go_up
        return Direction.UP if self.go_up else Direction.DOWN


class RandomAgent(Agent):
    def __init__(self, char, agent_type):
        super().__init__(char, agent_type)

    def get_move(self, observable):
        possible_dir = []
        self_pos = observable.pos[self.agent_type]

        for direction in Direction.ALL_DIRS:
            newpos = move(self_pos, direction)
            if observable.is_within_bounds(*newpos) and\
                    newpos not in observable.trail[self.agent_type]:
                possible_dir.append(direction)

        if len(possible_dir) == 0:
            return Direction.UP
        return random.choice(possible_dir)


class MinimaxAgent(Agent):
    def __init__(self, char, agent_type, eval_func, depth):
        super().__init__(char, agent_type)
        self.eval_func = eval_func
        self.depth = depth

    def get_move(self, observable):
        return mini_expecti_max.minimax(observable, self.depth, self.eval_func)['dir']


class ExpectimaxAgent(Agent):
    def __init__(self, char, agent_type, eval_func, depth):
        super().__init__(char, agent_type)
        self.eval_func = eval_func
        self.depth = depth

    def get_move(self, observable):
        return mini_expecti_max.expectimax(observable, self.depth, self.eval_func)['dir']


class HumanAgent(Agent):
    def __init__(self, char, agent_type, eval_func):
        super().__init__(char, agent_type)
        self.eval_func = eval_func

    def get_move(self, observable):
        observation_str = str(observable)
        print(observation_str)
        print('minimax state')
        pprint(mini_expecti_max.minimax(observable, 6, self.eval_func))

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
