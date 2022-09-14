from collections import deque
from time import sleep, monotonic
from contextlib import contextmanager
from heapq import heappop, heappush, heapify, heapreplace
from heapdict import heapdict

@contextmanager
def timeit():
    start = monotonic()
    yield
    end = monotonic()
    taken = end - start
    print(f'took {taken}s')

example = '''1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581'''

with open('inputs/day-15-input.txt') as input_file:
    data = input_file.read()

grid = [[int(e) for e in r] for r in data.split()]

print(grid)

def expand_grid(grid):
    new_grid = [[0] * (len(grid[0]) * 5) for _ in range(len(grid) * 5)]

    for row in range(len(grid) * 5):
        for col in range(len(grid[0]) * 5):
            for idx in range(5):
                new_grid[row][col] = grid[row % len(grid) ][col % len(grid[0])] + row // len(grid) + col // len(grid[0])
                if new_grid[row][col] > 9:
                    new_grid[row][col] -= 9

    return new_grid

class Graph:
    _directions = [
        (-1, 0),
        (0, 1),
        (1, 0),
        (0, -1),
    ]

    def __init__(self, grid):
        self._grid = grid
        self._height = len(grid)
        self._width = len(grid[0])

    def neighbours(self, p):
        x, y = p
        for dx, dy in self._directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < self._height and 0 <= ny < self._width:
                yield nx, ny

    def path_low_risk(self):
        risk_grid = [[1000000] * self._width for _ in range(self._height)]
        risk_grid[0][0] = 0
        to_visit = deque([(0,0)])

        while to_visit:
            p = to_visit.popleft()
            pr, pc = p
            for n in self.neighbours(p):
                    nr, nc = n
                    ncost = risk_grid[pr][pc] + self._grid[nr][nc]
                    if ncost < risk_grid[nr][nc]:
                        risk_grid[nr][nc] = ncost
                        to_visit.append(n)

        return risk_grid

def dijkstra(self, source, adj_list, target=None):
    if target is None:
        target = (self._height-1, self._width-1)
    
    Q = set()
    dist = {}
    prev = {}

    for state in adj_list:
        dist[state] = 1_000_000_000_000
        prev[state] = None
        Q.add(state)
    dist[source] = 0

    while Q:
        u, d = min(((v, d) for v, d in dist.items() if v in Q), key=lambda e: e[1])
        #print(u)
        Q.remove(u)
        if u == target:
            break
        for v in self.neighbours(u):
            if v in Q:
                alt = dist[u] + self._grid[v[0]][v[1]]
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u

    return dist, prev
    
    def dijkstra_prio(self, target=None):
        if target is None:
            target = (self._height-1, self._width-1)

        Q = heapdict()
        dist = {(0,0): 0}
        prev = {}

        for row in range(self._height):
            for col in range(self._width):
                if (row,col) != (0,0):
                    dist[(row,col)] = 10000000
                    prev[(row,col)] = None
                Q[(row,col)] =  dist[(row,col)]

        while Q:
            u, d = Q.popitem()

            if u == target:
                break
            for v in self.neighbours(u):
                if v in Q:
                    alt = dist[u] + self._grid[v[0]][v[1]]
                    if alt < dist[v]:
                        dist[v] = alt
                        prev[v] = u
                        Q[v] = alt
                        

        return dist, prev
print()
for r in expand_grid(grid):
    print(r)

#graph = Graph(grid)
graph = Graph(expand_grid(grid))
with timeit():
    risk = graph.path_low_risk()
# for r in risk:
#     print(r)
# with timeit():
#     dist, prev = graph.dijkstra()

with timeit():
    dist, prev = graph.dijkstra_prio()


print(dist[(len(grid)-1, len(grid[0])-1)])

