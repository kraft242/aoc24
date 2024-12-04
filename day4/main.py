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


class Grid:
    def __init__(self, chars):
        self.grid = [list(line) for line in chars.splitlines()]
        self.x_min = 0
        self.y_min = 0
        self.x_max = len(self.grid[0])
        self.y_max = len(self.grid)

    def count_word(self, word):
        return sum(
            self.contains_word(word, x, y, dx, dy)
            for x in range(self.x_max)
            for y in range(self.y_max)
            for dx, dy in deltas.values()
        )

    def count_cross(self, word):
        variant = {
            word[0]: tuple(word),
            word[-1]: tuple(reversed(word))
        }

        d = len(word) - 1

        return sum(
            (
                c1 in variant and c2 in variant
                and self.contains_word(variant[c1], x1, y1, *deltas["se"])
                and self.contains_word(variant[c2], x2, y2, *deltas["sw"])
            )
            for x1 in range(self.x_max - d)
            for y1 in range(self.y_max - d)
            for x2, y2 in [(x1 + d, y1)]
            for c1, c2 in [(self.grid[y1][x1], self.grid[y2][x2])]
        )

    def index_is_valid(self, x, y):
        return self.x_min <= x < self.x_max and self.y_min <= y < self.y_max

    def contains_word(self, word, x, y, dx, dy):
        for i, c in enumerate(word):
            curr_x = x + i * dx
            curr_y = y + i * dy
            if not self.index_is_valid(curr_x, curr_y) or not self.grid[curr_y][curr_x] == c:
                return False
        return True


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
