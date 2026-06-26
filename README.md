# workoutpact-app-ios

<!-- README-OVERVIEW-IMAGE -->
![Project overview](docs/readme-overview.svg)

## Overview

`garethpaul/workoutpact-app-ios` is an Apple platform application or Swift sample. Donation app if you miss a workout.

This README is based on the checked-in source, manifests, scripts, and repository metadata on the `master` branch. The project language mix found during review was: C/C++ headers (40), Swift (8).

## Project Status

This repository is an archival Swift 1-era prototype targeting iOS 8.3. It is
preserved for source review and maintenance-contract testing; it is not
production-ready and is not expected to build unchanged with a current Xcode or
iOS SDK. The app has no billing backend, creates no donation or charge, and
must not be configured with production credentials.

## Repository Contents

- `Podfile` - Apple platform dependency metadata
- `DigitsKit.framework` - source or example code
- `Fabric.framework` - source or example code
- `Podfile.lock` - Apple platform dependency metadata
- `SECURITY.md` - security reporting and disclosure guidance
- `TwitterCore.framework` - source or example code
- `TwitterKit.framework` - source or example code
- `VISION.md` - project direction and maintenance guardrails
- `workoutpact` - source or example code
- `workoutpact.xcodeproj` - Xcode project file
- `workoutpactTests` - source or example code

Additional scan context:

- Source directories: DigitsKit.framework, Fabric.framework, TwitterCore.framework, TwitterKit.framework, workoutpact, workoutpactTests
- Dependency and build manifests: Podfile, Podfile.lock
- Entry points or build surfaces: workoutpact.xcodeproj
- Test-looking files: workoutpactTests/workoutpactTests.swift

## Getting Started

### Prerequisites

- Git
- Python 3 and Ruby for the portable maintenance contracts
- A compatible legacy macOS/Xcode toolchain only if reconstructing the app
- CocoaPods capable of resolving the checked-in Stripe 4.0.3 and PaymentKit
  1.1.1 lockfile only if reconstructing the historical workspace

### Setup

```bash
git clone https://github.com/garethpaul/workoutpact-app-ios.git
cd workoutpact-app-ios
/usr/bin/make check
```

The portable verification path does not install Pods, load credentials, or
create a charge. To reconstruct the historical Xcode workspace on a compatible
machine, run `pod install`, then open `workoutpact.xcworkspace`. Do not open
`workoutpact.xcodeproj` after installing Pods; the workspace is the checked-in
container that includes both the app project and `Pods/Pods.xcodeproj`.

## Running or Using the Project

- For source and contract verification, run `/usr/bin/make check` from the
  repository root.
- For historical app exploration, open `workoutpact.xcworkspace` in a compatible
  legacy Xcode toolchain, choose the app scheme, and use a matching simulator or
  device without production credentials.

## Testing and Verification

This is an archival Swift 1-era project targeting iOS 8.3. Its lockfile retains
Stripe 4.0.3 and PaymentKit 1.1.1, and it vendors retired Fabric, DigitsKit,
TwitterCore, and TwitterKit binaries. It is not expected to build unchanged
with a current iOS SDK. Follow the staged dependency, payment, Swift, and device
verification sequence in
`docs/plans/2026-06-10-workoutpact-legacy-sdk-modernization-boundary.md`.

- `/usr/bin/make check` - runs local Python/Ruby static contracts without downloaded dependencies and attempts an Xcode build only when an explicit executable `XCODEBUILD` path and `Pods/` are available
- Public Make targets resolve the repository from the loaded Makefile and
  reject startup injection, unsafe execution modes, caller-controlled roots or
  shells, later single-colon recipe replacement, and Make expressions in
  `PYTHON` or `XCODEBUILD`. The caller-added double-colon recipes from an
  additional later `-f` file remain outside the repository Make trust boundary
  because GNU Make appends them after the checked-in target body.
- Make syntax in an explicit `-f` path is version-sensitive before the repository Makefile loads. The authority harness verifies pre-load execution on GNU Make 3.81 and 4.2.1 and non-execution on the hosted GNU Make 4.3 gate. For checkout paths containing literal `$(`, change into the checkout and invoke `/usr/bin/make` without an explicit Makefile path.
- Protected-screen contracts require any active keyboard offset to be restored
  before navigation removes keyboard observers.
- GitHub Actions runs the same portable gate on Python 3.10, 3.12, and 3.14
  on fixed Ubuntu 24.04 runners with read-only permissions, superseded-run
  cancellation, credential-free checkout, and manual dispatch; Linux runners
  intentionally skip the Xcode build pending the Swift and retired-SDK migration.
