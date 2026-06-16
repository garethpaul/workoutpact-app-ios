# Changes

## 2026-06-16

- Added a single Twitter login transition guard so duplicate successful
  callbacks cannot present multiple two-factor screens from one appearance.
- Broke the Twitter login button retain cycle with weak provider and queued
  main-thread callback captures while preserving stale-lifecycle rejection.

## 2026-06-15

- Rejected successful Twitter login callbacks after the login controller is
  dismissed or removed, before storyboard lookup or phone-verification UI.
- Added lifecycle and ordering contracts for stale Twitter login completions.

## 2026-06-14

- Moved the Stripe generation and visibility guard ahead of payment-button and
  tokenization-error handling so stale completions cannot mutate current UI.
- Added mutation-sensitive ordering coverage for the complete payment callback.

## 2026-06-13

- Bound Stripe and Digits requests to controller lifecycle generations so
  pre-dismissal callbacks remain invalid after a later appearance.
- Rejected Stripe tokenization requests and asynchronous completions after the
  payment screen is covered, before billing UI can be presented.
- Added portable lifecycle ordering contracts for both payment visibility
  guards.

## 2026-06-10

- Restored any active protected-screen keyboard offset before navigation
  removes observers, clearing stale visibility and height state for the next
  appearance.
- Documented and enforced the versioned legacy SDK modernization boundary for
  Swift 1-era syntax, iOS 8.3, Stripe 4.0.3, PaymentKit 1.1.1, and retired
  Fabric, DigitsKit, TwitterCore, and TwitterKit SDKs.
- Added immutable, read-only GitHub Actions verification on Python 3.10, 3.12,
  and 3.14 for the credential, payment, authentication, and sharing contracts,
  with manual dispatch for maintenance runs.
- Added static protection for workflow permissions, action revisions, matrix
  versions, timeout, and the `make check` entry point.
- Documented that hosted Linux checks intentionally skip the legacy Xcode build.
- Added an explicit post-tokenization notice that no donation or charge was
  created and requires `Continue without billing` before sharing.
- Pinned hosted verification to Ubuntu 24.04 with superseded-run cancellation
  and made static and optional workspace checks root-independent.

## 2026-06-09

- Gated the shake-to-share prompt on the delivered motion subtype instead of
  reading the event subtype.
- Added static checker coverage for the shake motion-subtype guard.
- Guarded protected-screen keyboard movement so duplicate show/hide
  notifications cannot repeatedly offset the view.
- Added static checker coverage for keyboard-shift state.
- Guarded the protected screen text-field outlet before assigning its delegate.
- Added static checker coverage for the text-field outlet guard.
- Removed Twitter composer result logging from the shake-to-share flow.
- Added static checker coverage for social-share result logging.
- Replaced raw Stripe tokenization error interpolation with a non-sensitive log
  message.
- Added static checker coverage for payment failure logging.
- Stopped payment tokenization when no local Stripe publishable key is
  configured.
- Added static checker coverage for the payment publishable-key guard.
- Replaced forced storyboard controller casts in login and logout navigation
  with guarded casts.
- Added static checker coverage for storyboard cast guards.
- Guarded PaymentKit input access throughout token creation instead of
  force-unwrapping `paymentView`.
- Added static checker coverage for the payment input guard.

## 2026-06-08

- Guarded payment submit-button state updates instead of force-unwrapping the
  optional `payButton`.
- Guarded logout navigation before presenting the login controller.
- Added docs-plan coverage for the WorkoutPact build/privacy and auth/payment
  baselines to the static contract checker.
- Restored the tracked app and test `Info.plist` files referenced by the Xcode project.
- Replaced machine-local Xcode paths with repo-relative build settings.
- Added static contracts for app metadata, privacy copy, social auth callbacks, and Stripe tokenization boundaries.
- Added `make check` as the local verification entry point for this legacy iOS project.
- Moved Stripe publishable key configuration to an empty plist placeholder, added callback guards for Twitter, Digits, and Stripe flows, disabled payment submission until card validation succeeds, and required explicit confirmation before opening Twitter sharing.
