# WorkoutPact Stale Payment Callback Guard

Status: Completed

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

- The portable stale-payment lifecycle contract passed.
- Local and external-directory `make check` passed.
- Eight hostile mutations were rejected: either visibility assignment removed,
  the request guard inverted, either guard removed, either guard ordered after
  its protected operation, and stale plan status.
- Python compilation and `git diff --check` passed.
- `xcodebuild` is unavailable on this Linux host, so no simulator or physical
  device behavior is claimed.
