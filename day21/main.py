from aocd import get_data
from itertools import pairwise
from functools import lru_cache

# Describes the best (shortest) path to get from the right key to the left key
possible_paths = {
    # ^
    ("^", "^"): [""],
    ("^", "A"): [">"],
    ("^", "v"): ["v"],
    ("^", ">"): [">v", "v>"],
    ("^", "<"): ["v<"],
    # A
    ("A", "^"): ["<"],
    ("A", "A"): [""],
    ("A", "v"): ["<v", "v<"],
    ("A", ">"): ["v"],
    ("A", "<"): ["v<<"],
    # >
    (">", "^"): ["^<", "<^"],
    (">", "A"): ["^"],
    (">", "v"): ["<"],
    (">", ">"): [""],
    (">", "<"): ["<<"],
    # v
    ("v", "^"): ["^"],
    ("v", "A"): [">^", "^>"],
    ("v", "v"): [""],
    ("v", ">"): [">"],
    ("v", "<"): ["<"],
    # <
    ("<", "^"): [">^"],
    ("<", "A"): [">>^"],
    ("<", "v"): [">"],
    ("<", ">"): [">>"],
    ("<", "<"): [""],
    # A
    ("A", "0"): ["<"],
    ("A", "1"): ["^<<"],
    ("A", "2"): ["^<", "<^"],
    ("A", "3"): ["^"],
    ("A", "4"): ["^^<<"],
    ("A", "5"): ["<^^", "^^<"],
    ("A", "6"): ["^^"],
    ("A", "7"): ["^^^<<"],
    ("A", "8"): ["<^^^", "^^^<"],
    ("A", "9"): ["^^^"],
    ("A", "A"): [""],
    # 0
    ("0", "0"): [""],
    ("0", "1"): ["^<"],
    ("0", "2"): ["^"],
    ("0", "3"): ["^>", ">^"],
    ("0", "4"): ["^^<"],
    ("0", "5"): ["^^"],
    ("0", "6"): [">^^", "^^>"],
    ("0", "7"): ["^^^<"],
    ("0", "8"): ["^^^"],
    ("0", "9"): ["^^^>", ">^^^"],
    ("0", "A"): [">"],
    # 1
    ("1", "0"): [">v"],
    ("1", "1"): [""],
    ("1", "2"): [">"],
    ("1", "3"): [">>"],
    ("1", "4"): ["^"],
    ("1", "5"): [">^", "^>"],
    ("1", "6"): [">>^", "^>>"],
    ("1", "7"): ["^^"],
    ("1", "8"): ["^^>", ">^^"],
    ("1", "9"): ["^^>>", ">>^^"],
    ("1", "A"): [">>v"],
    # 2
    ("2", "0"): ["v"],
    ("2", "1"): ["<"],
    ("2", "2"): [""],
    ("2", "3"): [">"],
    ("2", "4"): ["<^", "^<"],
    ("2", "5"): ["^"],
    ("2", "6"): [">^", "^>"],
    ("2", "7"): ["^^<", "<^^"],
    ("2", "8"): ["^^"],
    ("2", "9"): ["^^>", ">^^"],
    ("2", "A"): [">v", "v>"],
    # 3
    ("3", "0"): ["<v", "v<"],
    ("3", "1"): ["<<"],
    ("3", "2"): ["<"],
    ("3", "3"): [""],
    ("3", "4"): ["<<^", "^<<"],
    ("3", "5"): ["^<", "<^"],
    ("3", "6"): ["^"],
    ("3", "7"): ["^^<<", "<<^^"],
    ("3", "8"): ["^^<", "<^^"],
    ("3", "9"): ["^^"],
    ("3", "A"): ["v"],
    # 4
    ("4", "0"): [">vv"],
    ("4", "1"): ["v"],
    ("4", "2"): [">v", "v>"],
    ("4", "3"): [">>v", "v>>"],
    ("4", "4"): [""],
    ("4", "5"): [">"],
    ("4", "6"): [">>"],
    ("4", "7"): ["^"],
    ("4", "8"): ["^>", ">^"],
    ("4", "9"): ["^>>", ">>^"],
    ("4", "A"): [">>vv"],
    # 5
    ("5", "0"): ["vv"],
    ("5", "1"): ["<v", "v<"],
    ("5", "2"): ["v"],
    ("5", "3"): [">v", "v>"],
    ("5", "4"): ["<"],
    ("5", "5"): [""],
    ("5", "6"): [">"],
    ("5", "7"): ["^<", "<^"],
    ("5", "8"): ["^"],
    ("5", "9"): ["^>", ">^"],
    ("5", "A"): [">vv", "vv>"],
    # 6
    ("6", "0"): ["<vv", "vv<"],
    ("6", "1"): ["<<v", "v<<"],
    ("6", "2"): ["v<", "<v"],
    ("6", "3"): ["v"],
    ("6", "4"): ["<<"],
    ("6", "5"): ["<"],
    ("6", "6"): [""],
    ("6", "7"): ["^<<", "<<^"],
    ("6", "8"): ["^<", "<^"],
    ("6", "9"): ["^"],
    ("6", "A"): ["vv"],
    # 7
    ("7", "0"): [">vvv"],
    ("7", "1"): ["vv"],
    ("7", "2"): [">vv", "vv>"],
    ("7", "3"): [">>vv", "vv>>"],
    ("7", "4"): ["v"],
    ("7", "5"): [">v", "v>"],
    ("7", "6"): ["v>>", ">>v"],
    ("7", "7"): [""],
    ("7", "8"): [">"],
    ("7", "9"): [">>"],
    ("7", "A"): [">>vvv"],
    # 8
    ("8", "0"): ["vvv"],
    ("8", "1"): ["<vv", "vv<"],
    ("8", "2"): ["vv"],
    ("8", "3"): ["vv>", ">vv"],
    ("8", "4"): ["<v", "v<"],
    ("8", "5"): ["v"],
    ("8", "6"): ["v>", ">v"],
    ("8", "7"): ["<"],
    ("8", "8"): [""],
    ("8", "9"): [">"],
    ("8", "A"): [">vvv", "vvv>"],
    # 9
    ("9", "0"): ["<vvv", "vvv<"],
    ("9", "1"): ["<<vv", "vv<<"],
    ("9", "2"): ["<vv", "vv<"],
    ("9", "3"): ["vv"],
    ("9", "4"): ["<<v", "v<<"],
    ("9", "5"): ["v<", "<v"],
    ("9", "6"): ["v"],
    ("9", "7"): ["<<"],
    ("9", "8"): ["<"],
    ("9", "9"): [">"],
    ("9", "A"): ["vvv"],
}

