# WorkoutPact Payment Key Guard

## Status: Completed

## Context

The app delegate reads the Stripe publishable key from `Info.plist` and leaves
payment tokenization disabled when no local `pk_` key is configured. The payment
screen still attempted token creation after valid card input, which could call
Stripe with missing configuration.

## Objectives

- Preserve the prototype PaymentKit and Stripe tokenization flow.
- Stop before tokenization when no local Stripe publishable key is configured.
- Keep missing-key logs non-sensitive.
- Keep real publishable keys out of source control.
- Extend static checker coverage for the payment key boundary.

## Work Completed

- Added a `configuredStripePublishableKey()` guard inside `createToken()`.
- Returned before disabling the submit button or calling Stripe when no key is
  configured.
- Reused the existing non-sensitive missing-key log message.
- Extended `scripts/check_workoutpact_contracts.py`.
- Updated README, VISION, and CHANGES.

## Verification

- Negative check: `python3 scripts/check_workoutpact_contracts.py` failed
  before the payment publishable-key guard was added.
- `python3 scripts/check_workoutpact_contracts.py`
- `make check`
- `make verify`
- `git diff --check`

## Follow-Up Candidates

- Add user-visible payment-token failure guidance.
- Add simulator verification notes for payment setup and retry paths.
