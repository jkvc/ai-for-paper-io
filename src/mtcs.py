from mctspy.games.common import TwoPlayersAbstractGameState, AbstractGameAction
from direction import *
import game
import agent
import arena


class MTCSArenaMove(AbstractGameAction):
    def __init__(self, curr_agent, direction):
        self.curr_agent = curr_agent
        self.direction = direction

    def __repr__(self):
        return f'{"MAX_AGENT" if self.curr_agent == arena.MAX_AGENT else "MIN_AGENT"}-{Direction.tostring(self.direction)}'


class MTCSArena(arena.Arena, TwoPlayersAbstractGameState):
    def __init__(self, a):
        self.a = a.get_full_arena_copy()
        self.next_to_move = a.curr_agent

    def game_result(self):
        if not self.a.is_end():
            return None

        util = self.a.utility()
        if util > 0:
            return 1
        elif util < 0:
            return -1
        else:
            return 0

    def is_game_over(self):
        return self.a.is_end()

    def is_move_legal(self, move):
        return move.curr_agent == self.a.curr_agent \
            and move.direction in self.a.get_valid_move_dirs(move.curr_agent)

    def move(self, move):
        if not self.is_move_legal(move):
            raise ValueError()

        a_copy = self.a.get_full_arena_copy()
        a_copy.move_agent(move.curr_agent, move.direction)

        return MTCSArena(a_copy)

    def get_legal_actions(self):
        return [
            MTCSArenaMove(self.a.curr_agent, direction)
            for direction in self.a.get_valid_move_dirs(self.a.curr_agent)
        ]


if __name__ == "__main__":
    g = game.Game(6, 6, 50, vision_radius=10)

    max_agent = agent.MTCSAgent('X', arena.MAX_AGENT)
    g.add_agent(max_agent, arena.MAX_AGENT, (1, 1), init_territory_radius=1)

    min_agent = agent.RandomAgent('O', arena.MIN_AGENT)
    g.add_agent(min_agent, arena.MIN_AGENT, (4, 4), init_territory_radius=1)

    max_agent.initialize_memory(g.arena)
    min_agent.initialize_memory(g.arena)

    direction = max_agent.get_move(g.arena)
    print(Direction.tostring(direction))

    print(g.arena)
