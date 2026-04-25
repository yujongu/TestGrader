# Handover

## 1. Current Milestone

Auto-grader harness for Korean Baekjoon-style problems. Each problem has three sibling files (`<id>.py`, `<id>_input.txt`, `<id>_output.txt`) holding 50 test cases. `grader.py` runs every problem's solution against its input, compares stdout to the expected output, and reports per-problem pass/fail. `grader_detail.py` zooms into one problem and shows every failing case for instructor debugging.

10 problems are filled in and all pass: 2480, 2576, 31428, 32642, 34543, 5575, 34750, 25304, 25704, 15593. An 11th, `12000`, was just added to `PROBLEMS` but its files don't exist yet — see Gravel.

## 2. Context & Logic Decisions

- **Why an inline `RUNNER` wrapper that monkey-patches `input()`** — Problems like 25304 have variable-length input per test case (a budget line, then `N`, then `N` items). Fixed `lines_per_case = total / 50` chunking doesn't work there. The wrapper counts `input()` calls during each invocation and reports the count via `__LINES_CONSUMED__` on stderr, so the grader knows where the next case's input begins. We feed all remaining input on every run; the .py reads what it needs and exits.

- **Why `python -c RUNNER` instead of a separate `_runner.py` file** — Keeps the repo to just user-facing files. The wrapper is short and self-contained.

- **Why slice expected as `expected_lines[out_pos : out_pos + len(actual)]`** — Handles problems with variable *output* per case (2576 prints 1 or 2 lines depending on whether any odd numbers were given). Avoids needing a per-problem output-shape manifest. Caveat in Gravel.

- **Why all-or-nothing scoring (any fail → 0/50, stop the loop)** — Explicit user spec: "When one test case fails, stop the loop and make all test cases incorrect for that problem."

- **Why `VISIBLE_CASES = 5`** — Matches the 5-test-case docstring template at the top of every `<id>.py` file. Cases 6-50 are hidden (instructor's secret tests); on failure the grader prints only `Test Case N (hidden)`.

- **Why all `.py` files use `input()` rather than `sys.stdin`** — The wrapper only intercepts `builtins.input`. Direct `sys.stdin.readline()` would not be counted and would desync the input pointer. Every existing solution uses `input()`, so this is fine, but it's a soft constraint on future solutions.

## 3. The 'Gravel'

- **`12000` is in `PROBLEMS` but has no files.** `grader.py:22` lists it; `12000.py`, `12000_input.txt`, `12000_output.txt` don't exist. Running the grader will print `[ -- ] 12000  12000.py not found` and the overall total will read `10/11`.

- **`grader_detail.py` is stale.** It still uses the old fixed-chunk slicing (`len(input_lines) // NUM_TEST_CASES`) and bails with `not divisible by 50` on any variable-input problem (25304 has 257 input lines). The Makefile's `make detail PROB=...` target still points at it. Either port the wrapper-based runner from `grader.py` into it, or delete it and fold the detail view into `grader.py` behind a flag.

- **Empty-output false-positive in variable-output mode.** If a buggy `.py` prints nothing and the expected slice for that case happens to also be empty (only possible at end-of-input), the comparison `actual == expected_chunk` returns `True`. All-or-nothing scoring + the `EOFError`-on-stdin-exhaustion path masks this for now, but it's latent.

- **One subprocess per test case = ~500 Python interpreter startups per full grade run.** On Windows this takes a few seconds. Fine for a class of ~10 problems; would want to reconsider at 100+.

- **Makefile assumes `make` is on PATH.** Plain Windows doesn't have it. Direct `python grader.py` works as a fallback; mention this when handing off to a TA.

## 4. Next Immediate Step

Either create the three missing skeleton files for problem 12000 to bring the suite back to a clean `11/11`:

```
Write C:\Users\yujon\Desktop\Dev\TestCaseGen\12000.py
Write C:\Users\yujon\Desktop\Dev\TestCaseGen\12000_input.txt
Write C:\Users\yujon\Desktop\Dev\TestCaseGen\12000_output.txt
```

(use the same docstring template as the other skeletons — see `15593.py` lines 1-27 for the layout)

— or remove `12000` from the `PROBLEMS` list at `grader.py:22` if it was added by accident.
