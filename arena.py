import agent
from direction import *
# from observation import Observation

MAX_AGENT = 0
MIN_AGENT = 1


class Arena:
    WALL_CHAR = 'X'
    INITIAL_TERRITORY_RADIUS = 1

    def __init__(self, height, width):
        super().__init__()
        self.width = width
        self.height = height

        self.agent = [None, None]
        self.pos = [None, None]
        self.trail = [set(), set()]
        self.territory = [set(), set()]
        self.curr_agent = MAX_AGENT

        self.winner = None

    def add_agent(self, agent_obj, agent, pos,
                  init_territory_radius=INITIAL_TERRITORY_RADIUS):
        '''
        - add an agent to the arena,
        - add an initial territory around the agent
        - agent_char: one char repr of the agent
        - pos: initial position of the agent
        '''

        self.pos[agent] = pos
        self.agent[agent] = agent_obj

        agent_row, agent_col = pos
        for row in range(agent_row-init_territory_radius, agent_row+init_territory_radius+1):
            for col in range(agent_col-init_territory_radius, agent_col+init_territory_radius+1):
                self.territory[agent].add((row, col))

    def other_agent(self, agent):
        return (agent + 1) % 2

    def move_agent(self, agent, direction):
        '''
        - move agent to a new position
        - if enclosure completed, trail -> territory, any enclosed territory flooded
        - return a list of agents that died as a result of this move
        '''
        if agent != self.curr_agent:
            print(
                '[WARN] Arena.move_agent, moving agent is not consistent with self.curr_agent')
        self.curr_agent = self.other_agent(agent)

        oldpos = self.pos[agent]
        newpos = move(oldpos, direction)
        if oldpos not in self.territory[agent]:
            self.trail[agent].add(oldpos)

        self.pos[agent] = newpos

        new_territory = self.complete_enclosure_if_any(agent)
        other_agent = self.other_agent(agent)

        # remove territory from other agents
        if len(new_territory) != 0:
            self.territory[other_agent] =\
                self.territory[other_agent].difference(new_territory)

        # if we step on the other agents trail, win
        if newpos in self.trail[other_agent]:
            self.win(agent)
            return
        # if we enclose other agent completely, win
        if self.pos[other_agent] in new_territory:
            self.win(agent)
            return

    def win(self, agent):
        self.winner = agent

    def complete_enclosure_if_any(self, agent):
        '''
        - iterate over empty spaces
        - if space in an enclosed territory of `agent_char`, flood it to become the agents 
        territory
        - return the set of new territory
        '''

        # if enclosure not completed, no new territory
        if self.pos[agent] not in self.territory[agent] \
                or len(self.trail[agent]) == 0:
            return set()

        new_territory = set()

        # trail becomes territory
        new_territory = new_territory.union(self.trail[agent])
        self.territory[agent] =\
            self.territory[agent].union(
                self.trail[agent])
        self.trail[agent] = set()

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
                if (row, col) in self.territory[agent]:
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
                    self.territory[agent] = \
                        self.territory[agent].union(to_fill)

        return new_territory

    def is_within_bounds(self, row, col):
        return row >= 0 and row < self.height and col >= 0 and col < self.width

    def _get_trail_char(self, agent_char):
        return agent_char.lower() + '*'

    def _get_char(self, row, col):
        if row < 0 or col < 0 or row >= self.height or col >= self.width:
            return Arena.WALL_CHAR

        pos = (row, col)

        if pos == self.pos[MAX_AGENT]:
            return self.agent[MAX_AGENT].char
        if pos == self.pos[MIN_AGENT]:
            return self.agent[MIN_AGENT].char

        if pos in self.trail[MAX_AGENT]:
            return agent.Agent.get_trail_char(self.agent[MAX_AGENT].char)
        if pos in self.trail[MIN_AGENT]:
            return agent.Agent.get_trail_char(self.agent[MIN_AGENT].char)

        if pos in self.territory[MAX_AGENT]:
            return agent.Agent.get_territory_char(self.agent[MAX_AGENT].char)
        if pos in self.territory[MIN_AGENT]:
            return agent.Agent.get_territory_char(self.agent[MIN_AGENT].char)

        return ' '

    def get_arena_copy(self, min_row, max_row, min_col, max_col, agent):
        def is_in_range(row, col):
            return row >= min_row and row <= max_row and col >= min_col and col <= max_col

        arena_copy = Arena(self.height, self.width)

        arena_copy.curr_agent = self.curr_agent
        arena_copy.winner = self.winner
        arena_copy.agent = [*self.agent]

        arena_copy.pos[agent] = self.pos[agent]
        arena_copy.trail[agent] = set(list(self.trail[agent]))
        arena_copy.territory[agent] = set(list(self.territory[agent]))

        other_agent = self.other_agent(agent)
        for row, col in self.territory[other_agent]:
            if is_in_range(row, col):
                arena_copy.territory[other_agent].add((row, col))
        for row, col in self.trail[other_agent]:
            if is_in_range(row, col):
                arena_copy.trail[other_agent].add((row, col))

        return arena_copy

    def get_full_arena_copy(self):
        return self.get_arena_copy(
            0, self.height-1, 0, self.width-1, MAX_AGENT
        )

    def get_observable_arena(self, agent, radius):
        '''
        - return an observation of the agent, of observation radius
        '''

        agentpos = self.pos[agent]
        agent_row, agent_col = agentpos
        minrow = agent_row - radius
        maxrow = agent_row + radius
        mincol = agent_col - radius
        maxcol = agent_col + radius

        return self.get_arena_copy(minrow, maxrow, mincol, maxcol, agent)

    def get_territory_size(self, agent):
        return len(self.territory[agent])

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

        strlist.append(
            f'curr_agent: {"MAX_AGENT" if self.curr_agent == MAX_AGENT else "MIN_AGENT"} \n')
        strlist.append(
            f'winner: {self.winner} \n')

        return ''.join(strlist)


if __name__ == "__main__":
    arena = Arena(20, 20)
    arena.add_agent(agent.RandomAgent('A'), MAX_AGENT, (1, 1))
    arena.add_agent(agent.RandomAgent('B'), MIN_AGENT, (8, 8))

    print(arena)

    c = arena.get_full_arena_copy()
    print(c)

    o = arena.get_observable_arena(MAX_AGENT, 3)
    print(o)
    o = arena.get_observable_arena(MIN_AGENT, 10)
    print(o)
