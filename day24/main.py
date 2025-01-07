from aocd import get_data
from time import perf_counter_ns
import networkx as nx
import matplotlib.pyplot as plt
from graphviz import Digraph
import re


def parse_data(data):
    initial, combined = data.split("\n\n")
    active, inactive = {}, set()
    for line in initial.split("\n"):
        wire, value = line.split(": ")
        active[wire] = bool(int(value))

    for line in combined.split("\n"):
        lhs, rhs = line.split(" -> ")
        l, op, r = lhs.split(" ")
        inactive.add((l, op, r, rhs))

    return active, inactive


def solve(active, inactive):
    def get_value(l, r, op):
        match op:
            case "AND":
                return active[l] and active[r]
            case "OR":
                return active[l] or active[r]
            case "XOR":
                return active[l] != active[r]

    while inactive:
        next_inactive = set()
        for l, op, r, wire in inactive:
            if l in active and r in active:
                val = get_value(l, r, op)
                active[wire] = val
            else:
                next_inactive.add((l, op, r, wire))
        inactive = next_inactive

    return active


def get_value(active, first_char):
    result = [
        (wire, int(value))
        for wire, value in active.items()
        if wire.startswith(first_char)
    ]

    result.sort(reverse=True)

    binary = "".join(str(v) for _, v in result)

    return int(binary, 2)


def part_one(data):
    active, inactive = parse_data(data)

    active = solve(active, inactive)

    return get_value(active, "z")


def is_output(w):
    return w.startswith("z")


def is_input(w):
    return w.startswith("x") or w.startswith("y")


def part_two(data):
    _, inactive = parse_data(data)

    def rule_exists(op, input):
        return any(
            o == op and (l == input or r == input) for l, o, r, _ in inactive
        )

    def is_wrong(l, op, r, out):
        both_inputs = is_input(l) and is_input(r)

        invalid_output = (
            is_output(out)
            and op != "XOR"
            and out[1:] != "45"
        )
        invalid_intermediate = (
            op == "XOR"
            and not is_output(out)
            and not both_inputs
        )
        invalid_input = (
            both_inputs
            and not (l[1:] == "00" and r[1:] == "00")
            and (
                (op == "XOR" and not rule_exists("XOR", out)) or
                (op == "AND" and not rule_exists("OR", out))
            )
        )

        return invalid_output or invalid_intermediate or invalid_input

    wrong = {rule for rule in inactive if is_wrong(*rule)}
    outputs = {out for _, _, _, out in wrong}
    return ",".join(sorted(outputs))


def main():
    data = get_data(day=24, year=2024)
    t0 = perf_counter_ns()
    one = part_one(data)
    two = part_two(data)
    t1 = perf_counter_ns()
    print(f"Time: {(t1 - t0) / 1e6:.2f}ms")
    print(f"Part one: {one}")
    print(f"Part two: {two}")


if __name__ == "__main__":
    main()
