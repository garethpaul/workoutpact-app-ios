# WorkoutPact Hosted Static Verification

Status: completed

## Goal

Continuously enforce the repository's credential, payment, authentication, and
sharing safety contracts without claiming that Linux CI validates the legacy
iOS application binary.

## Changes

- Add a read-only GitHub Actions workflow on Python 3.10, 3.12, and 3.14.
- Support manual dispatch for maintenance verification.
- Pin checkout and setup-python to immutable revisions.
- Bound each matrix job with a five-minute timeout.
- Run `make check`, which executes the portable contracts and explicitly skips
  the Xcode build when the Apple toolchain is unavailable.
- Extend the static checker to prevent workflow permission and action-pin drift.

## Verification

- `python3 -m py_compile scripts/check_workoutpact_contracts.py`
- `make check`

## Follow-up Boundary

Modern Xcode validation requires a dedicated migration away from Swift 2,
retired Fabric/Digits/TwitterKit binaries, Stripe 4, and PaymentKit. The Linux
workflow intentionally verifies repository safety contracts without claiming
that the legacy application compiles or can process production payments.
