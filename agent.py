import curses
import arena
from direction import Direction, opposite, move
from observation import Observation
import random
import mini_expecti_max
from pprint import pprint
import td_learn
import json
import curses


class Agent:
    def __init__(self, char, agent_type):
        self.char = char
        self.is_god = False
        self.agent_type = agent_type
        self.memory = None

    def initialize_memory(self, a):
        self.memory = a.get_full_arena_copy()

    def update_memory_from_observation(self, observation):
        adversary_agent = observation.other_agent(self.agent_type)

        self.memory.winner = observation.winner
        self.memory.remaining_ticks = observation.remaining_ticks
        self.memory.curr_agent = observation.curr_agent

        self.memory.pos[self.agent_type] = observation.pos[self.agent_type]
        if observation.pos[adversary_agent] != None:
            self.memory.pos[adversary_agent] = observation.pos[adversary_agent]

        # copy trail and territory
        self.memory.trail[self.agent_type] = \
            set(list(observation.trail[self.agent_type]))
        self.memory.territory[self.agent_type] = \
            set(list(observation.territory[self.agent_type]))

        self.memory.trail[adversary_agent] = \
            set(list(observation.trail[adversary_agent]))

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


class DepthSearchAgent(Agent):
    def __init__(self, char, agent_type, eval_func, depth):
        super().__init__(char, agent_type)
        self.eval_func = eval_func
        self.depth = depth


class MinimaxAgent(DepthSearchAgent):
    def get_move(self, observable):
        self.update_memory_from_observation(observable)
        result = mini_expecti_max.minimax(
            self.memory, self.depth, self.eval_func)
        if 'dir' not in result:
            return Direction.UP
        return result['dir']


class ExpectimaxAgent(DepthSearchAgent):
    def get_move(self, observable):
        self.update_memory_from_observation(observable)
        result = mini_expecti_max.expectimax(
            self.memory, self.depth, self.eval_func)
        if 'dir' not in result:
            return Direction.UP
        return result['dir']


class TDAgent(Agent):
    def __init__(self, char, agent_type, w, feature_extractor):
        super().__init__(char, agent_type)
        self.w = w
        self.feature_extractor = feature_extractor

    def get_move(self, observable):
        self.update_memory_from_observation(observable)
        v, direction = td_learn.get_max_value_dir(
            self.memory, self.w, self.feature_extractor)
        return direction


def get_td_agent(char, agent_type, weights_filename, feature_extractor):
    with open(weights_filename) as f:
        w = json.load(f)
    agent = TDAgent(char, agent_type, w, feature_extractor)
    return agent

# class MTCSAgent(Agent):
#     def get_move(self, observable):
#         self.update_memory_from_observation(observable)

#         root = TwoPlayersGameMonteCarloTreeSearchNode(
#             mtcs.MTCSArena(self.memory)
#         )
#         mcts = MonteCarloTreeSearch(root)
#         best_node = mcts.best_action(100)

#         print(best_node)

#         return Direction.UP


class HumanAgent(Agent):
    def __init__(self, char, agent_type, window):
        super().__init__(char, agent_type)
        self.window = window

    def get_move(self, observable):
        d = None
        while d == None:
            ch = self.window.getch()
            if ch == curses.KEY_UP:
                d = Direction.UP
            if ch == curses.KEY_DOWN:
                d = Direction.DOWN
            if ch == curses.KEY_RIGHT:
                d = Direction.RIGHT
            if ch == curses.KEY_LEFT:
                d = Direction.LEFT
        return d
