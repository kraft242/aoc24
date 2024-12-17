from aocd import get_data
from time import perf_counter_ns
import re


def parse_data(data):
    registers = {"A": 0, "B": 0, "C": 0}

    numbers_pattern = r"\d+"
    numbers = re.findall(numbers_pattern, data, flags=re.MULTILINE)
    numbers = list(map(int, numbers))

    registers["A"] = numbers.pop(0)
    registers["B"] = numbers.pop(0)
    registers["C"] = numbers.pop(0)
    return registers, numbers


def part_one(data):
    registers, program = parse_data(data)

    output = []

    def get_combo(op):
        if 0 <= op <= 3:
            return op
        if op == 4:
            return registers["A"]
        if op == 5:
            return registers["B"]
        if op == 6:
            return registers["C"]
        if op == 7:
            raise ValueError("Reserved operation")
        raise ValueError("Invalid operation")

    def execute_instruction(ip, opcode, operand):
        match opcode:
            case 0:
                registers["A"] = registers["A"] // (2 ** get_combo(operand))
                return ip + 2
            case 1:
                registers["B"] = registers["B"] ^ operand
                return ip + 2
            case 2:
                registers["B"] = get_combo(operand) % 8
                return ip + 2
            case 3:
                return operand if registers["A"] != 0 else ip + 2
            case 4:
                registers["B"] = registers["B"] ^ registers["C"]
                return ip + 2
            case 5:
                output.append(get_combo(operand) % 8)
                return ip + 2
            case 6:
                registers["B"] = registers["A"] // (2 ** get_combo(operand))
                return ip + 2
            case 7:
                registers["C"] = registers["A"] // (2 ** get_combo(operand))
                return ip + 2
            case _:
                raise ValueError("Invalid operation")

    ip = 0
    while 0 <= ip < len(program):
        op, combo = program[ip], program[ip + 1]
        ip = execute_instruction(ip, op, combo)

    return ",".join(map(str, output))


def part_two(data):
    return 0


def main():
    data = get_data(day=17, year=2024)
    t0 = perf_counter_ns()
    one = part_one(data)
    two = part_two(data)
    t1 = perf_counter_ns()
    print(f"Time: {(t1 - t0) / 1e6:.2f}ms")
    print(f"Part one: {one}")
    print(f"Part two: {two}")


if __name__ == "__main__":
    main()
