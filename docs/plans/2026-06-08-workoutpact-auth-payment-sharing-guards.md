---
title: WorkoutPact Auth Payment And Sharing Guards
status: completed
date: 2026-06-08
origin: user-requested continuous engineering quality loop
execution: code
---

# WorkoutPact Auth Payment And Sharing Guards

## Problem Frame

The legacy prototype advanced after Twitter login, Digits verification, and Stripe token creation without checking callback errors. It also enabled the payment submit button before card validation and opened the Twitter composer directly on shake. Those behaviors are risky for a prototype that touches identity, cards, and social posting.

## Scope Boundaries

- Keep the existing UIKit, Fabric, Digits, TwitterKit, PaymentKit, and Stripe APIs.
- Do not add backend billing, real credentials, or real charge behavior.
- Do not modernize Swift syntax beyond the minimal guards needed for the existing project era.

## Requirements Traceability

- Improve engineering quality with focused behavior guardrails.
- Keep payment, authentication, and social sharing boundaries explicit.
- Add tests/static contracts that catch regressions without requiring a local simulator.

## Implementation Units

### U1: Callback Guards

Files:

- Modify `workoutpact/LoginViewController.swift`
- Modify `workoutpact/TwoFactorViewController.swift`
- Modify `workoutpact/PaymentViewController.swift`

Approach:

- Return early when Twitter, Digits, or Stripe callbacks include an error or nil session/token.
- Keep the payment submit button disabled until PaymentKit reports a valid card.

Test scenarios:

- Static check fails when login or Digits callbacks can advance on errors.
- Static check fails when Stripe tokenization can advance on errors or nil tokens.
- Static check fails when the submit button starts enabled before validation.

### U2: Explicit Sharing And Local Payment Configuration

Files:

- Modify `workoutpact/ShakeViewContorller.swift`
- Modify `workoutpact/AppDelegate.swift`
- Modify `workoutpact/Info.plist`
- Create `workoutpactTests/Info.plist`
- Modify `scripts/check_workoutpact_contracts.py`

Approach:

- Add a confirmation alert before opening the Twitter composer from a shake gesture.
- Read the Stripe publishable key from `Info.plist` local configuration while keeping the source value empty.
- Track the test bundle plist referenced by the Xcode project.
- Extend static contracts for the new auth, payment, sharing, and plist boundaries.

Test scenarios:

- Static check fails if shake-to-share opens the composer without a confirmation alert.
- Static check fails if the source or app plist contains a non-empty Stripe publishable key.
- Static check fails when the referenced test bundle plist is missing.

## Verification

- `make check`
- `git diff --check`
