from aocd import get_data
import re


def part_one(data):
    whole = data.replace("\n", " ")
    muls = r"mul\((\d+),(\d+)\)"
    matches = re.finditer(muls, whole)
    return sum(int(match.group(1)) * int(match.group(2)) for match in matches)


def part_two(data):
    whole = data.replace("\n", " ")
    mul_pattern = r"mul\((\d+),(\d+)\)"
    dont_pattern = r"don't\(\)"
    do_pattern = r"do\(\)"
    complete_pattern = r"|".join((mul_pattern, do_pattern, dont_pattern))

    matches = re.finditer(complete_pattern, whole)
    enabled = True
    acc = 0
    for m in matches:
        group = m.group()
        if group == "don't()":
            enabled = False
        elif group == "do()":
            enabled = True
        elif enabled:
            acc += int(m.group(1)) * int(m.group(2))

    return acc


def main():
    data = get_data(day=3, year=2024)
    one = part_one(data)
    two = part_two(data)
    print(f"Part one: {one}")
    print(f"Part two: {two}")


if __name__ == "__main__":
    main()
