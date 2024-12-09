from aocd import get_data
from itertools import zip_longest

PAD = -1


def part_one(data):
    values = [int(n) for n in list(data)]
    size = len(values)
    disk = []

    nums = (values[i] for i in range(size) if i % 2 == 0)
    pads = (values[i] for i in range(size) if i % 2 != 0)

    curr = 0
    for n, p in zip_longest(nums, pads, fillvalue=PAD):
        disk.extend(curr for _ in range(n))
        curr += 1
        disk.extend(PAD for _ in range(p))

    result = []
    i, j = 0, len(disk) - 1
    while i <= j:
        vi, vj = disk[i], disk[j]
        if vi != PAD:
            result.append(vi)
            i += 1
        elif vj == PAD:
            j -= 1
        elif vj != PAD:
            result.append(vj)
            i += 1
            j -= 1
        else:
            raise ValueError("Invalid")

    return sum(i*n for i, n in enumerate(result))


def part_two(data):
    return 0


def main():
    data = get_data(day=9, year=2024)
    # data = "2333133121414131402"
    one = part_one(data)
    two = part_two(data)
    print(f"Part one: {one}")
    print(f"Part two: {two}")


if __name__ == "__main__":
    main()
