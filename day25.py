with open('inputs/day-25-input.txt') as input_file:
    data = input_file.read()

example = '''v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>'''

example1 = '''...>>>>>...'''

example2 = '''..........
.>v....v..
.......>..
..........'''

example3 = '''...>...
.......
......>
v.....>
......>
.......
..vvv..'''


class CucumberPatch:
    def __init__(self, grid):
        self.cucumbers = {}
        self.height = len(grid)
        self.width = len(grid[0])
        self.moves = 0

        for r in range(self.height):
            for c in range(self.width):
                if grid[r][c] != '.':
                    self.cucumbers[(r,c)] = grid[r][c]


    def step(self):
        east_movers = [
            (r, c)
            for (r, c), t in self.cucumbers.items()
            if t == '>' and (r, (c+1) % self.width) not in self.cucumbers
        ]

        for (r, c) in east_movers:
            del self.cucumbers[(r,c)]
            self.cucumbers[(r, (c+1) % self.width)] = '>'

        south_movers = [
            (r, c)
            for (r, c), t in self.cucumbers.items()
            if t == 'v' and ((r+1) % self.height, c) not in self.cucumbers
        ]

        for (r, c) in south_movers:
            del self.cucumbers[(r,c)]
            self.cucumbers[((r+1) % self.height, c)] = 'v'

        self.moves += 1
        return len(east_movers) + len(south_movers)

    def print(self):
        grid = [['.'] * self.width for _ in range(self.height)]

        for (r, c), t in self.cucumbers.items():
            grid[r][c] = t

        for row in grid:
            print(''.join(row))
        print()

print('--- raw data ---')
print(data)
print('--- raw data ---')

CP = CucumberPatch([[c for c in line] for line in data.split('\n')])

CP.print()

while CP.step():
    pass

print(CP.moves)