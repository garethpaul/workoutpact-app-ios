# WorkoutPact Stale Payment UI State

Status: Planned

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
