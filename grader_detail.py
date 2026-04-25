"""Detailed grader for a single problem - shows failing test cases for the instructor.

Usage:
    python grader_detail.py <problem_number>
"""

import os
import subprocess
import sys
from pathlib import Path

NUM_TEST_CASES = 50
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


def run_test_case(py, chunk_lines):
    chunk = "\n".join(chunk_lines) + "\n"
    try:
        result = subprocess.run(
            [sys.executable, str(py)],
            input=chunk,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except subprocess.TimeoutExpired:
        return None, "timeout after 10s"
    if result.returncode != 0:
        err = result.stderr.strip().splitlines()
        return None, err[-1] if err else f"non-zero exit ({result.returncode})"
    return result.stdout.splitlines(), None


def print_block(label, lines, color):
    print(f"  {color}{label}{RESET}")
    if not lines:
        print(f"    {DIM}(no output){RESET}")
        return
    for line in lines:
        print(f"    {line}")


def grade_detail(problem):
    py = ROOT / f"{problem}.py"
    inp = ROOT / f"{problem}_input.txt"
    expected_path = ROOT / f"{problem}_output.txt"

    for path in (py, inp, expected_path):
        if not path.exists():
            print(f"{RED}Error: {path.name} not found{RESET}")
            return 1

    input_text = inp.read_text()
    expected_text = expected_path.read_text()

    if not input_text.strip() or not expected_text.strip():
        print(f"{YELLOW}Problem {problem}: input or output file is empty (skeleton not filled in){RESET}")
        return 1

    input_lines = input_text.splitlines()
    expected_lines = expected_text.splitlines()

    if len(input_lines) % NUM_TEST_CASES != 0:
        print(
            f"{RED}Error: input has {len(input_lines)} lines "
            f"(not divisible by {NUM_TEST_CASES}){RESET}"
        )
        return 1

    lines_per_case = len(input_lines) // NUM_TEST_CASES
    fixed_out = len(expected_lines) % NUM_TEST_CASES == 0
    out_per_case = len(expected_lines) // NUM_TEST_CASES if fixed_out else None

    layout = (
        f"{lines_per_case} input line(s)/case, "
        + (f"{out_per_case} output line(s)/case" if fixed_out else "variable output")
    )
    print(f"\n{BOLD}Problem {problem}{RESET}  {DIM}({NUM_TEST_CASES} cases, {layout}){RESET}")
    print(f"{DIM}{'-' * 70}{RESET}")

    failed = []
    pos = 0
    for i in range(NUM_TEST_CASES):
        chunk = input_lines[i * lines_per_case : (i + 1) * lines_per_case]
        actual, err = run_test_case(py, chunk)

        if err:
            expected = (
                expected_lines[i * out_per_case : (i + 1) * out_per_case]
                if fixed_out
                else None
            )
            failed.append({
                "case": i + 1,
                "input": chunk,
                "actual": None,
                "expected": expected,
                "error": err,
            })
            continue

        if fixed_out:
            expected = expected_lines[i * out_per_case : (i + 1) * out_per_case]
        else:
            expected = expected_lines[pos : pos + len(actual)]
            pos += len(actual)

        if actual != expected:
            failed.append({
                "case": i + 1,
                "input": chunk,
                "actual": actual,
                "expected": expected,
                "error": None,
            })

    passed = NUM_TEST_CASES - len(failed)
    color = GREEN if not failed else RED
    print(f"  {BOLD}{color}{passed}/{NUM_TEST_CASES} test cases passed{RESET}\n")

    if not failed:
        return 0

    print(f"{BOLD}Failed test cases:{RESET}\n")
    for f in failed:
        print(f"{RED}{BOLD}Test Case {f['case']}{RESET}")
        print_block("Input:", f["input"], CYAN)
        if f["error"]:
            print(f"  {RED}Error:{RESET} {f['error']}")
            if f["expected"] is not None:
                print_block("Expected:", f["expected"], CYAN)
        else:
            print_block("Expected:", f["expected"], CYAN)
            print_block("Actual:", f["actual"], YELLOW)
        print()

    return 1


def main():
    if len(sys.argv) != 2:
        print(f"Usage: python {Path(__file__).name} <problem_number>")
        sys.exit(2)
    try:
        problem = int(sys.argv[1])
    except ValueError:
        print(f"{RED}Invalid problem number: {sys.argv[1]}{RESET}")
        sys.exit(2)

    sys.exit(grade_detail(problem))


if __name__ == "__main__":
    main()
