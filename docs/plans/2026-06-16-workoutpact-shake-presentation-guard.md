# Guard Shake Confirmation Presentation Ownership

Status: Planned

## Context

`ShakeViewController.motionEnded` validates the delivered shake subtype but
always constructs and presents a new confirmation alert. Repeated shake
callbacks while an alert or tweet composer is already presented can therefore
attempt overlapping modal presentation.

## Objectives

- Preserve the delivered motion-subtype guard as the first decision.
- Reject shake confirmation while the controller already presents another
  view controller.
- Perform the ownership check before alert construction and presentation.
- Add mutation-sensitive static coverage for presence, polarity, and ordering.

## Scope Boundaries

- Do not change confirmation copy, tweet text, image, composer behavior,
  navigation, authentication, payment, or dependencies.
- Do not add throttling timers or a second presentation-state variable.
- Native Xcode and simulator validation remain unavailable on this Linux host
  and must be reported truthfully.
- The successor PR will be stacked on open PR #10; neither pull request may be
  merged or closed without explicit authorization.

## Implementation

1. Return from `motionEnded` when `presentedViewController` is non-nil.
2. Require the ownership guard after motion validation and before alert
   construction.
3. Add focused mutations for a missing, inverted, or late ownership guard.
4. Synchronize repository guidance and completed verification evidence.

## Verification

- Prove the pre-change shake handler fails the new focused contract.
- Run focused mutations and repository/external-directory `make check`.
- Record the Linux `xcodebuild` limitation without weakening portable checks.
- Audit exact paths, generated artifacts, credentials, conflict markers,
  binaries, modes, and large files before shipping.
