from aocd import get_data
from functools import cmp_to_key
from itertools import pairwise


def create_ordering(rules):
    parts = [r.split("|") for r in rules.splitlines()]
    parts = [(int(l), int(r)) for l, r in parts]
    ordering = {l: [] for l, _ in parts}
    for l, r in parts:
        ordering[l].append(r)
    return ordering
    values = [(int(lhs), int(rhs)) for lhs, rhs in parts]

    lt = {lhs: rhs for lhs, rhs in values}

    ordering = list(set(v for pair in values for v in pair))

    l = len(ordering)

    for i in range(l - 1):
        j_min = i
        for j in range(i + 1,  l):
            if lt.get(ordering[j], -1) == ordering[j_min]:
                j_min = j
        if j_min != i:
            ordering[i], ordering[j_min] = ordering[j_min], ordering[i]

    print(ordering)

    print(values)


def parse_update(u):
    return [int(e) for e in u.split(",")]


def parse_updates(updates):
    return [parse_update(u) for u in updates.splitlines()]


def update_is_valid(update, ordering):
    size = len(update)
    for i in range(size):
        l = update[i]
        for j in range(i + 1, size):
            r = update[j]
            if r in ordering and l in ordering[r]:
                print(f"Update {update} is invalid")
                return False
    return True


def part_one(data):
    rules, updates = data.split("\n\n")
    ordering = create_ordering(rules)
    print(ordering)

    updates = parse_updates(updates)

    result = 0
    for u in updates:
        if update_is_valid(u, ordering):
            print(f"Update {u} is valid")
            result += u[len(u) // 2]
    return result

    return 0


def fix_invalid(update, ordering):
    size = len(update)
    for i in range(size):
        l = update[i]
        for j in range(i + 1, size):
            r = update[j]
            if r in ordering and l in ordering[r]:
                update[i], update[j] = update[j], update[i]
    return update


def part_two(data):
    rules, updates = data.split("\n\n")
    ordering = create_ordering(rules)
    print(ordering)

    updates = parse_updates(updates)

    invalid = []
    for u in updates:
        if not update_is_valid(u, ordering):
            invalid.append(u)

    for update in invalid:
        while not update_is_valid(update, ordering):
            update = fix_invalid(update, ordering)

    return sum(u[len(u) // 2] for u in invalid)


def main():
    data = get_data(day=5, year=2024)
#    data = """47|53
#97|13
#97|61
#97|47
#75|29
#61|13
#75|53
#29|13
#97|29
#53|29
#61|53
#97|53
#61|29
#47|13
#75|47
#97|75
#47|61
#75|61
#47|29
#75|13
#53|13
#
#75,47,61,53,29
#97,61,53,29,13
#75,29,13
#75,97,47,61,53
#61,13,29
#97,13,75,29,47"""
    one = part_one(data)
    two = part_two(data)
    print(f"Part one: {one}")
    print(f"Part two: {two}")


if __name__ == "__main__":
    main()
