from __future__ import annotations
from collections import deque

from parsy import seq, char_from, regex, generate, string
from dataclasses import dataclass
from functools import reduce
from pprint import pprint
from itertools import permutations
from copy import deepcopy

class SnailFishNumber:
    number: int
    left: SnailFishNumber
    right: SnailFishNumber

    def __init__(self, number, left, right):
        self.number = number
        self.left = left
        self.right = right

    @property
    def magnitude(self):
        if self.is_regular:
            return self.number
        else:
            return self.left.magnitude * 3 + self.right.magnitude * 2

    @property
    def is_regular(self):
        return self.number is not None

    @property
    def is_pair(self):
        return not self.is_regular

    def __repr__(self):
        if self.is_regular:
            return f'{self.number}'
        else:
            return f'[{self.left!r},{self.right!r}]'


number_literal = regex(r'-?[0-9]+').map(int)

@generate
def snailfish_pair():
    yield string('[')
    left = yield snailfish_literal
    yield string(',')
    right = yield snailfish_literal
    yield string(']')

    return SnailFishNumber(None, left, right)

@generate
def snailfish_regular():
    n = yield number_literal
    return SnailFishNumber(n, None, None)

snailfish_literal = snailfish_regular | snailfish_pair


def get_leaves(sn):
    leaves = []
    q = deque([sn])

    while q:
        node = q.pop()
        if node.is_regular:
            leaves.append(node)
        else:
            q.append(node.right)
            q.append(node.left)

    return leaves

def sn_add(left, right):
    s = SnailFishNumber(None, left, right)
    #print(left, '+', right, '=', s)
    return sn_reduce(SnailFishNumber(None, left, right))

def sn_reduce(sn):
    # print('reduce', sn)
    while True:
        restart = sn_explode(sn)
        if restart:
            # print('exploded', sn)
            continue
        restart = sn_split(sn)
        if not restart:
            break
        # print('split', sn)

    # print(sn)
    return sn


def sn_split(sn):
    restart = False
    leaves = get_leaves(sn)
    for leaf in leaves:
        if leaf.number > 9:
            leaf.left = SnailFishNumber(leaf.number // 2, None, None)
            leaf.right = SnailFishNumber(leaf.number - leaf.number // 2, None, None)
            leaf.number = None
            restart =True
            break
    return restart

def sn_explode(sn):
    restart = False
    q = deque([(sn, 0)])

    while q:
        node, d = q.pop()
        #print(f'{node=} {d=}')
        if d == 4 and node.is_pair:
            leaves = get_leaves(sn)
            #print(leaves)
            left_idx = leaves.index(node.left)
            right_idx = left_idx + 1

            #print(left_idx, right_idx)           
            if left_idx > 0:
                leaves[left_idx-1].number += node.left.number
            
            if right_idx + 1 < len(leaves):
                leaves[right_idx+1].number += node.right.number

            node.number, node.left, node.right = 0, None, None
            
            restart = True
            break
        if node.is_regular:
            continue
        q.append((node.right, d + 1))
        q.append((node.left, d + 1))
    
    return restart


examples = [
    '[1,2]',
    '[[1,2],3]',
    '[9,[8,7]]',
    '[[1,9],[8,5]]',
    '[[[[1,2],[3,4]],[[5,6],[7,8]]],9]',
    '[[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]',
    '[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]',
]

examples = [
    '[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]',
    '[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]',
    '[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]',
    '[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]',
    '[7,[5,[[3,8],[1,4]]]]',
    '[[2,[2,2]],[8,[8,1]]]',
    '[2,9]',
    '[1,[[[9,3],9],[[9,0],[0,7]]]]',
    '[[[5,[7,4]],7],1]',
    '[[[[4,2],2],6],[8,7]]',
]

examples = [
    '[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]',
    '[[[5,[2,8]],4],[5,[[9,9],0]]]',
    '[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]',
    '[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]',
    '[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]',
    '[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]',
    '[[[[5,4],[7,7]],8],[[8,3],8]]',
    '[[9,3],[[9,9],[6,[4,9]]]]',
    '[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]',
    '[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]',
]

lines  = [l.strip() for l in open('inputs/day-18-input.txt').readlines()]

sns = [snailfish_pair.parse(e.strip()) for e in lines]
sns = [snailfish_pair.parse(e.strip()) for e in examples]
s = reduce(sn_add, sns)
print(s)
print(s.magnitude)

print(max(sn_add(snailfish_pair.parse(a), snailfish_pair.parse(b)).magnitude for a, b in permutations(lines, 2)))

# # pprint(sns)
# # r = reduce(sn_add, sns)
# # print(r)
# a = sns[0]
# for sn in sns[1:]:
#     print(a)
#     print('+', sn)
#     r = sn_add(a,sn)
#     print('=', r)
#     print()
#     a = r
 