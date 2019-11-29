from arena import Arena
from agent import *
from direction import *
import mini_expecti_max


class Game:
    DEFAULT_MAX_TICKS = 1000
    DEFAULT_VISION_RADIUS = 3

    def __init__(
        self, height, width,
        max_ticks=DEFAULT_MAX_TICKS,
        vision_radius=DEFAULT_VISION_RADIUS
    ):
        self.arena = Arena(height, width, max_ticks)
        self.vision_radius = vision_radius

    def add_agent(self, agent_obj, agent, pos, init_territory_radius=Arena.INITIAL_TERRITORY_RADIUS):
        '''
        add an agent to the game, add its pos to the arena
        '''
        self.arena.add_agent(agent_obj, agent, pos, init_territory_radius)

    def run(self):
        '''
        dev only, write a real game runner for production
        '''

        while not self.arena.is_end():
            print(self.arena)

            curr_agent = self.arena.curr_agent
            print(self.arena.agent_str(curr_agent), 'moving...')

            direction = self.arena.agent[curr_agent].get_move(
                self.arena.get_observable_arena(
                    curr_agent, self.vision_radius)
            )
            print(self.arena.agent_str(curr_agent),
                  'moves', Direction.tostring(direction))

            self.arena.move_agent(curr_agent, direction)

        print(self.arena)

    def __str__(self):
        s = ''
        s += 'agents: ' + str([a_ch for a_ch in self.agents]) + '\n'
        s += 'tick:' + str(self.tick) + '\n'
        s += 'vision_radius: ' + str(self.vision_radius) + '\n'
        s += str(self.arena)
        return s


if __name__ == "__main__":

    end_util = []

    for i in range(10):

        game = Game(6, 6, max_ticks=70, vision_radius=10)
        max_agent = MinimaxAgent(
            'X',
            arena.MAX_AGENT,
            mini_expecti_max.eval_builder_with_safeness,
            6
        )
        game.add_agent(max_agent, arena.MAX_AGENT,
                       (1, 1), init_territory_radius=1)

        min_agent = ExpectimaxAgent(
            'O',
            arena.MIN_AGENT,
            mini_expecti_max.eval_pure_builder,
            6
        )
        # min_agent = StationaryAgent('O', arena.MIN_AGENT)
        # min_agent = RandomAgent('O', arena.MIN_AGENT)
        game.add_agent(min_agent, arena.MIN_AGENT,
                       (4, 4), init_territory_radius=1)

        game.run()
        end_util.append(game.arena.utility())

    print(end_util)
    print(sum(end_util) / len(end_util))
