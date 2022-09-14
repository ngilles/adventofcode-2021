from collections import defaultdict, deque
from typing import Set, Tuple, Dict
from orderedset import OrderedSet

from heapdict import heapdict

example = (
    '#############' '\n'
    '#...........#' '\n'
    '###B#C#B#D###' '\n'
    '  #D#C#B#A#  ' '\n'
    '  #D#B#A#C#  ' '\n'
    '  #A#D#C#A#  ' '\n'
    '  #########  '
)

data = '''#############
#...........#
###C#A#D#D###
  #B#A#B#C#
  #########'''

data2 = '''#############
#...........#
###C#A#D#D###
  #D#C#B#A#  
  #D#B#A#C#  
  #B#A#B#C#  
  #########'''

maze = data2.split('\n')

def print_state(state):
    grid = [
        ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
        ['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
        ['#', '#', '#', '.', '#', '.', '#', '.', '#', '.', '#', '#', '#'],
        [' ', ' ', '#', '.', '#', '.', '#', '.', '#', '.', '#', ' ', ' '],
        [' ', ' ', '#', '.', '#', '.', '#', '.', '#', '.', '#', ' ', ' '],
        [' ', ' ', '#', '.', '#', '.', '#', '.', '#', '.', '#', ' ', ' '],
        [' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', '#', ' ', ' '],
    ]

    for (r, c), t in state.items():
        grid[r][c] = t

    for r in grid:
        print(''.join(r))


def build_adj_list_and_pos(data):
    r, c = 1, 1
    adj_list = defaultdict(set)
    amphipos: Dict[Tuple[int, int], str] = {}
    Q = deque([(r,c)])
    seen = set()

    while Q:
        node = Q.popleft()
        r, c = node
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            np = (nr, nc)
            # print(np, data[nr])
            if data[nr][nc] in '.ABCD' and np not in seen:
                if data[nr][nc] in 'ABCD':
                    amphipos[np] = data[nr][nc]

                seen.add(np)
                Q.append(np)
                adj_list[node].add(np)
                adj_list[np].add(node)

    return adj_list, amphipos

energies = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000,
}

target_cols = {
    'A': 3,
    'B': 5,
    'C': 7,
    'D': 9,
}

hallway_stops = [i for i in range(1, 12) if i not in target_cols.values()]

def as_state(pos: Dict[Tuple[int, int], str]):
    return frozenset(pos.items())

def next_states(state: Dict[Tuple[int, int], str]):
    orig_state = state.copy()
    for amphi_pos, amphi_type in orig_state.items():
        r, c = amphi_pos
        new_state = state.copy()
        del new_state[amphi_pos]

        if r == 1:
            # In hallway
            # dest pit is empty
            #if ((2, target_cols[amphi_type]) not in state) and ((3, target_cols[amphi_type]) not in state):
            # print(f'{amphi_type=}')
            for cri in (2,3,4,5):
                # print(cri, range(2, cri+1), all((ri, target_cols[amphi_type]) not in state for ri in range(2, cri+1)), [state.get((ri, target_cols[amphi_type]), '.') for ri in range(2, cri+1)])
                # print(cri, range(cri+1, 4), all(state.get((ri, target_cols[amphi_type])) == amphi_type for ri in range(cri+1, 4)), [state.get((ri, target_cols[amphi_type]), '.') for ri in range(cri+1, 4)], amphi_type)
                if (
                    all((ri, target_cols[amphi_type]) not in state for ri in range(2, cri+1)) and
                    all(state.get((ri, target_cols[amphi_type])) == amphi_type for ri in range(cri+1, 6))
                ):
                    hallway_pos = list(range(min(c, target_cols[amphi_type]), max(c, target_cols[amphi_type]) + 1))
                    if all(
                        (1, hc) not in new_state
                        for hc in hallway_pos
                    ):
                        yield new_state | {(cri, target_cols[amphi_type]): amphi_type}, energies[amphi_type] * (abs(c-target_cols[amphi_type])+cri-1)

            # if all((ri, target_cols[amphi_type]) not in state for ri in (2,3,4,5)):
            #     # move to bototm of pit
            #     # if hallway is clear
            #     hallway_pos = list(range(min(c, target_cols[amphi_type]), max(c, target_cols[amphi_type]) + 1))
            #     if all(
            #         (1, hc) not in new_state
            #         for hc in hallway_pos
            #     ):
            #         yield new_state | {(3, target_cols[amphi_type]): amphi_type}, energies[amphi_type] * (abs(c-target_cols[amphi_type])+2)

            # elif state.get((3, target_cols[amphi_type])) == amphi_type and (2, target_cols[amphi_type]) not in state:
            #     # move to top of pit
            #     if all(
            #         (1, hc) not in new_state
            #         for hc in range(min(c, target_cols[amphi_type]), max(c, target_cols[amphi_type]) + 1)
            #     ):
            #         yield new_state | {(2, target_cols[amphi_type]): amphi_type}, energies[amphi_type] * (abs(c-target_cols[amphi_type])+1)

        elif 2 <= r <= 5:
            # print(r,c, amphi_type, 
            # [(ri, c) not in state for ri in range(2, r)], all([(ri, c) not in state for ri in range(2, r)]),
            # [state.get((ri, c)) != amphi_type for ri in range(r+1,4)], any([state.get((ri, c)) != amphi_type for ri in range(r+1,4)]))
            if (
                all((ri, c) not in state for ri in range(2, r)) and
                (
                    c != target_cols[amphi_type] or
                    any(state.get((ri, c)) != amphi_type for ri in range(r+1,6))
                )
            ):
                # move to each reachable hallways position                      
                for h in hallway_stops:
                    if all(
                        (1, hc) not in new_state
                        for hc in range(min(c, h), max(c, h) + 1)
                    ):
                        yield new_state | {(1, h): amphi_type}, energies[amphi_type] * (abs(c-h) + r - 1)
                
        # elif r == 2:
        #     # Do I need to move to hallway
        #     # not in target col, or blocking other type
        #     if c != target_cols[amphi_type] or state.get((3, target_cols[amphi_type])) != amphi_type:  
        #         # move to each reachable hallways position                      
        #         for h in hallway_stops:
        #             if all(
        #                 (1, hc) not in new_state
        #                 for hc in range(min(c, h), max(c, h) + 1)
        #             ):
        #                 yield new_state | {(1, h): amphi_type}, energies[amphi_type] * (abs(c-h) + 1)
        #     # moves to hallway
        # elif r == 3:
        #     # Do  (and can) I need to move to hallyway?
        #     # not in targt call and r == 2 is free
        #     if c != target_cols[amphi_type] and (2, c) not in state:
        #         for h in hallway_stops:
        #             if all(
        #                 (1, hc) not in new_state
        #                 for hc in range(min(c, h), max(c, h) + 1)
        #             ):
        #                 yield new_state | {(1, h): amphi_type}, energies[amphi_type] * (abs(c-h) + 2)


