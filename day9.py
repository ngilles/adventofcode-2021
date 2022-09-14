
from collections import defaultdict, deque

example = '''2199943210
3987894921
9856789892
8767896789
9899965678'''

with open('inputs/day-9-input.txt') as input_file:
    data = input_file.read()

class Grid:
    _directions = [
        (-1, 0),
        (0, 1),
        (1, 0),
        (0, -1),
    ]

    def __init__(self, data):
        self._height = len(data)
        self._width = len(data[0])
        self._data = data


    def neighbours(self, p):
        x, y = p
        for dx, dy in self._directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < self._height and 0 <= ny < self._width:
                yield nx, ny

    def value(self, p):
        x, y = p
        return self._data[x][y]

    def low_points(self):
        for x in range(self._height):
            for y in range(self._width):
                v = self.value((x, y))
                if all(v < self.value((nx,ny)) for nx, ny in self.neighbours((x,y))):
                    yield x, y
        
    def find_basins(self):
        seen = set()
        basins = defaultdict(set)
        current_basin = 0

        for x in range(self._height):
            for y in range(self._width):
                p = (x, y)
                v = self.value(p)
                if p not in seen and v != 9:
                    needs_visit = deque()
                    needs_visit.append(p)

                    while needs_visit:
                        vp = needs_visit.popleft()
                        basins[current_basin].add(vp)
                        seen.add(vp)

                        for np in self.neighbours(vp):
                            if np not in seen and np not in needs_visit and self.value(np) != 9:
                                needs_visit.append(np)

                    current_basin += 1

        return basins
                        
    
grid = Grid([[int(n) for n in r] for r in data.split()])
print(sum(1+ grid.value(p) for p in grid.low_points()))

basins = grid.find_basins()
basins_sizes = [len(v) for v in basins.values()]
basins_sizes.sort()
print(basins_sizes[-3:])


