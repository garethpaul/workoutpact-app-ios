# WorkoutPact Async Flow Safety Review

Status: Completed

## Scope

Review the open PR #2 through #11 stack and the diverged PR #1 delivery branch,
following payment, Digits, Twitter, and shake callbacks through their UIKit side
effects. Preserve the legacy Swift/iOS boundary rather than claiming a
current-toolchain migration.

## Findings

- PaymentKit card validation could re-enable Submit while Stripe tokenization
  was active, allowing more than one token request and result alert in the same
  controller generation.
- Repeated Digits activation or provider completion could start or consume more
  than one protected-navigation transition.
- The Twitter transition reservation reset on every resumed appearance, so a
  delayed duplicate success callback could become valid after the two-factor
  controller was dismissed.
- Shake confirmation guarded only the currently presented controller. It did
  not reserve ownership across alert dismissal and Twitter composer startup.
- Stripe configuration accepted any non-empty `pk_` prefix and did not state
  the server-side amount/currency validation required before billing.

## Changes

- Added one in-flight reservation per payment, Digits, and share flow.
- Claimed reservations before provider calls or presentation construction,
  rejected duplicate completions on the main queue, and released reservations
  only on explicit failure, cancellation, or provider completion.
- Weakly captured controllers in Stripe, Digits, payment-alert, shake-alert,
  and Twitter composer callbacks.
- Kept successful Twitter transition ownership consumed across resumed
  appearances and moved the claim after destination validation.
- Restricted local Stripe configuration to test-mode `pk_test_` values without
  embedded whitespace and rejected live-mode keys in the retired prototype.
- Documented that any future charge backend must use server-authoritative
  integer minor units and an explicit ISO 4217 currency allowlist.

## Provenance

The duplicate-flow seams were carried forward from the original 2015 provider
callbacks. PRs #3 through #11 added lifecycle and presentation guards, but the
stack still lacked per-request consumption across provider duplicate delivery
and modal resume boundaries. PR #2 already delivers PR #1's actual
modernization-boundary patch onto current `master`; PR #1's side-base artwork,
agent instructions, and device preview are not part of PR #1's diff.

## Evidence

- The new async-flow contract failed against the untouched PR #11 head on all
  payment, Digits, Twitter, shake, publishable-key, and billing-boundary checks.
- The updated contract passes and rejects ten targeted mutations.
- Existing login lifecycle, callback ownership, shake presentation, and full
  repository contracts remain part of `make check`.
- `make check` passed on local Python 3.11, 3.12, 3.13, and 3.14, from the
  repository root, from `/tmp`, and with a hostile command-line `ROOT` value.
- A direct Xcode 26 probe reached project evaluation but failed because the
  historical Pods xcconfig is absent, iOS 8.3 is below the supported deployment
  range, and the unset Swift language version is no longer supported.
- Native execution still requires a historical compatible Xcode/CocoaPods
  environment and live provider credentials; static success is not a release
  claim.
