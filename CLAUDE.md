# TestGrader
Auto-grader for competitive programming problems (Korean Baekjoon-style). Grades solutions by running them against 50 test cases per problem.

## Overview
The grader orchestrates problem solutions through a specialized batch runner that executes all test cases for a single problem in one Python interpreter process, reducing startup overhead from 550 interpreter launches down to 11 (one per problem).

**Current Status:** 11 problems, 10 fully passing (50/50 cases), 1 with wrong algorithm (12000: 6/50).

## Key Components

### `grader.py`
Main entry point. For each problem: reads input and expected output files, spawns a subprocess running the batch runner, parses JSON results, and reports per-problem success/failure with full test case details.

**Core design principles:**
- **One subprocess per problem** via `BATCH_RUNNER` embedded string. All 50 cases execute in one Python process.
- **Fresh execution context per case**: Each case gets its own `globals` dict, captured stdout via `io.StringIO`, and patched `builtins.input`.
- **10-second per-case timeout** via `threading.Timer` firing `os._exit(1)`. Works on Windows and macOS.
- **Variable-length input/output tracking**: Uses `input()` call counting and dynamic output slicing so problems with unpredictable case sizes (e.g., 25304 with budget + N items) work without per-problem manifests.
- **Partial scoring**: On first failure, stops and reports how many cases passed (e.g., `6/50`), not zero.
- **Full failure details**: No hidden cases. Input, expected, and actual output always shown.

**Important limitation:** Only intercepts `builtins.input`. Solutions using `sys.stdin.readline()` will desync the input pointer and fail.

### `grader_detail.py`
Stale utility for per-problem detailed output. Uses fixed-chunk slicing and breaks on variable-input problems. Candidate for deletion or update.

### Test Data
Each problem is a triplet:
- `<id>.py` — solution code
- `<id>_input.txt` — 50 test cases (newline-separated inputs)
- `<id>_output.txt` — 50 expected outputs (newline-separated)

## Running the Grader

```bash
make grade
# or
python3 grader.py
```

## Development Notes

- Add new problems: Create `<id>.py`, `<id>_input.txt`, `<id>_output.txt` triplets and append the ID to `PROBLEMS` in `grader.py`.
- Debugging: The batch runner logs full tracebacks for exceptions, consumed input count, and actual output for each case.
- Performance: Single interpreter per problem is ~10x faster than per-case spawning; timeout safety is maintained via thread-based killing.
