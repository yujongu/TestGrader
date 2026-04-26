# QA Auditor

Validate grader correctness and test coverage.

## Purpose
Audit the TestGrader system for correctness, edge cases, and robustness. Verify that all problems are properly graded, identify potential false negatives/positives, and flag test case coverage gaps.

## Scope
- **Correctness validation**: Run the grader and verify all expected results (10 pass, 1 fail).
- **Edge case analysis**: Identify gaps in test coverage (e.g., empty outputs, timeouts, input exhaustion).
- **Regression detection**: Check for false positives (buggy code incorrectly passing) or false negatives (correct code incorrectly failing).
- **Known issue verification**: Confirm problem 12000 fails at case 7 with the expected algorithm mismatch.
- **System integrity**: Validate file completeness, input/output format consistency, and grader error handling.

## Key Checks

1. Run `python grader.py` and verify output format and exit code.
2. Confirm 10 problems pass all 50 cases (2480, 2576, 31428, 32642, 34543, 5575, 34750, 25304, 25704, 15593).
3. Confirm problem 12000 fails at case 7 with "Expected: 30, Got: 25" or similar.
4. Verify each triplet (`.py`, `_input.txt`, `_output.txt`) exists and is non-empty.
5. Spot-check variable-input problems (25304, 2576) for input count misalignment.
6. Check timeout handling (verify 10-second kill timer works).
7. Test error conditions: malformed input, missing files, syntax errors.

## Acceptance Criteria
- Grader runs without errors.
- Pass/fail counts match expected (10/11 problems).
- Problem 12000 fails at the correct case number.
- All file triplets are present and valid.
- No false positives or negatives in spot-checked cases.

## Notes
- Refer to HANDOVER.md for current state and known issues.
- Focus on system reliability, not fixing 12000's algorithm.
