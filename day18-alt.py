from functools import reduce
from itertools import permutations
from json import loads
from time import perf_counter

# from advent import getData


class Snail():
    def __init__(self, data=None) -> None:
        self.val, self.left, self.right = [None]*3
        if isinstance(data, int):
            self.val = data
        elif isinstance(data, Snail):
            self.left = data.left
            self.right = data.right
        else:
            self.left, self.right = map(Snail, data)

    def __repr__(self) -> str:
        if self.val is None:
            return f'[{self.left},{self.right}]'
        return str(self.val)

    def mag(self) -> int:
        if self.val is not None:
            return self.val
        return self.left.mag()*3 + 2*self.right.mag()


def get_leaves(sn):
    lst = []
    q = [sn]
    while q:
        node = q.pop()
        assert isinstance(node, Snail)
        if node.val is not None:
            lst.append(node)
        else:
            q.append(node.right)
            q.append(node.left)
    return lst


def add(s1, s2):
    return sn_reduce(Snail([s1, s2]))


def sn_reduce(sn):
    print('reduce', sn)
    while True:
        restart = explode(sn)
        if restart:
            print('exploded', sn)
            continue
        restart = split(sn)
        if not restart:
            break
        print('split', sn)

    return sn


def split(sn):
    restart = False
    leaves = get_leaves(sn)
    for leaf in leaves:
        if leaf.val > 9:
            leaf.left = Snail(leaf.val//2)
            leaf.right = Snail(leaf.val - leaf.val//2)
            leaf.val = None
            restart = True
            break
    return restart


def explode(sn):
    restart = False
    q = [(sn, 0)]
    while q:
        node, d = q.pop()
        print(f'{node=} {d=}')
        if d == 4 and node.val is None:
            leaves = get_leaves(sn)
            print(leaves)
            left_idx = leaves.index(node.left)
            right_idx = left_idx + 1

            print(left_idx, right_idx)
            if left_idx > 0:
                leaves[left_idx-1].val += node.left.val
            if right_idx + 1 < len(leaves):
                leaves[right_idx+1].val += node.right.val
            node.val, node.left, node.right = 0, None, None
            restart = True
            break
        if node.val is not None:
            continue
        q.append((node.right, d+1))
        q.append((node.left, d+1))
    return restart


if __name__ == '__main__':
    a = Snail([[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]])
    b = Snail([7,[[[3,7],[4,3]],[[6,3],[8,8]]]])
    s = Snail([[[[4,0],[5,0]],[[[4,5],[2,6]],[9,5]]],[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]])
    print(s)
    explode(s)
    print(s)
    # d = list(map(loads, getData(18)))
    # t0 = perf_counter()
    # print(reduce(add, map(Snail, d)).mag())
    # t1 = perf_counter()
    # print(max(add(*map(Snail, pair)).mag() for pair in permutations(d, 2)))
    # t2 = perf_counter()
    # print(f'Part 1 completed in {t1-t0:.3f} seconds.')
    # print(f'Part 2 completed in {t2-t1:.3f} seconds.')