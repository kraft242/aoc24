from aocd import get_data

deltas = [
    (0, -1),  # North
    (1, -1),  # North East
    (1, 0),   # East
    (1, 1),   # South East
    (0, 1),   # South
    (-1, 1),  # South West
    (-1, 0),  # West
    (-1, -1),  # North West
]


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
                    for dx, dy in deltas
                )

        return sum(sum(self.count, []))

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
    return 0


def main():
    data = get_data(day=4, year=2024)
    one = part_one(data)
    two = part_two(data)
    print(f"Part one: {one}")
    print(f"Part two: {two}")


if __name__ == "__main__":
    main()
