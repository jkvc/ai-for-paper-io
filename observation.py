class Observation:
    def __init__(self, radius):
        self.content = {}
        self.radius = radius

    def add(self, observer_pos, pos, content):
        relative_pos = (
            pos[0] - observer_pos[0],
            pos[1] - observer_pos[1]
        )
        self.add_relative(relative_pos, content)

    def add_relative(self, relative_pos, content):
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

    def update_memory(self, new_observation):
        for row in range(-new_observation.radius, new_observation.radius + 1):
            for col in range(-new_observation.radius, new_observation.radius + 1):
                if (row, col) not in new_observation.content:
                    if (row, col) in self.content:
                        del self.content[(row, col)]
                else:
                    self.content[(row, col)] = \
                        new_observation.content[(row, col)]

    def to_string_full(self):
        rowidx = []
        colidx = []
        for (row, col) in self.content:
            rowidx.append(row)
            colidx.append(col)
        minrow = min(rowidx)
        maxrow = max(rowidx)
        mincol = min(colidx)
        maxcol = max(colidx)
        return self.to_string(minrow, maxrow, mincol, maxcol)

    def to_string(self, min_row, max_row, min_col, max_col):
        strlist = []

        def get_horizontal_border():
            l = ['   ']
            for col in range(min_col, max_col+1):
                l.append(str(col).rjust(2, '0'))
                l.append(' ')
            return ''.join(l) + '\n'

        strlist.append(get_horizontal_border())
        for row in range(min_row, max_row+1):
            strlist.append(f'{str(row).rjust(2, "0")} ')
            for col in range(min_col, max_col+1):
                ch = self.content[(row, col)] if (
                    row, col) in self.content else ' '
                strlist.append(ch)
                strlist.append('  ' if len(ch) == 1 else ' ')
            strlist.append(f' {str(row).rjust(2, "0")}\n')
        strlist.append(get_horizontal_border())

        return ''.join(strlist)

    def __str__(self):
        return self.to_string(-self.radius, self.radius, -self.radius, self.radius)


if __name__ == "__main__":
    o = Observation(1)
    o.add_relative((0, 0), 'A')
    o.add_relative((0, 1), 'a*')
    o.add_relative((1, 1), 'b*')
    print('old')
    print(o)

    o.shift(0, 1)
    print('old shifted')
    print(o)

    new_observation = Observation(1)
    new_observation.add_relative((0, 0), 'A')
    new_observation.add_relative((0, 1), 'a*')
    print('new')
    print(new_observation)

    o.update_memory(new_observation)
    print('old updated')
    print(o.to_string_full())
