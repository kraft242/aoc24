from aocd import get_data
import numpy as np
import re


def parse_machine(machine):
    number_pattern = r"\d+"
    matches = re.finditer(number_pattern, machine, flags=re.DOTALL)
    numbers = [int(m.group()) for m in matches]
    ax, ay, bx, by, X, Y = numbers
    lhs = np.array([[ax, bx], [ay, by]])
    rhs = np.array([[X], [Y]])
    return lhs, rhs


def solve_system(lhs, rhs):
    is_invertible = np.linalg.det(lhs) != 0
    if not is_invertible:
        return np.zeros((2, 1))
    return np.linalg.solve(lhs, rhs)


def is_valid_solution(sol, atol=1e-3):
    positive = np.all(sol >= 0)
    abs_diff = np.abs(sol - np.round(sol))
    return positive and all(abs_diff < atol)


def solve(data, increment=0):
    machines = data.split("\n\n")
    token_cost = np.array([[3], [1]]).flatten()

    parsed = (parse_machine(m) for m in machines)
    solutions = (solve_system(lhs, rhs + increment) for lhs, rhs in parsed)
    valid_solutions = filter(is_valid_solution, solutions)
    costs = (np.dot(sol.flatten(), token_cost) for sol in valid_solutions)

    return int(sum(costs))


def part_one(data):
    return solve(data)


def part_two(data):
    return solve(data, increment=10000000000000)


def main():
    data = get_data(day=13, year=2024)
    one = part_one(data)
    two = part_two(data)
    print(f"Part one: {one}")
    print(f"Part two: {two}")


if __name__ == "__main__":
    main()
