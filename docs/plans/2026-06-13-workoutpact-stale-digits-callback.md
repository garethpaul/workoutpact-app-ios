# WorkoutPact Stale Digits Callback Guard

Status: Completed

## Goal

Prevent a delayed successful Digits authentication callback from navigating to
protected content after the two-factor controller has been dismissed or
removed from its presentation hierarchy.

## Scope

- Track whether `TwoFactorViewController` remains active in its presentation
  hierarchy without treating the Digits overlay itself as dismissal.
- Reject authentication requests while the controller context is inactive.
- Recheck the active presentation context on the main-thread success callback
  before performing the protected segue.
- Preserve Digits appearance, cancellation and error handling, main-thread UI
  dispatch, storyboard identifiers, and the archival Swift 1/iOS 8.1 boundary.
- Add callback-scoped ordering contracts and hostile mutation coverage.

## Verification Completed

- The portable static contract passed directly and through repository-local and
  external-directory `make check` invocations.
- Python checker compilation and `git diff --check` passed.
- Ten isolated hostile mutations were rejected: either lifecycle assignment or
  the dismissal-only boundary removed; request or completion guard removed,
  inverted, or ordered after its protected operation; and stale plan status.
- Exact-base path, generated-artifact, and added-line secret-pattern scans
  passed without vendored, lockfile, project metadata, or workflow changes.
- Both Make runs reported `xcodebuild` unavailable on this Linux host, so no
  simulator, physical-device, or current-SDK behavior is claimed.
