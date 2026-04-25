"""Grade problem solutions by running each .py once per problem.

A single subprocess is launched per problem. Inside it, all NUM_TEST_CASES
test cases are executed back-to-back via exec(), with stdout captured and
input() patched so the grader can track how many lines each case consumed
(needed for variable-length-input problems like 25304).

A per-case timer kills the subprocess via os._exit if any single case runs
longer than 10 seconds.

Results are streamed back as JSON lines on stderr, one per case.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

PROBLEMS = [2480, 2576, 31428, 32642, 34543, 5575, 34750, 25304, 25704, 15593, 12000]
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

# Runs all test cases for one .py in a single interpreter.
# Each case gets a fresh globals dict, captured stdout, and a 10s kill timer.
# Results are written as JSON to stderr: one __CASE__:{...} line per case.
BATCH_RUNNER = r'''
import builtins, io, json, os, sys, threading, traceback

target = sys.argv[1]
num_cases = int(sys.argv[2])

all_lines = sys.stdin.read().splitlines()
pos = 0

with open(target, encoding="utf-8") as f:
    code = f.read()
compiled = compile(code, target, "exec")

for case_idx in range(num_cases):
    case_start = pos
    out_buf = io.StringIO()

    def _patched_input(prompt=""):
        global pos
        if pos >= len(all_lines):
            raise EOFError()
        v = all_lines[pos]
        pos += 1
        return v

    builtins.input = _patched_input
    sys.stdout, old_stdout = out_buf, sys.stdout

    timer = threading.Timer(10.0, lambda: os._exit(1))
    timer.start()
    error = None
    try:
        exec(compiled, {"__name__": "__main__", "__file__": target})
    except SystemExit:
        pass
    except EOFError:
        error = "EOFError: ran out of input"
    except Exception:
        error = traceback.format_exc().strip().splitlines()[-1]
    finally:
        timer.cancel()
        sys.stdout = old_stdout

    consumed = pos - case_start
    sys.stderr.write("__CASE__:" + json.dumps({
        "idx": case_idx,
        "consumed": consumed,
        "output": out_buf.getvalue(),
        "error": error,
    }) + "\n")
    sys.stderr.flush()
'''


def run_problem(py, input_text, num_cases):
    try:
        proc = subprocess.run(
            [sys.executable, "-c", BATCH_RUNNER, str(py), str(num_cases)],
            input=input_text,
            capture_output=True,
            text=True,
            timeout=10 * num_cases + 5,
        )
    except subprocess.TimeoutExpired:
        return None

    results = {}
    for line in proc.stderr.splitlines():
        if line.startswith("__CASE__:"):
            try:
                data = json.loads(line[9:])
                results[data["idx"]] = data
            except (json.JSONDecodeError, KeyError):
                pass
    return results


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

    case_results = run_problem(py, input_text, NUM_TEST_CASES)

    in_pos = 0
    out_pos = 0

    for i in range(NUM_TEST_CASES):
        if case_results is None or i not in case_results:
            fail = {
                "case": i + 1,
                "input": input_lines[in_pos : in_pos + 1],
                "expected": None,
                "actual": None,
                "error": "timeout after 10s",
            }
            return ("FAIL", i, fail, None)

        case = case_results[i]
        consumed = case["consumed"]
        err = case["error"]

        if err is not None:
            fail = {
                "case": i + 1,
                "input": input_lines[in_pos : in_pos + max(consumed, 1)],
                "expected": None,
                "actual": None,
                "error": err,
            }
            return ("FAIL", i, fail, None)

        actual = case["output"].splitlines()
        expected_chunk = expected_lines[out_pos : out_pos + len(actual)]
        if actual != expected_chunk:
            fail = {
                "case": i + 1,
                "input": input_lines[in_pos : in_pos + consumed],
                "expected": expected_chunk,
                "actual": actual,
                "error": None,
            }
            return ("FAIL", i, fail, None)

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
        f"{DIM}({NUM_TEST_CASES} cases/problem){RESET}"
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
