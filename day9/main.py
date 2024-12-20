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


def get_disk(data):
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

    return disk


def part_one(data):
    disk = get_disk(data)

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
    disk = get_disk(data)

    def get_sequence_start(index, c):
        start = index
        while disk[start] == c:
            start -= 1
        return start + 1

    def get_sequence_end(index, c):
        end = index
        while disk[end] == c:
            end += 1
        return end - 1

    # print("Before:")
    # print_disk(disk)

    j = len(disk) - 1
    while j >= 0:
        k = get_sequence_start(j, disk[j])
        dj = j - k + 1
        if disk[j] == PAD:
            j -= dj
            continue

        # print(f"j: {j}, k: {k}, dj: {dj}")
        i = 0
        while i < j - dj:
            end = get_sequence_end(i, disk[i])
            di = end - i + 1
            if disk[i] == PAD and di >= dj:
                print(f"j: {j}, i: {i}, end: {end}, di: {di}, dj: {dj}")
                # print(f"i: {i}, end: {end}, di: {di}")
                ilo, ihi = i, i + dj
                jlo, jhi = j - dj + 1, j + 1
                # print(f"ilo: {ilo}, ihi: {ihi}, jlo: {jlo}, jhi: {jhi}")
                disk[ilo: ihi], disk[jlo:jhi] = disk[jlo:jhi], disk[ilo:ihi]
                break
            i += di
            # i += di
        # print_disk(disk)
        j -= dj

    # print("After: ")
    # print_disk(disk)

    return sum(i*n if n != PAD else 0 for i, n in enumerate(disk))


def main():
    data = get_data(day=9, year=2024)
    # data = "2333133121414131402"
    one = part_one(data)
    two = part_two(data)
    print(f"Part one: {one}")
    print(f"Part two: {two}")


if __name__ == "__main__":
    main()
