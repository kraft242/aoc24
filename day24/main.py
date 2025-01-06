from aocd import get_data
from time import perf_counter_ns


def parse_data(data):
    active = {}
    initial, combined = data.split("\n\n")
    active = {
        wire: bool(int(value))
        for line in initial.split("\n")
        for wire, value in [line.split(": ")]
    }
    inactive = {
        (l, op, r, rhs)
        for line in combined.split("\n")
        for lhs, rhs in [line.split(" -> ")]
        for l, op, r in [lhs.split(" ")]
    }
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


def part_one(data):
    active, inactive = parse_data(data)

    active = solve(active, inactive)

    result = [
        (wire, int(value))
        for wire, value in active.items()
        if wire.startswith("z")
    ]

    result.sort(reverse=True)

    binary = "".join(str(v) for _, v in result)

    return int(binary, 2)


def part_two(data):
    return 0


def main():
    data = get_data(day=24, year=2024)
#    data = """x00: 1
# x01: 0
# x02: 1
# x03: 1
# x04: 0
# y00: 1
# y01: 1
# y02: 1
# y03: 1
# y04: 1
#
# ntg XOR fgs -> mjb
# y02 OR x01 -> tnw
# kwq OR kpj -> z05
# x00 OR x03 -> fst
# tgd XOR rvg -> z01
# vdt OR tnw -> bfw
# bfw AND frj -> z10
# ffh OR nrd -> bqk
# y00 AND y03 -> djm
# y03 OR y00 -> psh
# bqk OR frj -> z08
# tnw OR fst -> frj
# gnj AND tgd -> z11
# bfw XOR mjb -> z00
# x03 OR x00 -> vdt
# gnj AND wpb -> z02
# x04 AND y00 -> kjc
# djm OR pbm -> qhw
# nrd AND vdt -> hwm
# kjc AND fst -> rvg
# y04 OR y02 -> fgs
# y01 AND x02 -> pbm
# ntg OR kjc -> kwq
# psh XOR fgs -> tgd
# qhw XOR tgd -> z09
# pbm OR djm -> kpj
# x03 XOR y03 -> ffh
# x00 XOR y04 -> ntg
# bfw OR bqk -> z06
# nrd XOR fgs -> wpb
# frj XOR qhw -> z04
# bqk OR frj -> z07
# y03 OR x01 -> nrd
# hwm AND bqk -> z03
# tgd XOR rvg -> z12
# tnw OR pbm -> gnj"""
    t0 = perf_counter_ns()
    one = part_one(data)
    two = part_two(data)
    t1 = perf_counter_ns()
    print(f"Time: {(t1 - t0) / 1e6:.2f}ms")
    print(f"Part one: {one}")
    print(f"Part two: {two}")


if __name__ == "__main__":
    main()
