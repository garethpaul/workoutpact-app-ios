# WorkoutPact Payment Input Guard

## Status: Completed

## Context

The payment button state and token callback paths were guarded, but
`createToken()` still checked `paymentView` for nil and then force-unwrapped the
same optional to read its card. Payment tokenization should keep the PaymentKit
input guarded throughout the flow.

## Objectives

- Preserve the existing prototype tokenization flow.
- Avoid force-unwrapping `paymentView`.
- Reject missing PaymentKit input before tokenization.
- Reject missing card input before tokenization.
- Keep submit-button disabling and token callback behavior intact.
- Extend static checks for the guarded payment input contract.

## Work Completed

- Wrapped PaymentKit input access in `if let paymentInput = paymentView`.
- Checked `paymentInput.card` before building the Stripe card.
- Read card details from the guarded `paymentInput` value.
- Updated `scripts/check_workoutpact_contracts.py` to reject `paymentView!`.
- Updated README, VISION, and CHANGES.

## Verification

- `python3 scripts/check_workoutpact_contracts.py`
- `make check`
- `make verify`
- `git diff --check`

## Follow-Up Candidates

- Guard storyboard controller casts in auth/logout navigation.
- Replace raw Stripe error interpolation with a non-sensitive failure message.
