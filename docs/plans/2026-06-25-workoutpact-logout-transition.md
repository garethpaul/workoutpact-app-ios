# WorkoutPact Logout Transition Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use executing-plans to implement this plan task-by-task.

**Goal:** Prevent repeated logout taps or stale queued work from presenting more than one login controller.

**Architecture:** Add one controller-owned logout transition reservation and validate it immediately before queued main-thread navigation. Keep Digits/Twitter session clearing and the existing guarded storyboard cast unchanged.

**Tech Stack:** Legacy Swift/UIKit, Python mutation contracts, repository Make verification.

---

## Status: Completed

### Task 1: Add the failing async-flow contract

**Files:**
- Modify: `scripts/test_async_flow_safety_contract.py`

Require a `logoutTransitionInFlight` owner, reject duplicate entry before session logout, claim before queueing, weakly capture the controller, revalidate ownership plus presentation availability on the main queue, and release ownership if destination lookup fails. Run the script and confirm it fails against the current controller.

### Task 2: Implement the minimal transition reservation

**Files:**
- Modify: `workoutpact/ViewController.swift`

Add the boolean owner, guard repeated or overlapping logout requests, claim before clearing sessions, use weak captures in the queued callback, present only while the claim is current and no modal is already shown, and clear the claim when storyboard lookup or casting cannot produce the login controller.

### Task 3: Document and validate

**Files:**
- Modify: `scripts/check_workoutpact_contracts.py`
- Modify: `README.md`
- Modify: `SECURITY.md`
- Modify: `VISION.md`
- Modify: `CHANGES.md`
- Modify: `docs/plans/2026-06-25-workoutpact-logout-transition.md`

Run `python3 scripts/test_async_flow_safety_contract.py`, the portable Python checks available without Ruby, and hosted `make check`. Record the local Ruby limitation and hosted evidence before merge.

## Validation Evidence

- The async-flow contract failed against the original controller on all six
  logout ownership requirements.
- The updated contract passed with twelve hostile mutations rejected.
- Adjacent login lifecycle, login callback ownership, and shake presentation
  mutation suites passed.
- Local `make check` requires Ruby/Psych for semantic workflow parsing; hosted
  verification remains the authoritative complete gate.
