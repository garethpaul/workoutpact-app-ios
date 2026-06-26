# WorkoutPact Payment Validity State

Status: Completed

## Priority

P2 payment-input correctness. A Stripe failure callback can re-enable Submit
after the user has edited the card into an invalid state during tokenization.

## Problem

`PaymentViewController` receives current card validity through the existing
`PTKViewDelegate` callback, but does not retain it. The async failure path and
view re-entry therefore restore the button independently of the latest input
state. `createToken()` also relies on button state and card presence rather than
requiring the last validated input state directly.

## Decision

- Persist the latest PaymentKit validity in `paymentInputValid`.
- Require a visible, idle, valid input before tokenization.
- Restore Submit from `paymentInputValid` after current-request failures,
  cancellation, and view re-entry.
- Preserve generation, visibility, weak-capture, key, and card-presence guards.

## Implementation Plan

1. Add mutation-sensitive contracts for stored validity, entry guarding, and
   callback/button restoration.
2. Observe the focused async-flow test fail against the current controller.
3. Implement the smallest controller state changes.
4. Update README, security, vision, changelog, and canonical-plan registration.
5. Run focused mutations, repository and external-directory `make check`, and
   hosted static verification before merge.

## Verification Evidence

- RED: the focused async-flow contract reported missing stored validity,
  delegate ownership, invalid-input entry rejection, and callback restoration.
- GREEN: the controller stores `paymentInputValid`, guards tokenization with it,
  and restores Submit from the current value after failure, cancellation, and
  view re-entry.
- The first hostile callback-enable mutation exposed a decoy weakness because a
  later valid restoration masked the regression; the contract was narrowed to
  the Stripe completion block.
- The focused async-flow suite passes with 17 hostile mutations rejected.
- Python 3.10.20, 3.12.13, and 3.14.6 with Ruby 3.1.2 passed full `make check`,
  including the Make authority harness, static checker, fixture tests, and all
  lifecycle, ownership, presentation, and async-flow mutation suites.
- Compatible legacy `xcodebuild` and Pods remain unavailable in the portable
  containers and skipped truthfully.
- Hosted checks and exact-head review remain the publication gate.
