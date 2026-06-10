# WorkoutPact No-Backend Billing Notice

Status: Completed

## Context

The prototype advanced to the workout-sharing screen immediately after Stripe
tokenization, even though it has no application backend and creates no donation
or charge. That transition could imply a billing pact existed when only a
transient Stripe token had been created.

## Changes

- Show a clear notice after tokenization that no donation or charge was created.
- Require an explicit `Continue without billing` action before advancing.
- Keep the token transient and out of application persistence and logging.
- Pin hosted verification to Ubuntu 24.04 with superseded-run cancellation.
- Make static checks and the optional Xcode workspace build root-independent.

## Verification

- `make check`
- Root-independent `make test`
- Mutation checks for billing disclosure, continuation, CI, and Make paths
- `git diff --check`
