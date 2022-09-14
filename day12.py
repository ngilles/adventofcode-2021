from collections import defaultdict

example = '''start-A
start-b
A-c
A-b
b-d
A-end
b-end'''

example2 = '''dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc'''

example3 = '''fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW'''

with open('inputs/day-12-input.txt') as input_file:
    data = input_file.read()

adj_list = defaultdict(list)

for l in data.split():
    a, b = l.split('-')
    adj_list[a].append(b)
    adj_list[b].append(a)


class Graph:
    def __init__(self, graph):
        self._adj_list = graph


    def paths(self, path, seen):
        node = path[-1]
        for next_node in self._adj_list[node]:
            if next_node not in seen:
                if next_node == 'end':
                    yield path + [next_node]
                else:
                    new_seen = seen.copy()
                    if next_node[0].islower():
                        new_seen |= {next_node}

                    new_path = path[:] + [next_node]
                    yield from self.paths(new_path, new_seen)
                

    def paths2(self, path, seen, max_seen):
        node = path[-1]
        for next_node in self._adj_list[node]:
            #print(path, next_node, seen, max_seen)
            if next_node == 'end':
                yield path + [next_node]
            elif next_node != 'start':
                if next_node[0].isupper() or max_seen < 2 or seen[next_node] == 0:
                    new_seen = seen.copy()
                    if next_node[0].islower():
                        new_seen[next_node] += 1

                    new_path = path[:] + [next_node]
                    yield from self.paths2(new_path, new_seen, max(new_seen.values(), default=0))

graph = Graph(adj_list)

paths = list(graph.paths(['start'], {'start'})) 
# for path in paths:
#     print(path)
print(len(paths))

paths = list(graph.paths2(['start'], defaultdict(int), 1)) 
# paths.sort()
# for path in paths:
#     print(path)
print(len(paths))