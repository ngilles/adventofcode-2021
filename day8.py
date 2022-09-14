with open('inputs/day-8-input.txt') as input_file:
    data = input_file.readlines()

data = [e.strip().split('|') for e in data]
print(data)

digits = {
    0: {0,1,2,4,5,6},
    1: {2,5},
    2: {0,2,3,4,6},
    3: {0,2,3,5,6},
    4: {1,2,3,5},
    5: {0,1,3,5,6},
    6: {0,1,3,4,5,6},
    7: {0,2,5},
    8: {0,1,2,3,4,5,6},
    9: {0,1,2,3,5,6},
}
specific_lens = {2, 4, 3, 7}
counts = 0

for _, digits in data:
    digs = digits.split()
    for dig in digs:
        if len(dig) in specific_lens:
            counts += 1
    print(digs)

print(counts)

def pick(s, predicate):
    r = [e for e in s if predicate(e)]
    if len(r) != 1:
        raise Exception('went wrong')

    s.remove(r[0])

    return r[0]

total = 0

for signals, digits in data:
    signals = [frozenset(s) for s in signals.split()]

    # pick the ones that are unique
    d1 = pick(signals, lambda x: len(x) == 2)
    d4 = pick(signals, lambda x: len(x) == 4)
    d7 = pick(signals, lambda x: len(x) == 3)
    d8 = pick(signals, lambda x: len(x) == 7)
    # len 5:
    # 3 overlabs with "1" in 2 places
    # 2 overlaps with "4" in 2 places
    # 5 is last one
    d3 = pick(signals, lambda x: len(x) == 5 and len(x & d1) == 2) 
    d2 = pick(signals, lambda x: len(x) == 5 and len(x & d4) == 2)
    d5 = pick(signals, lambda x: len(x) == 5)
    # len 6:
    # 6 overlabs with 1 in 1 place
    # 9 overlaps with 4 in 4 places
    # 0 is left over
    d6 = pick(signals, lambda x: len(x) == 6 and len(x & d1) == 1)
    d9 = pick(signals, lambda x: len(x) == 6 and len(x & d4) == 4)
    d0 = pick(signals, lambda x: len(x) == 6)

    signal_map = {d0: '0', d1: '1', d2: '2', d3: '3', d4: '4', d5: '5', d6: '6', d7: '7', d8: '8', d9: '9'}

    print(digits)
    v = int(''.join(signal_map[frozenset(d)] for d in digits.split()))
    print(v)
    total += v

print(total)
