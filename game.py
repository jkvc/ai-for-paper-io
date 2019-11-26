from arena import *
from agent import *


class Game:
    DEFAULT_NUM_TICKS = 1000
    DEFAULT_VISION_RADIUS = 3

    def __init__(
        self, height, width,
        num_ticks=DEFAULT_NUM_TICKS,
        vision_radius=DEFAULT_VISION_RADIUS
    ):
        self.agents = {}
        self.arena = Arena(height, width)
        self.tick = 0
        self.num_ticks = num_ticks
        self.game_ended = False
        self.vision_radius = vision_radius

    def add_agent(self, agent, pos):
        self.agents[agent.char] = agent
        self.arena.add_agent(agent.char, pos)

    def run(self):
        while not self.game_ended:
            self.tick += 1
            for agent_ch in self.agents:
                agent = self.agents[agent_ch]
                observation = self.arena.get_observation(
                    agent_ch, self.vision_radius
                )

                print(
                    f'Getting input from agent {agent_ch}...'
                )
                move_dir = agent.get_move(observation)
                self.arena.move_agent(agent_ch, move_dir)

    def __str__(self):
        s = 'Game: \n'
        s += 'agents: ' + str([a_ch for a_ch in self.agents]) + '\n'
        s += 'tick:' + str(self.tick) + '\n'
        s += 'vision_radius: ' + str(self.vision_radius) + '\n'
        s += str(self.arena)
        return s


if __name__ == "__main__":
    game = Game(20, 20)
    human_agent = HumanAgent('H')
    human_agent.game_oracle = game
    game.add_agent(human_agent, (3, 3))

    print(game)
    game.run()
