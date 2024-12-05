from aocd import get_data
from functools import cmp_to_key


def create_ordering(rules):
    parts = (r.split("|") for r in rules.splitlines())
    return {(int(l), int(r)) for l, r in parts}


def parse_update(u):
    return [int(e) for e in u.split(",")]


def parse_updates(updates):
    return [parse_update(u) for u in updates.splitlines()]


def parse_data(data):
    rules, updates = data.split("\n\n")
    return create_ordering(rules), parse_updates(updates)


def sort_updates(updates, less_than):
    def compare(l, r):
        if (l, r) in less_than:
            return -1
        if (r, l) in less_than:
            return 1
        return 0

    return [sorted(u, key=cmp_to_key(compare)) for u in updates]


def midpoint(v):
    return v[len(v) // 2]


def solve(data, condition):
    less_than, updates = parse_data(data)
    ordered = sort_updates(updates, less_than)
    filtered = (o for u, o in zip(updates, ordered) if condition(u, o))

    return sum(map(midpoint, filtered))


def part_one(data):
    def condition(l, r): return l == r
    return solve(data, condition)


def part_two(data):
    def condition(l, r): return l != r
    return solve(data, condition)


def main():
    data = get_data(day=5, year=2024)
    one = part_one(data)
    two = part_two(data)
    print(f"Part one: {one}")
    print(f"Part two: {two}")


if __name__ == "__main__":
    main()
