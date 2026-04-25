"""Grade problem solutions by running each .py once per test case.

For each problem, the .py is invoked NUM_TEST_CASES times. A small wrapper
counts how many input() calls each invocation makes, so the grader can
advance the input pointer for the next case (this handles problems with
variable-length input per case, like 25304).

Scoring is all-or-nothing: as soon as any test case fails (wrong output,
runtime error, or timeout), the loop stops and the problem is marked
0/NUM_TEST_CASES. If every case passes, the problem is NUM_TEST_CASES/NUM_TEST_CASES.

When the failing case falls within VISIBLE_CASES, its input/expected/got are
printed. Failures in cases beyond VISIBLE_CASES are hidden — only the case
number is shown.
"""

import os
import subprocess
import sys
from pathlib import Path

PROBLEMS = [2480, 2576, 31428, 32642, 34543, 5575, 34750, 25304, 25704, 15593, 12000]
NUM_TEST_CASES = 50
VISIBLE_CASES = 5
ROOT = Path(__file__).parent

if os.name == "nt":
    os.system("")  # enable ANSI escape sequences in Windows terminals

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"

# Inline wrapper: runs a target .py and reports input() call count via stderr.
RUNNER = r'''
import builtins, sys
target = sys.argv[1]
_real_input = builtins.input
_count = 0
def _counting_input(prompt=""):
    global _count
    line = _real_input(prompt)
    _count += 1
    return line
builtins.input = _counting_input
try:
    with open(target, encoding="utf-8") as f:
        code = f.read()
    exec(compile(code, target, "exec"), {"__name__": "__main__", "__file__": target})
except SystemExit:
    pass
finally:
    sys.stderr.write(f"\n__LINES_CONSUMED__:{_count}\n")
    sys.stderr.flush()
'''


def run_one_case(py, remaining_input):
    try:
        result = subprocess.run(
            [sys.executable, "-c", RUNNER, str(py)],
            input=remaining_input,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except subprocess.TimeoutExpired:
        return None, 0, "timeout after 10s"

    consumed = 0
    other_err = []
    for line in result.stderr.splitlines():
        if line.startswith("__LINES_CONSUMED__:"):
            try:
                consumed = int(line.split(":", 1)[1])
            except ValueError:
                pass
        elif line.strip():
            other_err.append(line)

    if result.returncode != 0:
        msg = other_err[-1] if other_err else f"non-zero exit ({result.returncode})"
        return None, consumed, msg

    return result.stdout.splitlines(), consumed, None


def grade(problem):
    py = ROOT / f"{problem}.py"
    inp = ROOT / f"{problem}_input.txt"
    expected_path = ROOT / f"{problem}_output.txt"

    for path in (py, inp, expected_path):
        if not path.exists():
            return ("MISSING", 0, None, f"{path.name} not found")

    input_text = inp.read_text()
    expected_text = expected_path.read_text()
    if not input_text.strip() or not expected_text.strip():
        return ("EMPTY", 0, None, "input or output file is empty")

    input_lines = input_text.splitlines()
    expected_lines = expected_text.splitlines()

    in_pos = 0
    out_pos = 0

    for i in range(NUM_TEST_CASES):
        remaining = "\n".join(input_lines[in_pos:]) + "\n"
        actual, consumed, err = run_one_case(py, remaining)

        if err is not None:
            fail = {
                "case": i + 1,
                "input": input_lines[in_pos : in_pos + max(consumed, 1)],
                "expected": None,
                "actual": None,
                "error": err,
            }
            return ("FAIL", 0, fail, None)

        expected_chunk = expected_lines[out_pos : out_pos + len(actual)]
        if actual != expected_chunk:
            fail = {
                "case": i + 1,
                "input": input_lines[in_pos : in_pos + consumed],
                "expected": expected_chunk,
                "actual": actual,
                "error": None,
            }
            return ("FAIL", 0, fail, None)

        in_pos += consumed
        out_pos += len(actual)

    return ("PASS", NUM_TEST_CASES, None, None)


def print_block(label, lines, color, indent):
    print(f"{indent}{color}{label}{RESET}")
    if not lines:
        print(f"{indent}  {DIM}(no output){RESET}")
        return
    for line in lines:
        print(f"{indent}  {line}")


def print_failure(fail):
    indent = "      "
    if fail["case"] > VISIBLE_CASES:
        print(f"    {RED}[X]{RESET} {BOLD}Test Case {fail['case']}{RESET} {DIM}(hidden){RESET}")
        print()
        return
    print(f"    {RED}[X]{RESET} {BOLD}Test Case {fail['case']}{RESET}")
    print_block("Input:", fail["input"], CYAN, indent)
    if fail["error"]:
        print(f"{indent}{RED}Error:{RESET} {fail['error']}")
        if fail["expected"]:
            print_block("Expected:", fail["expected"], CYAN, indent)
    else:
        print_block("Expected:", fail["expected"], CYAN, indent)
        print_block("Got:", fail["actual"], YELLOW, indent)
    print()


def main():
    print(
        f"\n{BOLD}Problem Grader{RESET}  "
        f"{DIM}({NUM_TEST_CASES} cases/problem; cases 1-{VISIBLE_CASES} visible, "
        f"{VISIBLE_CASES + 1}-{NUM_TEST_CASES} hidden){RESET}"
    )
    print(f"{DIM}{'=' * 70}{RESET}")

    overall_passed = 0
    for prob in PROBLEMS:
        status, passed, fail, msg = grade(prob)

        if status == "PASS":
            overall_passed += 1
            print(f"  {GREEN}[PASS]{RESET}  {BOLD}{prob:<6}{RESET}  {GREEN}{passed}/{NUM_TEST_CASES}{RESET} cases passed")
        elif status == "FAIL":
            print(f"  {RED}[FAIL]{RESET}  {BOLD}{prob:<6}{RESET}  {RED}{passed}/{NUM_TEST_CASES}{RESET} cases passed")
            print()
            print_failure(fail)
        else:
            print(f"  {YELLOW}[ -- ]{RESET}  {BOLD}{prob:<6}{RESET}  {DIM}{msg}{RESET}")

    print(f"{DIM}{'=' * 70}{RESET}")
    color = GREEN if overall_passed == len(PROBLEMS) else (YELLOW if overall_passed > 0 else RED)
    print(f"  {BOLD}{color}{overall_passed}/{len(PROBLEMS)} problems passed{RESET}\n")

    sys.exit(0 if overall_passed == len(PROBLEMS) else 1)


if __name__ == "__main__":
    main()
