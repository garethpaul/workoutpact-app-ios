# Changes

## 2026-06-10

- Documented and enforced the versioned legacy SDK modernization boundary for
  Swift 1-era syntax, iOS 8.3, Stripe 4.0.3, PaymentKit 1.1.1, and retired
  Fabric, DigitsKit, TwitterCore, and TwitterKit SDKs.
- Added immutable, read-only GitHub Actions verification on Python 3.10 and
  3.12 for the credential, payment, authentication, and sharing contracts.
- Added static protection for workflow permissions, action revisions, matrix
  versions, timeout, and the `make check` entry point.
- Documented that hosted Linux checks intentionally skip the legacy Xcode build.

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
