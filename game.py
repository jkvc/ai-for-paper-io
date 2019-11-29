from arena import Arena
from agent import *
from direction import *
# from observation import Observation


class Game:
    DEFAULT_MAX_TICKS = 1000
    DEFAULT_VISION_RADIUS = 3

    def __init__(
        self, height, width,
        max_ticks=DEFAULT_MAX_TICKS,
        vision_radius=DEFAULT_VISION_RADIUS
    ):
        self.arena = Arena(height, width)
        self.tick = 0
        self.max_ticks = max_ticks
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

        while self.arena.winner == None and self.tick < self.max_ticks:
            print(self.arena)
            self.tick += 1

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
    game = Game(15, 15, vision_radius=5)

    a = RandomAgent('R', arena.MIN_AGENT)
    game.add_agent(a, arena.MIN_AGENT, (10, 10), init_territory_radius=1)

    human_agent = HumanAgent('H', arena.MAX_AGENT)
    human_agent.is_god = True
    game.add_agent(human_agent, arena.MAX_AGENT,
                   (3, 3), init_territory_radius=2)

    game.run()
