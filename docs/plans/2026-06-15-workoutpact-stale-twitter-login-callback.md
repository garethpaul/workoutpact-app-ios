# WorkoutPact Stale Twitter Login Callback

Status: Planned

## Problem

`LoginViewController` checks TwitterKit errors before advancing, but its
asynchronous success callback can still present `TwoFactorViewController`
after the login screen has been dismissed or removed. A late success can
therefore reveal authentication UI from a stale controller lifecycle.

## Requirements

1. Track whether the login controller remains an active navigation context.
2. Activate that context on appearance and invalidate it only when the
   controller is dismissed or removed, not while TwitterKit temporarily covers
   the screen for authentication.
3. Recheck the lifecycle on the main queue after TwitterKit succeeds and
   before storyboard lookup or presentation.
4. Preserve cancellation/error behavior, the guarded storyboard cast, the
   existing controller identifier, and the legacy TwitterKit API boundary.
5. Add mutation-sensitive static coverage for missing state, invalidation,
   queue ordering, and presentation before the lifecycle guard.
6. Synchronize the changelog and README maintenance evidence.

## Verification

- Run focused checker mutations for the login lifecycle and ordering contract.
- Run repository-root and external-directory `make check` with explicit
  timeouts.
- Audit the exact diff, generated artifacts, conflict markers, file modes,
  whitespace, and added credential-like values.
- Record Linux's unavailable Xcode/simulator boundary without weakening the
  portable gate.
- Require the stacked pull request's exact-head push and pull-request matrices
  to complete successfully before recording terminal evidence.

## Scope Boundaries

- Do not modernize Swift, update vendored SDKs, change authentication UX, or
  alter storyboard/project metadata.
- Do not merge or close the existing pull-request stack without explicit owner
  authorization.
