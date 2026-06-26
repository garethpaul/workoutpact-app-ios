# Payment Submit Configuration

Status: Completed

## Problem

The controller rejected tokenization when `StripePublishableKey` was missing,
but PaymentKit validity alone still enabled Submit. The action then appeared
available even though every tap could only log that tokenization was disabled.

## Decision

Centralize Submit availability in `paymentSubmissionEnabled()`. Require valid
card input, no active tokenization flow, and the same configured Stripe test-key
boundary used by application launch and `createToken()`.

## Verification

- The focused contract failed first on the missing configuration-aware state.
- Validation, re-entry, failure, defensive token, and cancellation paths all use
  the shared availability decision.
- Hostile mutations remove the configured-key condition and replace callback
  restoration with unconditional enablement.
- Full portable `make check`, hosted, and exact-head review evidence is recorded
  before merge.
