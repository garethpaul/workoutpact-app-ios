---
title: WorkoutPact Payment Button Guard
status: completed
date: 2026-06-08
origin: user-requested continuous engineering quality loop
execution: code
---

# WorkoutPact Payment Button Guard

Status: Completed

## Problem Frame

`PaymentViewController` stored the submit button as an optional `UIBarButtonItem`
but force-unwrapped it while initializing, validating card input, disabling
submission during tokenization, and re-enabling after the Stripe callback. The
button is normally created in `viewDidLoad`, but guarded access better matches
the optional property and avoids avoidable crashes in tests or future reuse.

## Scope Boundaries

- Preserve the existing PaymentKit validation and Stripe tokenization flow.
- Do not add backend billing, charges, or real payment credentials.
- Do not modernize unrelated Swift syntax.

## Implementation

- Guard `payButton` before enabling or disabling it.
- Keep the button disabled until PaymentKit reports a valid card.
- Keep the button disabled during token creation and re-enable it on callback.
- Extend `scripts/check_workoutpact_contracts.py` to reject `payButton!`
  state updates.

## Verification

- `python3 scripts/check_workoutpact_contracts.py`
- `make check`
- `make verify`
- `git diff --check`
