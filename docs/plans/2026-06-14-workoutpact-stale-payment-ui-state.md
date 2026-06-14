# WorkoutPact Stale Payment UI State

Status: Completed

## Problem

The Stripe completion re-enables the payment button and handles tokenization
errors before checking the retained payment generation and screen visibility.
A callback from a dismissed or prior appearance can therefore mutate current
UI state and process an obsolete failure even though `handleToken` is guarded.

## Requirements

1. Make the generation and visibility check the first main-thread completion
   action after Stripe tokenization returns.
2. Re-enable the guarded payment button only for the current visible payment
   request.
3. Preserve current-request error handling, token handling, publishable-key and
   card guards, and the explicit no-billing continuation.
4. Add mutation-sensitive portable ordering contracts and completed plan
   evidence.

## Verification Plan

- Run the focused payment completion contract and hostile mutations.
- Run bounded local, external-directory, and hostile-root `make check` gates.
- Compile the checker and audit the exact diff, structured project files,
  generated artifacts, whitespace, and changed lines for credential material.
- Record that Xcode, simulator, device, Stripe SDK, and PaymentKit execution are
  unavailable on this Linux host.

## Scope Boundaries

- Do not modernize Swift, update vendored SDKs, change billing behavior, or
  alter storyboard/project metadata.
- Do not merge or close stacked pull requests without explicit authorization.

## Work Completed

- Moved the retained payment generation and visibility check to the start of
  the main-thread Stripe completion.
- Kept payment-button restoration, current-request error handling, and token
  handling behind that lifecycle guard.
- Added portable ordering, documentation, and completed-plan contracts.

## Verification Results

- The focused completion-order contract passed before enabling completed-plan
  verification.
- Six isolated hostile mutations were rejected: button restoration or error
  handling before the lifecycle guard, either missing comparison, token handling
  before the guard, and incomplete plan evidence.
- Local `make lint`, `make test`, `make build`, and `make check` passed the
  portable contracts.
- External-directory and hostile-root `make check` passed with paths anchored
  to the protected Makefile root.
- Every full gate truthfully skipped `xcodebuild` because it is unavailable on
  this Linux host; no simulator, device, Stripe, or PaymentKit execution is
  claimed.
