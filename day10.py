example = '''[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]'''

with open('inputs/day-10-input.txt') as input_file:
    data = input_file.read()

opens = {
    '(': ')',
    '[': ']',
    '<': '>',
    '{': '}',
}

scores = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

close_scores = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}

def validate(chunks: str):
    stack = []

    for c in chunks:
        if c in opens:
            stack.append(opens[c])
        else:
            e = stack.pop()
            if c != e:
                return scores[c]

    return 0

def validate2(chunks: str):
    stack = []

    for c in chunks:
        if c in opens:
            stack.append(opens[c])
        else:
            e = stack.pop()
            if c != e:
                return 0

    total = 0
    print(stack)
    for c in stack[::-1]:
        total *= 5
        total += close_scores[c]
        print(total)
    return total

for line in example.split():
    print(line, validate2(line))

scores = [validate2(line) for line in data.split()]
scores = [score for score in scores if score > 0]
scores.sort()
print(scores[len(scores)//2])