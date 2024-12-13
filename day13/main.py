from aocd import get_data
import numpy as np
from time import perf_counter_ns
import re


def parse_machine(machine):
    number_pattern = r"\d+"
    matches = re.finditer(number_pattern, machine, flags=re.DOTALL)
    numbers = (int(m.group()) for m in matches)
    ax, ay, bx, by, X, Y = numbers
    lhs = np.array([[ax, bx], [ay, by]])
    rhs = np.array([[X], [Y]])
    return lhs, rhs


def solve_system(lhs, rhs):
    is_invertible = np.linalg.det(lhs) != 0
    if not is_invertible:
        return np.zeros((2, 1))
    return np.linalg.solve(lhs, rhs)


def is_valid_solution(sol):
    tolerance = 1e-3
    positive = np.all(sol >= 0)
    abs_diff = np.abs(sol - np.round(sol))
    return positive and np.all(abs_diff < tolerance)


def solve(data, increment=0):
    machines = data.split("\n\n")
    token_cost = np.array([3, 1])

    parsed = [parse_machine(m) for m in machines]
    lhs_matrices = np.array([lhs for lhs, _ in parsed])
    rhs_matrices = increment + np.array([rhs for _, rhs in parsed])

    solutions = np.array(
        [
            solve_system(lhs, rhs)
            for lhs, rhs in zip(lhs_matrices, rhs_matrices)
        ]
    )
    valid_solutions = np.array(
        [
            sol
            for sol in solutions
            if is_valid_solution(sol)
        ]
    )

    costs = np.dot(valid_solutions.reshape(-1, 2), token_cost)

    return int(sum(costs))


def part_one(data):
    return solve(data)


def part_two(data):
    return solve(data, increment=10000000000000)


def main():
    data = get_data(day=13, year=2024)
    t0 = perf_counter_ns()
    one = part_one(data)
    two = part_two(data)
    t1 = perf_counter_ns()
    print(f"Time: {(t1 - t0) / 1e6:.2f}ms")
    print(f"Part one: {one}")
    print(f"Part two: {two}")


if __name__ == "__main__":
    main()