possible_paths = {
    k: [p + "A" for p in v] for k, v in possible_paths.items()
}


def parse_data(data):
    return data.split("\n")


@lru_cache(maxsize=None)
def get_shortest_path_length(seq, depth, max_depth):
    if depth == max_depth:
        return len(seq)

    sequence = "A" + seq

    paths = (possible_paths[(src, dst)] for src, dst in pairwise(sequence))

    step_lengths = (
        (get_shortest_path_length(p, depth + 1, max_depth) for p in ps)
        for ps in paths
    )
    return sum(min(sl) for sl in step_lengths)


def extract_digits(s):
    return int("".join(str(n) for n in s if n.isdigit()))


def solve(parsed, max_depth):
    spls = [
        get_shortest_path_length(code, depth=0, max_depth=max_depth)
        for code in parsed
    ]
    ns = [extract_digits(code) for code in parsed]
    cs = [spl * n for spl, n in zip(spls, ns)]
    return sum(cs)


def part_one(data):
    parsed = parse_data(data)
    return solve(parsed, max_depth=3)


def part_two(data):
    parsed = parse_data(data)
    return solve(parsed, max_depth=26)


def main():
    data = get_data(day=21, year=2024)
    one = part_one(data)
    two = part_two(data)
    print(f"Part one: {one}")
    print(f"Part two: {two}")


if __name__ == "__main__":
    main()