- `/usr/bin/make verify` - runs the WorkoutPact metadata, privacy, auth, payment-token,
  payment input, payment-button, payment-key, payment-error logging, stale
  payment callback, callback-generation, and no-backend billing disclosure,
  stale Twitter login callback and weak callback ownership,
  social-share result logging, motion-subtype, and overlapping shake confirmation,
  storyboard navigation, and protected-screen
  outlet and keyboard-shift static contracts
- Swift files that directly use the retained Fabric-era SDKs import their
  defining modules explicitly. The Objective-C bridging header remains limited
  to Stripe and PaymentKit declarations.
- Completed maintenance plans live under `docs/plans` and are checked by
  `make check`.
- The Make authority boundary and adversarial regression matrix are documented
  in `docs/plans/2026-06-21-workoutpact-make-authority-isolation.md`.
- Xcode's test action or `xcodebuild test` with the appropriate scheme and destination

When the required SDK or runtime is unavailable, use static checks and source review first, then verify on a machine that has the matching platform toolchain.

## Configuration and Secrets

- Detected references to Twitter. Keep API keys, OAuth credentials, tokens, and account-specific values in local configuration only.
- `workoutpact/Info.plist` contains placeholder URL scheme metadata only. Replace placeholder Twitter/Digits/Fabric values locally when running the legacy prototype, and do not commit real credentials.
- `workoutpact/Info.plist` contains an empty `StripePublishableKey` placeholder. Configure only a `pk_test_` publishable key locally; this retired prototype rejects live-mode keys and keeps billing disabled unless a backend contract and tests exist.
- Successful tokenization must disclose that no donation or charge exists and
  require explicit continuation without billing.
- Stripe tokenization requests and completions must not present billing UI
  after the payment screen has been covered.
- Stale Stripe completions must return before re-enabling the payment button or
  handling an obsolete tokenization failure.
- The shake-to-share flow should always require explicit user confirmation before opening Twitter composition.
- The shake-to-share flow should gate on the delivered motion subtype before
  presenting the confirmation prompt.
- Successful Twitter login, Digits verification, Stripe tokenization, and
  shake-to-share flows each reserve one transition so duplicate provider or UI
  callbacks cannot repeat protected navigation, billing UI, or composition.
- Logout reserves one queued login transition, rejects overlapping modal
  presentation, and releases ownership when destination lookup fails.
- Billing remains disabled; any future backend must validate
  server-authoritative integer minor units and an explicit ISO 4217 currency
  allowlist.

## Payment Token Flow

The checked-in payment screen stops at client-side Stripe tokenization:

1. PaymentKit validates the local card form before enabling submission.
2. The app requires a locally configured `pk_test_` publishable key and asks
   Stripe 4.0.3 to create a transient token.
3. The token is neither persisted nor logged and is not sent to an application
   server because this repository has no billing backend.
4. The app presents a `Billing unavailable` notice stating that no donation or
   charge was created. Only the explicit `Continue without billing` action may
   advance to the workout-sharing screen.

Real billing must remain disabled until a separate, tested backend contract
defines authenticated ownership, server-authoritative integer minor units,
allowed ISO 4217 currencies, idempotent charge creation, provider error
handling, and auditable success/failure behavior. Client-provided card data,
amounts, or success claims are not a substitute for that backend boundary.

## Security and Privacy Notes

- Review changes touching authentication or token handling; examples from the scan include DigitsKit.framework/Headers/DGTAuthenticateButton.h, DigitsKit.framework/Headers/DGTContacts.h, DigitsKit.framework/Headers/DGTOAuthSigning.h, DigitsKit.framework/Headers/DGTSession.h, and 6 more.
- Review changes touching external API calls or credential-adjacent configuration; examples from the scan include DigitsKit.framework/Headers/DGTAppearance.h, DigitsKit.framework/Headers/DGTAuthenticateButton.h, DigitsKit.framework/Headers/DGTContactAccessAuthorizationStatus.h, DigitsKit.framework/Headers/DGTContacts.h, and 6 more.
- Review changes touching network requests, sockets, or service endpoints; examples from the scan include TwitterCore.framework/Headers/TWTRAPIErrorCode.h, TwitterCore.framework/Headers/TWTRAuthConfig.h, TwitterCore.framework/Headers/TWTRCoreOAuthSigning.h, TwitterKit.framework/Headers/TWTRAPIClient.h, and 3 more.
- Review changes touching mobile permissions or privacy-sensitive device data; examples from the scan include DigitsKit.framework/Headers/DGTContactAccessAuthorizationStatus.h, DigitsKit.framework/Headers/DGTContacts.h, DigitsKit.framework/Headers/DGTContactsUploadResult.h, DigitsKit.framework/Headers/DGTErrors.h, and 1 more.
- Review changes touching file, media, JSON, XML, CSV, OCR, or data parsing; examples from the scan include DigitsKit.framework/Headers/DGTContacts.h, DigitsKit.framework/Headers/DGTContactsUploadResult.h, TwitterCore.framework/Headers/TWTRConstants.h, TwitterCore.framework/Headers/TWTRCoreOAuthSigning.h, and 6 more.
- Review changes touching database, model, or persistence code; examples from the scan include TwitterKit.framework/Headers/TWTRTweetTableViewCell.h, TwitterKit.framework/Headers/TWTRTweetViewDelegate.h.

