# WorkoutPact Weak Twitter Login Callback

Status: Planned

## Problem

`LoginViewController` owns the Twitter login button through its view hierarchy,
and `TWTRLogInButton` retains its login completion. The completion currently
captures the controller strongly, creating a controller-view-button-closure
retain cycle that can keep the dismissed login screen alive indefinitely.

## Requirements

1. Capture `LoginViewController` weakly in the TwitterKit login completion.
2. Capture it weakly again in the queued main-thread presentation block so the
   dispatch queue cannot extend a dismissed controller lifecycle.
3. Promote the weak reference only inside the main-thread block and return
   without presentation when the controller no longer exists.
4. Preserve cancellation/error behavior, lifecycle-state rejection, main-queue
   ordering, guarded storyboard lookup/cast, identifier, and presentation.
5. Add mutation-sensitive static coverage for either missing weak capture,
   promotion outside the main block, presentation through `self`, and removed
   ownership-contract registration.
6. Synchronize README, security, vision, changelog, and completed-plan evidence.

## Scope Boundaries

- Do not modernize Swift, replace TwitterKit, change authentication UX, or
  alter storyboard/project metadata.
- Do not change the existing stale-callback lifecycle boundary.
- Do not merge or close the pull-request stack without explicit authorization.

## Implementation Units

### U1. Add callback ownership contracts

- **Files:** `scripts/check_workoutpact_contracts.py`, a focused mutation test.
- Require weak outer and inner captures, main-block promotion, lifecycle
  ordering, and presentation through the promoted controller.

### U2. Break the login-button retain cycle

- **Files:** `workoutpact/LoginViewController.swift`.
- Add weak capture lists and use a promoted controller only inside the queued
  main-thread block.

### U3. Preserve maintained guidance

- **Files:** `README.md`, `SECURITY.md`, `VISION.md`, `CHANGES.md`.
- Record the weak callback ownership boundary without claiming SDK support.

## Verification

- Pending implementation.
- Run focused ownership contracts and mutations, then repository-root and
  external-directory `make check` with explicit timeouts.
- Audit the exact diff, generated artifacts, conflict markers, file modes,
  whitespace, and added credential-like values.
- Record Linux's unavailable Xcode/simulator boundary without weakening the
  portable gate.
