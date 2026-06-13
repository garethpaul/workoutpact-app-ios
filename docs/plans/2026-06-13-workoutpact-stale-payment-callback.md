# WorkoutPact Stale Payment Callback Guard

Status: In Progress

## Goal

Prevent an asynchronous Stripe tokenization completion from presenting billing
UI after the payment screen has been covered or dismissed.

## Scope

- Track whether the payment screen is currently visible.
- Reject tokenization before the Stripe request when the screen is inactive.
- Recheck visibility on the main-thread completion before calling
  `handleToken`.
- Preserve guarded PaymentKit input, publishable-key validation, button state,
  generic error logging, and the no-backend billing notice.
- Add portable ordering contracts and hostile mutation coverage.

## Verification

- Run the focused stale-payment callback contract.
- Run `make check` locally and from an external working directory.
- Reject mutations that remove or invert lifecycle state and move either guard
  after its protected operation.
- Run Python compilation and `git diff --check`.
- Record the unavailable Xcode/device boundary without claiming runtime proof.
