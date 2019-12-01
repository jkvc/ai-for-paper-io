from agent import *
from direction import *
import mini_expecti_max
import arena
import td_learn


class Game:
    DEFAULT_MAX_TICKS = 1000
    DEFAULT_VISION_RADIUS = 3

    def __init__(
        self, height, width,
        max_ticks=DEFAULT_MAX_TICKS,
        vision_radius=DEFAULT_VISION_RADIUS
    ):
        self.arena = arena.Arena(height, width, max_ticks)
        self.vision_radius = vision_radius
        self.is_initialized = False
        self.history = []

    def initialize(self):
        for agent in [arena.MIN_AGENT, arena.MAX_AGENT]:
            agent_obj = self.arena.agent[agent]
            agent_obj.initialize_memory(self.arena)
        self.is_initialized = True

    def add_agent(self, agent_obj, agent, pos,
                  init_territory_radius):
        '''
        add an agent to the game, add its pos to the arena
        '''
        self.arena.add_agent(agent_obj, agent, pos, init_territory_radius)

    def run(self, quiet=False):
        '''
        dev only, write a real game runner for production
        '''

        if not self.is_initialized:
            self.initialize()

        while not self.arena.is_end():
            self.history.append(self.arena.get_full_arena_copy())

            if not quiet:
                print('\n[God view]')
                print(self.arena)

            curr_agent = self.arena.curr_agent
            if not quiet:
                print('>', self.arena.agent_str(curr_agent), 'moving...')

            direction = self.arena.agent[curr_agent].get_move(
                self.arena.get_observable_arena(
                    curr_agent, self.vision_radius)
            )
            if not quiet:
                print('>', self.arena.agent_str(curr_agent),
                      'moves', Direction.tostring(direction))

            self.arena.move_agent(curr_agent, direction)

        self.history.append(self.arena.get_full_arena_copy())
        if not quiet:
            print(self.arena)
            print(self.arena.utility())

    def __str__(self):
        s = ''
        s += 'agents: ' + str([a_ch for a_ch in self.agents]) + '\n'
        s += 'tick:' + str(self.tick) + '\n'
        s += 'vision_radius: ' + str(self.vision_radius) + '\n'
        s += str(self.arena)
        return s


if __name__ == "__main__":

    outcomes = []

    for i in range(300):
        print('Running game', i)

        game = Game(6, 6, max_ticks=50, vision_radius=1)
        # max_agent = ExpectimaxAgent(
        #     'X',
        #     arena.MAX_AGENT,
        #     mini_expecti_max.eval_pure_builder,
        #     4
        # )
        max_agent = get_td_agent('X', arena.MAX_AGENT,
                                 'td_train_output/td_minimax_4_pure.json',
                                 td_learn.dist_features)
        game.add_agent(max_agent, arena.MAX_AGENT,
                       (1, 1), init_territory_radius=1)

        min_agent = ExpectimaxAgent(
            'O',
            arena.MIN_AGENT,
            mini_expecti_max.eval_pure_builder,
            2
        )
        # min_agent = StationaryAgent('O', arena.MIN_AGENT)
        # min_agent = RandomAgent('O', arena.MIN_AGENT)
        game.add_agent(min_agent, arena.MIN_AGENT,
                       (4, 4), init_territory_radius=1)

        game.run(quiet=True)
        outcomes.append(game.arena.utility())

    print(outcomes)
    print('expected outcome', sum(outcomes) / len(outcomes))
