from aocd import get_data
import re


def get_mul_sum(s):
    mul_pattern = r"mul\((\d+),(\d+)\)"
    matches = re.findall(mul_pattern, s)

    return sum(int(lhs) * int(rhs) for lhs, rhs in matches)


def part_one(data):
    return get_mul_sum(data)


def remove_dont_do_sequences(s):
    banned_pattern = re.compile(
        r"""don't\(\)  # Literal don't()
        .*?            # As few any matches as possible
        (do\(\)|$)     # Literal do() OR EOL""", flags=re.VERBOSE | re.DOTALL
    )

    return re.sub(banned_pattern, "", s)


def part_two(data):
    cleaned = remove_dont_do_sequences(data)
    return get_mul_sum(cleaned)


def main():
    data = get_data(day=3, year=2024)
    one = part_one(data)
    two = part_two(data)
    print(f"Part one: {one}")
    print(f"Part two: {two}")


if __name__ == "__main__":
    main()
