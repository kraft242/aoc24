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
        variant = {
            word[0]: word,
            word[-1]: "".join(reversed(word))
        }

        for y1 in range(self.y_max - 2):
            for x1 in range(self.x_max - 2):
                x2, y2 = x1 + 2, y1

                c1 = self.grid[y1][x1]
                c2 = self.grid[y2][x2]

                self.count[y1][x1] = (
                    c1 in variant and c2 in variant
                    and self.count_word_recursive(variant[c1], 0, x1, y1, *deltas["se"]) > 0
                    and self.count_word_recursive(variant[c2], 0, x2, y2, *deltas["sw"]) > 0
                )

        return sum_2d(self.count)

    def count_word_recursive(self, word, depth, x, y, dx, dy):
        if not self.index_is_valid(x, y) or self.grid[y][x] != word[depth]:
            return 0

        if depth == len(word) - 1:
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
