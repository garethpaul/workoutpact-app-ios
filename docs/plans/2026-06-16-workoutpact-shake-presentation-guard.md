# Guard Shake Confirmation Presentation Ownership

Status: Completed

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

1. Return from `motionEnded` when a share flow is already reserved or
   `presentedViewController` is non-nil.
2. Reserve the share flow after motion validation and before alert construction.
3. Release the reservation only on explicit cancellation or Twitter composer
   completion.
4. Add focused mutations for a missing, inverted, late, or unclaimed guard.
5. Synchronize repository guidance and completed verification evidence.

## Verification

- The pre-change shake handler failed the new focused contract.
- All five shake-presentation mutations were rejected.
- Repository and external-directory `make check` passed; Linux reported
  `xcodebuild unavailable` and truthfully skipped the legacy native build.
- Exact-path diff, generated-artifact and credential-pattern audits passed,
  together with conflict-marker, binary, mode, and large-file checks.