def build_state_graph(adj_list: Dict[Tuple[int, int], Set[Tuple[int, int]]], initial_state: Dict[Tuple[int, int], str]):
    Q = deque([initial_state])
    state_adj_list = defaultdict(set)
    seen = set()
    count = 0
    while Q:
        count = (count + 1) % 1000
        if count == 0:
            print('.', end='', flush=True)

        state = Q.popleft()
        frozen_state = as_state(state)
        for next_state, cost in next_states(state):
            frozen_next = as_state(next_state)
            if frozen_next not in seen:
                seen.add(frozen_next)
                Q.append(next_state)
            state_adj_list[frozen_state].add((frozen_next, cost))
            state_adj_list[frozen_next].add((frozen_state, cost))

    return state_adj_list


def dijkstra(source, adj_list, target=None):
    Q = heapdict()
    dist = {source: 0}
    prev = {}

    for state in adj_list:
        if state != source:
            dist[state] = 1_000_000_000_000
            prev[state] = None
        Q[state] = dist[state]

    while Q:
        u, _ = Q.popitem()

        if u == target:
            break

        for state, c in adj_list[u]:
            if state in Q:
                alt = dist[u] + c
                if alt < dist[state]:
                    dist[state] = alt
                    prev[state] = u
                    Q[state] = alt

    return dist, prev


target = frozenset([
    ((2,3), 'A'),
    ((3,3), 'A'),
    ((4,3), 'A'),
    ((5,3), 'A'),
    ((2,5), 'B'),
    ((3,5), 'B'),
    ((4,5), 'B'),
    ((5,5), 'B'),
    ((2,7), 'C'),
    ((3,7), 'C'),
    ((4,7), 'C'),
    ((5,7), 'C'),
    ((2,9), 'D'),
    ((3,9), 'D'),
    ((4,9), 'D'),
    ((5,9), 'D'),
])

adj_list, amphipos = build_adj_list_and_pos(maze)


print('adj_list:', adj_list)
print('amphipos:', amphipos)
print()

state_adj_list = build_state_graph(adj_list, amphipos)
print()
print('target exists:', target in state_adj_list)
dists, prev = dijkstra(as_state(amphipos), state_adj_list, target=target)


print()
print()
# print(dists)
print(dists.get(target, 'boooo!'))

# Print reverse path
# cur = target
# while cur != as_state(amphipos):
#     print_state(dict(cur))
#     print()
#     cur = prev[cur]

#############
#...B.......#
###B#.#C#D###
  #A#D#C#A#
  #########
# some_state = OrderedSet([
#     ((2, 3), 'B'),
#     ((3, 3), 'A'),
#     ((1,6), 'C'), #((2, 5), 'C'),
#     ((3, 5), 'D'),
#     ((1,4), 'B'), #((2, 7), 'B'),
#     ((3, 7), 'C'),
#     ((2, 9), 'D'),
#     ((3, 9), 'A'),
# ])

# picks = [16, 1, 6]

# for ns, cost in next_states(dict(some_state)):
#     print('cost:', cost)
#     print_state(ns)
#     print()
