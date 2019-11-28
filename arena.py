from agent import Agent
from direction import *
from observation import Observation


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
        self.dead_agents = set()

    def add_agent(self, agent_char, pos,
                  init_territory_radius=INITIAL_TERRITORY_RADIUS):
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
        for row in range(agent_row-init_territory_radius, agent_row+init_territory_radius+1):
            for col in range(agent_col-init_territory_radius, agent_col+init_territory_radius+1):
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

    def remove_agent(self, agent_char):
        '''
        - remove an agent from the arena
        - this should be called when an agent is killed
        '''
        del self.agent_pos[agent_char]
        del self.agent_territory[agent_char]
        del self.agent_trails[agent_char]

    def move_agent(self, agent_char, direction):
        '''
        - move agent to a new position
        - if enclosure completed, trail -> territory, any enclosed territory flooded
        - return a list of agents that died as a result of this move
        '''

        oldpos = self.agent_pos[agent_char]
        newpos = move(oldpos, direction)
        if oldpos not in self.agent_territory[agent_char]:
            self.agent_trails[agent_char].add(oldpos)
        self.update_agent_pos(agent_char, newpos)

        new_territory = self.complete_enclosure_if_any(agent_char)

        # remove territory from other agents
        if len(new_territory) != 0:
            for other_agent_char in self.agent_territory:
                if other_agent_char == agent_char:
                    continue
                self.agent_territory[other_agent_char] =\
                    self.agent_territory[other_agent_char].difference(
                        new_territory)

        agents_to_kill = set()
        for other_agent_char in self.agent_territory:
            # kill an agent by stepping on their trail, you can get yourself killed
            if newpos in self.agent_trails[other_agent_char]:
                agents_to_kill.add(other_agent_char)
            # kill an agent by encircling it
            if other_agent_char != agent_char:
                if self.agent_pos[other_agent_char] in new_territory:
                    agents_to_kill.add(other_agent_char)

        for dead_agent in agents_to_kill:
            self.dead_agents.add(dead_agent)

        return agents_to_kill

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

    def is_within_bounds(self, row, col):
        return row >= 0 and row < self.height and col >= 0 and col < self.width

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
                return Agent.get_trail_char(agent_char)
        for agent_char in self.agent_pos:
            if (row, col) in self.agent_territory[agent_char]:
                return Agent.get_territory_char(agent_char)
        return ' '

    def get_arena_copy(self, min_row, max_row, min_col, max_col, agent_char=None):
        def is_in_range(row, col):
            return row >= min_row and row <= max_row and col >= min_col and col <= max_col

        arena_copy = Arena(self.height, self.width)

        for agent_ch in self.agent_pos:
            row, col = self.agent_pos[agent_ch]
            arena_copy.agent_pos[agent_ch] = (
                row, col) if is_in_range(row, col) else None

            arena_copy.agent_territory[agent_ch] = set()
            arena_copy.agent_trails[agent_ch] = set()

            for row, col in self.agent_territory[agent_ch]:
                if is_in_range(row, col) or agent_ch == agent_char:
                    arena_copy.agent_territory[agent_ch].add((row, col))

            for row, col in self.agent_trails[agent_ch]:
                if is_in_range(row, col) or agent_ch == agent_char:
                    arena_copy.agent_trails[agent_ch].add((row, col))

        return arena_copy

    def get_full_arena_copy(self):
        return self.get_arena_copy(
            0, self.height-1, 0, self.width-1
        )

    def get_observable_arena(self, agent, radius):
        '''
        - return an observation of the agent, of observation radius
        '''

        if agent not in self.agent_pos:
            print(
                f'[WARN] Arena.get_observable_arena: agent {agent} not in arena. Returning None.'
            )
            return None

        agentpos = self.agent_pos[agent]
        agent_row, agent_col = agentpos
        minrow = agent_row - radius
        maxrow = agent_row + radius
        mincol = agent_col - radius
        maxcol = agent_col + radius

        return self.get_arena_copy(minrow, maxrow, mincol, maxcol, agent_char=agent)

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
