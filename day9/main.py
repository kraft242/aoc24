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


def get_checksum(disk):
    return sum(i * n if n != PAD else 0 for i, n in enumerate(disk))


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

    return get_checksum(disk)


def get_segments(disk):
    segments = []

    val, start, size = disk[0], 0, 0

    i = 0

    while i < len(disk):
        if disk[i] == val:
            size += 1
            i += 1
        else:
            segments.append((val, start, size))
            val, start, size = disk[i], i, 1
            i += 1

    segments.append((val, start, size))
    return segments


def get_pad_list_index(pads, val_index, val_len):
    for j, (pad_index, pad_len) in enumerate(pads):
        if pad_index < val_index and pad_len >= val_len:
            return j
    return -1


def part_two(data):
    disk = get_disk(data)

    segments = get_segments(disk)

    files = [(v, i, l) for v, i, l in segments if v != PAD]
    pads = [(i, l) for v, i, l in segments if v == PAD]

    while files:
        val, val_index, val_len = files.pop()

        pad_list_index = get_pad_list_index(pads, val_index, val_len)

        found = pad_list_index != -1
        if not found:
            continue

        pad_index, pad_len = pads.pop(pad_list_index)

        for i in range(pad_index, pad_index + val_len):
            disk[i] = val

        for i in range(val_index, val_index + val_len):
            disk[i] = PAD

        diff = pad_len - val_len
        if diff > 0:
            new_pad_index = pad_index + val_len
            pads.append((new_pad_index, diff))
            pads.sort()

    return get_checksum(disk)


def main():
    data = get_data(day=9, year=2024)
    one = part_one(data)
    two = part_two(data)
    print(f"Part one: {one}")
    print(f"Part two: {two}")


if __name__ == "__main__":
    main()
