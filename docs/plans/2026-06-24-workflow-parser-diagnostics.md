# Workflow Parser Diagnostics Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use executing-plans to implement this plan task-by-task.

**Goal:** Report YAML parser infrastructure failures truthfully and prevent them from satisfying workflow mutation checks.

**Architecture:** Keep the existing Ruby/Psych semantic parser, but return parser errors separately from the reviewed/not-reviewed workflow result. The aggregate checker only evaluates semantic assertions when parsing succeeded, and a focused stdlib test forces a missing-Ruby failure to verify the boundary.

**Tech Stack:** Python 3 standard library, Ruby/Psych, GNU Make

Status: Completed

---

### Task 1: Reproduce Missing Parser Diagnostics

**Files:**
- Create: `scripts/test_check_workoutpact_contracts.py`
- Test: `scripts/test_check_workoutpact_contracts.py`

**Step 1: Write the failing test**

Patch `subprocess.run` to raise `FileNotFoundError`, call the real checker
`main()`, and capture its output.

**Step 2: Run test to verify it fails**

Run: `python3 scripts/test_check_workoutpact_contracts.py`

Expected: FAIL because the parser-unavailable diagnostic is omitted while
checkout-policy failures are reported.

### Task 2: Preserve Parser Failure State

**Files:**
- Modify: `scripts/check_workoutpact_contracts.py`
- Test: `scripts/test_check_workoutpact_contracts.py`

**Step 1: Return structured review results**

Return the semantic reviewed/not-reviewed result alongside parser errors.

**Step 2: Guard semantic assertions**

Append parser errors directly and skip positive and negative workflow
assertions that did not parse.

**Step 3: Run test to verify it passes**

Run: `python3 scripts/test_check_workoutpact_contracts.py`

Expected: PASS with the parser diagnostic present and derivative workflow
messages absent.

### Task 3: Integrate the Regression Test

**Files:**
- Modify: `Makefile`

**Step 1: Add compile coverage**

Include the new test in the existing `py_compile` command.

**Step 2: Add execution coverage**

Run the focused test from the existing `test` target.

**Step 3: Run verification**

Run: `make check`

Expected: PASS on a host with Python, Ruby/Psych, GNU Make, and the repository
tooling; report the Xcode boundary when Xcode is unavailable.

### Task 4: Close the Maintenance Cycle

**Files:**
- Modify: `CHANGES.md`
- Modify: `docs/plans/2026-06-24-workflow-parser-diagnostics.md`

**Step 1: Record validation evidence**

Add the focused RED/GREEN results, full gate result, hosted checks, review, and
remaining platform boundary to `CHANGES.md`.

**Step 2: Mark the plan complete**

Change `Status: In Progress` to `Status: Completed` only after `make check`
passes in a Ruby-capable environment and the PR review gate is clean.

Completed with Ubuntu 24.04, Ruby 3.2.3, Psych 5.0.1, Python 3.12.3, and GNU
Make 4.3. Correctness, quality, and security reviewers approved the final diff.

**Step 3: Commit**

```bash
git add Makefile CHANGES.md docs/plans/2026-06-24-workflow-parser-diagnostics.md scripts/check_workoutpact_contracts.py scripts/test_check_workoutpact_contracts.py
git commit -m "fix: surface workflow parser failures"
```
