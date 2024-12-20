from aocd import get_data
from itertools import zip_longest

PAD = -1


def print_disk(disk):
    for n in disk:
        if n == PAD:
            c = "."
        else:
            c = str(n)
        print(c, end="")
    print()


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

    i, j = 0, len(disk) - 1
    while i <= j:
        match (disk[i] == PAD, disk[j] == PAD):
            case True, True:
                j -= 1
            case False, True:
                j -= 1
            case True, False:
                disk[i], disk[j] = disk[j], disk[i]
                i += 1
                j -= 1
            case False, False:
                i += 1
            case _:
                raise ValueError("Invalid")

    return sum(i*n if n != PAD else 0 for i, n in enumerate(disk))


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
