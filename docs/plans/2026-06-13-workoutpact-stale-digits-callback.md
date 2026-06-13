# WorkoutPact Stale Digits Callback Guard

Status: Planned

## Goal

Prevent a delayed successful Digits authentication callback from navigating to
protected content after the two-factor screen has been covered or dismissed.

## Scope

- Track whether `TwoFactorViewController` is currently visible.
- Reject authentication requests while the controller is inactive.
- Recheck visibility on the main-thread success callback before performing the
  protected segue.
- Preserve Digits appearance, cancellation and error handling, main-thread UI
  dispatch, storyboard identifiers, and the archival Swift 1/iOS 8.1 boundary.
- Add callback-scoped ordering contracts and hostile mutation coverage.

## Verification Plan

- Run the portable static contract directly and through `make check` from both
  the repository and an external working directory.
- Compile the Python checker and run `git diff --check`.
- Verify hostile mutations reject missing lifecycle assignments, missing or
  inverted request/completion guards, guards ordered after protected work, and
  stale plan status.
- Inspect the exact diff for generated artifacts, vendored changes, project
  metadata drift, and credential-like additions.
- Do not claim simulator, physical-device, or current-SDK behavior when
  `xcodebuild` is unavailable.
