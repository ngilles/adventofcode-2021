from __future__ import annotations

from dataclasses import dataclass
from collections import Counter, defaultdict

from parsy import (
    any_char,
    char_from,
    digit,
    eof,
    generate,
    letter,
    peek,
    regex,
    seq,
    string,
    string_from,

)

example = '''NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C'''

with open('inputs/day-14-input.txt') as input_file:
    data = input_file.read()

polymer_literal = regex(r'[A-Z]+')
pair_literal = regex(r'[A-Z]{2}')
single_literal = regex(r'[A-Z]')
replacement_rule = seq(pair_literal, string(' -> ') >> single_literal)
replacement_rules = replacement_rule.sep_by(char_from('\n'))

polymer_rules = seq(polymer_literal, string('\n\n') >> replacement_rules)

polymer, base_rules = polymer_rules.parse(data)

print(polymer)
print(base_rules)

rules = dict(base_rules)
# for pair, ins in base_rules:
#     rules[pair] = ins
#     rules[pair[::-1]] = ins


elements = defaultdict(int)
for e in polymer:
    elements[e] +=1

pairs = defaultdict(int)
for p in zip(polymer, polymer[1:]):
    pairs[p[0]+p[1]] += 1

print(pairs)
print(elements)

def react(elements, pairs, rules):
    ne = elements.copy()
    np = pairs.copy()

    for p, c in pairs.items():
        if p in rules:
            ne[rules[p]] += c
            np[p] -= c
            np[p[0]+rules[p]] += c
            np[rules[p] + p[1]] += c

    return ne, np

for _ in range(40):
    elements, pairs  = react(elements, pairs, rules)
    # print(elements, pairs)

print(max(elements.values()) - min(elements.values()))

# def react(polymer, rules):
#     np = [polymer[0]]
#     # print(np)
#     for a, b in zip(polymer, polymer[1:]):
#         p = a+b
#         if a+b in rules:
#             np.append(rules[a+b])
#         np.append(b)
#         # print(np, p, rules.get(p))

#     return ''.join(np)


# for _ in range(40):
#     polymer = react(polymer, rules)
#     # print(polymer)

# print(len(polymer))
# freq = Counter(polymer)
# sorted_freq = list(sorted(freq.items(), key=lambda f: f[1]))
# print(sorted_freq)
# print(sorted_freq[-1][1] - sorted_freq[0][1])
