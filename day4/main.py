from aocd import get_data


deltas = {
    "n": (0, -1),  # North
    "ne": (1, -1),  # North East
    "e": (1, 0),   # East
    "se": (1, 1),   # South East
    "s": (0, 1),   # South
    "sw": (-1, 1),  # South West
    "w": (-1, 0),  # West
    "nw": (-1, -1),  # North West
}


def sum_2d(values):
    return sum(sum(values, []))


class Grid:
    def __init__(self, chars):
        self.grid = [list(line) for line in chars.splitlines()]
        self.x_min = 0
        self.y_min = 0
        self.x_max = len(self.grid[0])
        self.y_max = len(self.grid)
        self.count = [
            [0 for _ in range(self.x_max)] for _ in range(self.y_max)
        ]

    def index_is_valid(self, x, y):
        return self.x_min <= x < self.x_max and self.y_min <= y < self.y_max

    def count_word(self, word):
        for y in range(self.y_max):
            for x in range(self.x_max):
                self.count[y][x] = sum(
                    self.count_word_recursive(word, 0, x, y, dx, dy)
                    for dx, dy in deltas.values()
                )

        return sum_2d(self.count)

    def count_cross(self, word):
        variants = {
            word[0]: word,
            word[-1]: "".join(reversed(word))
        }
        for y in range(self.y_max - 2):
            for x in range(self.x_max - 2):
                c = self.grid[y][x]
                d = self.grid[y][x + 2]

                if not (c in variants.keys() and d in variants.keys()):
                    continue

                south_east = self.count_word_recursive(
                    variants[c], 0, x, y, *deltas["se"]
                )

                if south_east == 0:
                    continue

                south_west = self.count_word_recursive(
                    variants[d], 0, x + 2, y, *deltas["sw"]
                )

                if south_west == 0:
                    continue
                self.count[y][x] += 1

        return sum_2d(self.count)

    def count_word_recursive(self, word, depth, x, y, dx, dy):
        if not self.index_is_valid(x, y):
            return 0

        if depth >= len(word):
            return 0

        correct = self.grid[y][x] == word[depth]

        if not correct:
            return 0

        if correct and depth == len(word) - 1:
            return 1

        return self.count_word_recursive(word, depth + 1, x + dx, y + dy, dx, dy)


def part_one(data):
    grid = Grid(data)
    return grid.count_word("XMAS")


def part_two(data):
    grid = Grid(data)
    return grid.count_cross("MAS")


def main():
    data = get_data(day=4, year=2024)
    one = part_one(data)
    two = part_two(data)
    print(f"Part one: {one}")
    print(f"Part two: {two}")


if __name__ == "__main__":
    main()
