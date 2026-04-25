# Handover

## 1. Current State

Auto-grader for Korean Baekjoon-style problems. Each problem has three sibling files (`<id>.py`, `<id>_input.txt`, `<id>_output.txt`) holding 50 test cases. `grader.py` runs each solution against its input, compares stdout to expected output, and reports per-problem results.

11 problems active: 2480, 2576, 31428, 32642, 34543, 5575, 34750, 25304, 25704, 15593, 12000. 10 pass (50/50). `12000` scores 6/50 — its algorithm is wrong (see Gravel).

## 2. Key Design Decisions

- **Batch runner (`BATCH_RUNNER`)** — One subprocess per problem runs all 50 cases via `exec()` inside a loop. Reduces 550 Python interpreter startups to 11. Each case gets a fresh globals dict, patched `builtins.input`, and captured stdout via `io.StringIO`. Results stream back as JSON lines on stderr.

- **Per-case 10s kill timer** — `threading.Timer` fires `os._exit(1)` if a case hangs. Works on Windows and Mac. The parent detects a timeout when a case's JSON entry is missing from stderr.

- **Variable-length input tracking** — `input()` calls are counted per case via the patch. `in_pos` advances by `consumed` after each case, so problems like 25304 (budget + N items) work without a per-problem line-count manifest.

- **Variable-length output** — Expected lines are sliced as `expected_lines[out_pos : out_pos + len(actual)]`, so 2576 (prints 1 or 2 lines) works without a manifest.

- **Partial scoring** — On first failure the loop stops and reports how many cases passed before it (e.g., `6/50`), not 0.

- **All failures show full detail** — No hidden-case concept. Input, expected, and actual output are always printed.

- **`input()` only, not `sys.stdin`** — The patch only intercepts `builtins.input`. Solutions using `sys.stdin.readline()` would desync the input pointer.

## 3. Gravel

- **`12000` algorithm is wrong.** The code minimizes `sum(r[i] * ((i-k) % n))` over all k. For `r=[1,2,3,4,5]` it finds k=2 → 25, but expected is 30. Cases 1–6 pass by coincidence; case 7 is the first to expose the bug. The docstring also shows pairs as input format but the code reads one int per line — likely the wrong algorithm was submitted.

- **`grader_detail.py` is stale.** Still uses fixed-chunk slicing; breaks on variable-input problems. Either update it or delete it.

- **Empty-output false-positive.** If a buggy solution prints nothing and the expected slice is also empty (end-of-input edge case), the comparison passes silently.

- **Makefile assumes `make` is on PATH.** Windows users should run `python grader.py` directly.
