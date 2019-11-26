from agent import *
from direction import *
from observation import *


class Arena:
    WALL_CHAR = 'X'
    INITIAL_TERRITORY_RADIUS = 1

    def __init__(self, height, width):
        super().__init__()
        self.width = width
        self.height = height
        self.agent_pos = {}
        self.agent_territory = {}
        self.agent_trails = {}

    def add_agent(self, agent_char, pos):
        '''
        - add an agent to the arena,
        - add an initial territory around the agent
        - agent_char: one char repr of the agent
        - pos: initial position of the agent
        '''

        if agent_char in self.agent_pos:
            print(
                f'[WARN] Arena.add_agent: {agent_char} already exists in arena, overwriting.'
            )
        self.agent_trails[agent_char] = set()

        # populate initial territory around new agent
        self.agent_territory[agent_char] = set()
        agent_row, agent_col = pos
        for row in range(agent_row-Arena.INITIAL_TERRITORY_RADIUS, agent_row+Arena.INITIAL_TERRITORY_RADIUS+1):
            for col in range(agent_col-Arena.INITIAL_TERRITORY_RADIUS, agent_col+Arena.INITIAL_TERRITORY_RADIUS+1):
                self.agent_territory[agent_char].add((row, col))

        # add its position
        self.update_agent_pos(agent_char, pos)

    def update_agent_pos(self, agent_char, newpos):
        '''
        - update agent to a new position
        - if agent does not exist, add it
        '''

        if newpos[0] >= self.height or newpos[1] >= self.width:
            print(
                f'[WARN] Arena:update_gent_pos: newpos {newpos} is out of arena of shape {(self.height, self.width)}')
        self.agent_pos[agent_char] = newpos

    def move_agent(self, agent_char, direction):
        '''
        - move agent to a new position
        - if enclosure completed, trail -> territory, any enclosed territory flooded
        '''

        oldpos = self.agent_pos[agent_char]
        newpos = move(oldpos, direction)
        if oldpos not in self.agent_territory[agent_char]:
            self.agent_trails[agent_char].add(oldpos)
        self.update_agent_pos(agent_char, newpos)

        self.complete_enclosure_if_any(agent_char)

    def complete_enclosure_if_any(self, agent_char):
        '''
        - iterate over empty spaces
        - if space in an enclosed territory of `agent_char`, flood it to become the agents 
        territory
        - return the set of new territory
        '''

        # if enclosure not completed, no new territory
        if self.agent_pos[agent_char] not in self.agent_territory[agent_char] \
                or len(self.agent_trails[agent_char]) == 0:
            return set()

        new_territory = set()

        # trail becomes territory
        new_territory = new_territory.union(self.agent_trails[agent_char])
        self.agent_territory[agent_char] =\
            self.agent_territory[agent_char].union(
                self.agent_trails[agent_char])
        self.agent_trails[agent_char] = set()

        def flood(row, col):
            '''
            return (set, leaked)
            where the set is a set of explored spaces
            leaked is a bool denoted whether the flood exceeded the arena bounds
            '''

            to_fill = set()
            touched = set()
            queue = [(row, col)]
            leaked = False
            while queue:
                row, col = queue.pop(0)
                if (row, col) in touched:
                    continue
                touched.add((row, col))

                if row < 0 or col < 0 or row >= self.height or col >= self.width:
                    leaked = True
                    continue
                if (row, col) in self.agent_territory[agent_char]:
                    continue

                to_fill.add((row, col))
                queue.extend([
                    (row, col+1),
                    (row, col-1),
                    (row+1, col),
                    (row-1, col),
                ])

            return to_fill, leaked

        # attempt to flood any enclosed region
        explored = set()
        for row in range(self.height):
            for col in range(self.width):
                if (row, col) in explored:
                    continue
                explored.add((row, col))

                to_fill, leaked = flood(row, col)
                explored = explored.union(to_fill)
                if not leaked:
                    new_territory = new_territory.union(to_fill)
                    self.agent_territory[agent_char] = \
                        self.agent_territory[agent_char].union(to_fill)

        return new_territory

    def _get_trail_char(self, agent_char):
        return agent_char.lower() + '*'

    def _get_char(self, row, col):
        if row < 0 or col < 0 or row >= self.height or col >= self.width:
            return Arena.WALL_CHAR
        for agent_char in self.agent_pos:
            if (row, col) == self.agent_pos[agent_char]:
                return agent_char
        for agent_char in self.agent_pos:
            if (row, col) in self.agent_trails[agent_char]:
                return agent_char.lower() + '*'
        for agent_char in self.agent_pos:
            if (row, col) in self.agent_territory[agent_char]:
                return agent_char.lower()
        return ' '

    def get_observation(self, agent, radius):
        '''
        - return an observation of the agent, of observation radius
        '''

        if agent not in self.agent_pos:
            print(
                f'[WARN] Arena.get_observation: agent {agent} not in arena. Returning empty observation.'
            )
            return Observation(0)

        agentpos = self.agent_pos[agent]
        agent_row, agent_col = agentpos
        minrow = agent_row - radius
        maxrow = agent_row + radius
        mincol = agent_col - radius
        maxcol = agent_col + radius
        observation = Observation(radius)

        for row in range(minrow, maxrow + 1):
            for col in range(mincol, maxcol + 1):
                observation.add(agentpos, (row, col), self._get_char(row, col))
        return observation

    def get_territory_size(self, agent_ch):
        return len(self.agent_territory[agent_ch])

    def __str__(self):
        strlist = []

        def get_horizontal_border():
            l = ['   ']
            for col in range(self.width):
                l.append(str(col).rjust(2, '0'))
                l.append(' ')
            return ''.join(l) + '\n'

        strlist.append(get_horizontal_border())
        for row in range(self.height):
            strlist.append(f'{str(row).rjust(2, "0")} ')
            for col in range(self.width):
                ch = self._get_char(row, col)
                strlist.append(ch)
                strlist.append('  ' if len(ch) == 1 else ' ')
            strlist.append(f' {str(row).rjust(2, "0")}\n')
        strlist.append(get_horizontal_border())

        return ''.join(strlist)


if __name__ == "__main__":
    arena = Arena(20, 20)
    arena.add_agent('A', (1, 1))
    arena.add_agent('B', (8, 8))
    arena.add_agent('N', (5, 5))

    arena.update_agent_pos('B', (19, 19))
    arena.agent_trails['A'].add((1, 2))

    print(arena)

    print(arena.get_observation('A', 2))
    print(arena.get_observation('B', 2))
    print(arena.get_observation('N', 6))
    print(arena.get_observation('C', 2))
