from aocd import get_data
from functools import cmp_to_key


def create_ordering(rules):
    parts = [r.split("|") for r in rules.splitlines()]
    parts = [(int(l), int(r)) for l, r in parts]
    return set(parts)


def parse_update(u):
    return [int(e) for e in u.split(",")]


def parse_updates(updates):
    return [parse_update(u) for u in updates.splitlines()]


def parse_data(data):
    rules, updates = data.split("\n\n")
    return create_ordering(rules), parse_updates(updates)


def sort_updates(updates, ordering):
    def compare(l, r):
        if (l, r) in ordering:
            return -1
        if (r, l) in ordering:
            return 1
        return 0

    return [sorted(u, key=cmp_to_key(compare)) for u in updates]


def midpoint(v):
    return v[len(v) // 2]


def part_one(data):
    ordering, updates = parse_data(data)

    ordered = sort_updates(updates, ordering)

    valid = [u for u, o in zip(updates, ordered) if u == o]

    return sum(map(midpoint, valid))


def part_two(data):
    ordering, updates = parse_data(data)

    ordered = sort_updates(updates, ordering)

    invalid = [u for u, o in zip(updates, ordered) if u != o]

    fixed = sort_updates(invalid, ordering)

    return sum(map(midpoint, fixed))


def main():
    data = get_data(day=5, year=2024)
    one = part_one(data)
    two = part_two(data)
    print(f"Part one: {one}")
    print(f"Part two: {two}")


if __name__ == "__main__":
    main()