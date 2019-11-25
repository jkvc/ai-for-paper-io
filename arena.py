class Arena:
    def __init__(self, height, width, agent_pos):
        super().__init__()
        self.width = width
        self.height = height
        self.agent_trails = {
            agent: set() for agent in agent_pos
        }
        self.agent_pos = {
            **agent_pos
        }

    def update_agent_pos(self, agent, newpos):
        if newpos[0] >= self.height or newpos[1] >= self.width:
            print(
                f'[WARN] Arena:update_gent_pos: newpos {newpos} is out of arena of shape {(self.height, self.width)}')
        self.agent_pos[agent] = newpos

    def _get_char(self, row, col):
        for agent in self.agent_pos:
            if (row, col) == self.agent_pos[agent]:
                return agent
            if (row, col) in self.agent_trails[agent]:
                return agent.lower() + '*'
        return ' '

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


class Observation:
    def __init__(self):
        self.content = {}

    def add(self, observer_pos, pos, content):
        relative_pos = (
            pos[0] - observer_pos[0],
            pos[1] - observer_pos[1]
        )
        self.content[relative_pos] = content

    def shift(self, offset_row, offset_col):
        newcontent = {}
        for pos in self.content:
            newpos = (
                pos[0] + offset_row,
                pos[1] + offset_col
            )
            newcontent[newpos] = self.content[pos]
        self.content = newcontent

    def to_string(self, center_row, center_col, row_begin, row_end, col_begin, col_end):
        strlist = []

        def get_horizontal_border():
            l = ['   ']
            for col in range(col_begin, col_end + 1):
                l.append(str(col).rjust(2, '0'))
                l.append(' ')
            return ''.join(l) + '\n'

        strlist.append(get_horizontal_border())
        for row in range(row_begin, row_end + 1):
            strlist.append(f'{str(row).rjust(2, "0")} ')
            for col in range(col_begin, col_end + 1):
                ch = self.content[(row, col)] if (
                    row, col) in self.content else ' '
                strlist.append(ch)
                strlist.append('  ' if len(ch) == 1 else ' ')
            strlist.append(f' {str(row).rjust(2, "0")}\n')
        strlist.append(get_horizontal_border())

        return ''.join(strlist)


if __name__ == "__main__":
    arena = Arena(20, 20, {'A': (1, 1), 'B': (8, 8), 'X': (0, 0)})
    arena.update_agent_pos('B', (19, 19))
    arena.agent_trails['A'].add((1, 2))
    print(arena)

    o = Observation()
    o.add((1, 1), (1, 1), 'A')
    o.add((1, 1), (1, 2), 'a*')
    o.add((1, 1), (0, 0), 'X')
    print(o.to_string(1, 1, -1, 1, -1, 1))

    o.shift(1, 1)
    print(o.to_string(1, 1, -2, 2, -2, 2))
