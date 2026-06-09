---
title: WorkoutPact Logout Navigation Guard
status: completed
date: 2026-06-08
origin: user-requested continuous engineering quality loop
execution: code
---

# WorkoutPact Logout Navigation Guard

Status: Completed

## Problem Frame

The protected controller logged out of Digits and Twitter, then force-unwrapped
`self.storyboard!` before presenting the login controller. If the controller is
not storyboard-backed in a test or future embedding, logout navigation can crash
after credentials have already been cleared.

## Scope Boundaries

- Preserve the existing logout behavior and target login controller.
- Do not change Digits/Twitter session clearing.
- Do not modernize Swift syntax beyond the minimal guard.

## Implementation

- Guard `self.storyboard` before instantiating `LoginViewController`.
- Extend the static contract checker to reject `self.storyboard!` in the
  protected controller and require this plan.

## Verification

- `python3 scripts/check_workoutpact_contracts.py`
- `make check`
- `git diff --check`
