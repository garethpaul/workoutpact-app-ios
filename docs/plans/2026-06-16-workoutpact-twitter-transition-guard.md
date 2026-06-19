# WorkoutPact Twitter Transition Guard

Status: Completed

## Priority

P1 navigation integrity. Multiple successful Twitter login completions can be
queued before the first one presents the two-factor screen, allowing duplicate
modal presentations from one visible login context.

## Problem

The current callback correctly rejects errors, weakly captures the controller,
returns after dismissal, and presents on the main queue. It does not record that
a successful transition has already been claimed. Main-queue blocks execute
serially, but each block sees the same active login context and can independently
instantiate and present `TwoFactorViewController`.

## Requirements

1. Permit at most one successful Twitter-to-two-factor transition for the
   lifetime of the login controller.
2. Acquire transition ownership on the main queue after controller, lifecycle,
   presentation, storyboard, and destination validation, immediately before
   presentation.
3. Keep transition eligibility consumed when the login screen appears again so
   delayed duplicate callbacks cannot become valid after a modal round trip.
4. Preserve error/cancellation behavior, weak captures, lifecycle rejection,
   storyboard identifier and cast, and main-thread presentation.
5. Add mutation-sensitive static coverage, maintained guidance, and completed
   verification evidence.

## Implementation Units

### U1: Add single-transition state

**Files:** `workoutpact/LoginViewController.swift`

- Track whether the login controller has claimed its successful transition.
- Do not reset that state in `viewWillAppear`.
- Reject a second successful main-queue completion, validate the destination,
  and claim ownership immediately before presentation.

**Test scenarios:**

- First successful callback in an active context claims and presents.
- A second queued success in the same appearance returns before storyboard work.
- Reappearance preserves the guard so delayed duplicate delivery remains inert.
- Errors, missing sessions, dismissed contexts, and deallocated controllers
  remain inert.

### U2: Lock the contract and evidence

**Files:** `scripts/check_workoutpact_contracts.py`, `README.md`, `SECURITY.md`,
`VISION.md`, `CHANGES.md`,
`docs/plans/2026-06-16-workoutpact-twitter-transition-guard.md`

- Require state declaration, appearance reset, guard ordering, ownership claim,
  weak capture, and completed plan evidence.
- Reject isolated implementation, guidance, registration, and plan mutations.

## Scope Boundaries

- Do not modernize Swift, replace TwitterKit, alter authentication UX, or change
  storyboard/project metadata.
- Do not change Digits authentication, payment tokenization, billing behavior,
  or existing callback-generation boundaries.
- Keep the pull-request stack open and retain base-first merge ordering.

## Verification

- Run the focused Twitter lifecycle and transition contracts.
- Run repository and external-directory `make check` gates available on Linux.
- Reject isolated state, reset, ordering, guard, claim, guidance, registration,
  and plan-evidence mutations.
- Audit the exact diff, generated artifacts, credentials, conflict markers,
  binaries, large files, modes, and whitespace.

## Success Criteria

- One visible login appearance can present at most one two-factor controller.
- Returning to the login screen restores eligibility for a later successful login.
- Existing weak ownership and stale-callback protections remain intact.

## Verification Completed

- The focused transition contract and existing callback-ownership contract
  passed; 14 lifecycle mutations were rejected by the combined lifecycle gate.
- Repository and external-directory `make check` passed every portable contract;
  both runs truthfully skipped unavailable `xcodebuild`.
- Checker and mutation-script compilation passed.
- Exact intended-path, generated-artifact and credential-pattern audits passed,
  together with conflict-marker, binary, large-file, mode, and whitespace checks.
