# WorkoutPact Storyboard Cast Guards

## Status: Completed

## Context

Login and logout navigation already guarded optional storyboard lookup, but the
instantiated controllers were still force-cast with `as!`. A missing storyboard
identifier or unexpected controller class could crash those auth navigation
paths.

## Objectives

- Preserve successful Twitter login navigation into phone verification.
- Preserve logout navigation back to the login screen.
- Avoid forced storyboard controller casts.
- Extend static contract coverage for guarded navigation.

## Work Completed

- Replaced the `TwoFactorViewController` forced cast with a guarded `as?` cast.
- Replaced the `LoginViewController` forced cast with a guarded `as?` cast.
- Added static checker coverage for both storyboard cast guards.
- Updated README, VISION, and CHANGES.

## Verification

- `python3 scripts/check_workoutpact_contracts.py`
- `make check`
- `make verify`
- `git diff --check`

## Follow-Up Candidates

- Add user-visible fallback handling when storyboard identifiers are missing.
- Add simulator verification notes for auth/logout navigation.