## Maintenance Notes

- This looks like an Apple platform project or sample. Xcode, Swift, CocoaPods, and deployment target versions may need to match the original project era.
- See `SECURITY.md` for vulnerability reporting and safe research guidance.
- See `VISION.md` for project direction and contribution guardrails.
- See `docs/plans/2026-06-08-workoutpact-build-privacy-contracts.md` and
  `docs/plans/2026-06-08-workoutpact-auth-payment-sharing-guards.md` for the
  current build, privacy, auth, payment, and sharing baselines.
- See `docs/plans/2026-06-08-workoutpact-logout-navigation-guard.md` for the
  logout navigation guard contract.
- See `docs/plans/2026-06-08-workoutpact-payment-button-guard.md` for guarded
  payment submit-button state updates.
- See `docs/plans/2026-06-09-workoutpact-payment-input-guard.md` for guarded
  PaymentKit input access before tokenization.
- See `docs/plans/2026-06-09-workoutpact-storyboard-cast-guards.md` for guarded
  storyboard controller casts in login and logout navigation.
- See `docs/plans/2026-06-09-workoutpact-payment-error-log.md` for
  non-sensitive Stripe tokenization failure logging.
- See `docs/plans/2026-06-09-workoutpact-payment-key-guard.md` for stopping
  tokenization when no local Stripe publishable key is configured.
- See `docs/plans/2026-06-09-workoutpact-textfield-outlet-guard.md` for the
  protected screen text-field outlet guard.
- See `docs/plans/2026-06-09-workoutpact-keyboard-shift-guard.md` for the
  protected screen keyboard animation state guard.
- See `docs/plans/2026-06-09-workoutpact-share-result-log.md` for keeping
  Twitter composer outcomes out of console logs.
- See `docs/plans/2026-06-09-workoutpact-shake-motion-subtype-guard.md` for
  using the delivered motion subtype before prompting to share.
- See `docs/plans/2026-06-10-workoutpact-hosted-static-verification.md` for
  the pinned, least-privilege hosted contract baseline.
- See `docs/plans/2026-06-10-workoutpact-no-backend-billing-notice.md` for the
  explicit no-charge disclosure and root-independent verification contract.
- See `docs/plans/2026-06-10-workoutpact-keyboard-lifecycle-reset.md` for
  protected-screen keyboard restoration during navigation.
- See `docs/plans/2026-06-13-workoutpact-stale-payment-callback.md` for rejecting
  tokenization work after the payment screen is covered.
- See `docs/plans/2026-06-13-workoutpact-callback-generation-guards.md` for
  rejecting pre-dismissal Stripe and Digits callbacks after reappearance.
- See `docs/plans/2026-06-14-workoutpact-stale-payment-ui-state.md` for rejecting
  stale Stripe completions before any completion-side UI or error handling.
- See `docs/plans/2026-06-15-workoutpact-stale-twitter-login-callback.md` for
  rejecting Twitter success callbacks after the login controller leaves its
  navigation lifecycle.
- See `docs/plans/2026-06-16-workoutpact-weak-twitter-login-callback.md` for the
  ownership boundary where the Twitter login button stays cycle-free.
  Queued presentation callbacks capture the controller weakly.
- See `docs/plans/2026-06-19-workoutpact-async-flow-safety-review.md` for the
  exactly-once payment, Digits, Twitter, and sharing callback boundaries.
- See `docs/plans/2026-06-25-workoutpact-digits-import.md` for the protected
  logout controller's explicit DigitsKit module boundary.
- Keep the single Twitter login transition guard consumed across resumed
  appearances so duplicate success cannot present another verification screen.

## Contributing

Keep changes small and tied to the project that is already present in this repository. For code changes, document the toolchain used, avoid committing generated dependency directories or local configuration, and update this README when setup or verification steps change.
