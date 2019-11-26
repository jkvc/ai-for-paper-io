from arena import Arena
from agent import *
from direction import *
from observation import Observation


class Game:
    DEFAULT_MAX_TICKS = 1000
    DEFAULT_VISION_RADIUS = 3

    def __init__(
        self, height, width,
        max_ticks=DEFAULT_MAX_TICKS,
        vision_radius=DEFAULT_VISION_RADIUS
    ):
        self.agents = {}
        self.arena = Arena(height, width)
        self.tick = 0
        self.max_ticks = max_ticks
        self.game_decided = False
        self.vision_radius = vision_radius

    def add_agent(self, agent, pos, init_territory_radius=Arena.INITIAL_TERRITORY_RADIUS):
        '''
        add an agent to the game, add its pos to the arena
        '''
        self.agents[agent.char] = agent
        self.arena.add_agent(
            agent.char, pos, init_territory_radius=init_territory_radius)

    def run(self):
        '''
        dev only, write a real game runner for production
        '''

        while not self.game_decided:
            self.tick += 1

            agents_to_kill = set()

            for agent_ch in self.agents:
                agent = self.agents[agent_ch]
                observation = self.arena.get_observation(
                    agent_ch, self.vision_radius
                )

                move_dir = agent.get_move(observation)
                to_kill = self.arena.move_agent(agent_ch, move_dir)

                agents_to_kill = agents_to_kill.union(to_kill)

            for agent_char in agents_to_kill:
                del self.agents[agent_char]
                self.arena.remove_agent(agent_char)

            if len(self.agents) <= 1:
                self.game_decided = True
                break

            if self.tick >= self.max_ticks:
                break

        print(self)
        if self.game_decided:
            for agent_ch in self.agents:
                print('Winner', agent_ch)

    def __str__(self):
        s = ''
        s += 'agents: ' + str([a_ch for a_ch in self.agents]) + '\n'
        s += 'tick:' + str(self.tick) + '\n'
        s += 'vision_radius: ' + str(self.vision_radius) + '\n'
        s += str(self.arena)
        return s


if __name__ == "__main__":
    game = Game(25, 25, vision_radius=5)

    a = StationaryAgent('S')
    game.add_agent(a, (6, 6), init_territory_radius=1)

    human_agent = HumanAgent('H')
    human_agent.game_oracle = game
    game.add_agent(human_agent, (3, 3), init_territory_radius=2)

    print(game)
    # print(game.arena.get_territory_size('H'))
    game.run()
