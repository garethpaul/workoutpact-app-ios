# Fix: Workflow parser diagnostics

**Date:** 2026-06-24
**Status:** ✅ Fixed
**Severity:** Medium
**Commit:** Included in the PR commit that adds this document
**Investigation Tier:** STANDARD

## Problem

When Ruby/Psych could not execute, the static contract checker reported that
the immutable checkout was misconfigured even when the workflow correctly set
`persist-credentials: false`. The same infrastructure failure could count as a
successful rejection of hostile workflow mutations.

**Root Cause:**

The YAML parser returned useful infrastructure errors, but the workflow review
layer collapsed them into the same boolean used for semantic rejection.

## Investigation Summary

- **Code tracer**: followed `make check` through the Ruby parser and found the
  error-to-boolean collapse.
- **History hunter**: identified commit `035b81c` as the parser and diagnostic
  boundary introduction.
- **Dependency mapper**: found every aggregate Make entry point and mutation
  suite was affected.
- **Hypothesis challenger**: independently confirmed missing Ruby and refuted
  an actual checkout YAML defect.

## Solution

Workflow review now returns parser errors separately from semantic results.
The aggregate checker reports infrastructure errors directly and stops before
semantic or mutation assertions that did not execute.

## Files Modified

- `scripts/check_workoutpact_contracts.py` — preserves parser error state.
- `scripts/test_check_workoutpact_contracts.py` — covers baseline and
  mutation-time parser failures.
- `scripts/test-makefile-root.sh` — mirrors the new test in authority fixtures.
- `Makefile` — compiles and executes the regression test.

## Testing

- ✅ Regression tests fail against the old checker and pass against the fix.
- ✅ All 35 Make authority cases pass.
- ✅ Ubuntu 24.04 `/usr/bin/make check` passes with Ruby 3.2.3, Psych 5.0.1,
  Python 3.12.3, and GNU Make 4.3.

## Review Results

- Correctness: ✅ APPROVED
- Quality: ✅ APPROVED
- Security: ✅ APPROVED

## Impact

Parser outages now fail closed with truthful diagnostics, and mutation checks
cannot pass without semantic YAML evaluation.
