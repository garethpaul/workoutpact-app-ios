# WorkoutPact Keyboard Shift Guard

## Status: Completed

## Context

The protected workout screen moved the whole view when keyboard show and hide
notifications arrived, but it did not track whether the view was already
shifted. Duplicate show notifications could move the screen upward repeatedly,
and duplicate hide notifications could move it back down when it was already in
place.

## Objectives

- Preserve the existing keyboard show and hide animation behavior.
- Track whether the protected screen is currently shifted for the keyboard.
- Ignore duplicate keyboard show notifications while already shifted.
- Ignore keyboard hide notifications when the view is not shifted.
- Cover the keyboard state guard in dependency-free static checks.

## Work Completed

- Added `keyboardIsVisible` state to the protected workout screen.
- Guarded `keyboardWillShow` against duplicate show notifications.
- Guarded `keyboardWillHide` against unpaired hide notifications.
- Updated the static checker with keyboard-shift state coverage.
- Updated README, SECURITY, VISION, and CHANGES.

## Verification

- `python3 scripts/check_workoutpact_contracts.py`
- `make lint`
- `make test`
- `make build`
- `make check`
- `git diff --check`
