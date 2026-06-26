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
- Root and external clean-copy `make check` passed the Make authority harness,
  static contracts, two checker tests, 15 login lifecycle mutations, five
  ownership mutations, five shake mutations, and 18 async-flow mutations.
- Pull request #23 implementation head
  `ae6795b4a47059a4cca4bc63aba04ce4d4fa607a` passed both hosted Python
  3.10/3.12/3.14 matrices, CodeQL actions and Python analyses, and the aggregate
  gate.
- Required Codex review was attempted against `origin/master`; the helper
  stopped before analysis because OpenAI WebSocket and HTTPS transports both
  returned HTTP 401. Local, remote, and pull-request heads were identical, and
  an immutable manual fallback review found no actionable defects.
- Legacy `xcodebuild` remained unavailable and was skipped truthfully.
