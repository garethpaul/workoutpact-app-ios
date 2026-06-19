# WorkoutPact legacy SDK modernization boundary

status: completed

## Current boundary

The prototype uses Swift 1-era syntax, an iOS 8.3 deployment target, Stripe
4.0.3, PaymentKit 1.1.1, and vendored Fabric, DigitsKit, TwitterCore, and
TwitterKit binaries. These versions are retained only to preserve the archival
snapshot and are not supported by a current iOS SDK toolchain.

## Modernization sequence

1. Preserve `make check` coverage for credential, payment, navigation, motion, and sharing boundaries.
2. Replace Fabric, DigitsKit, TwitterCore, and TwitterKit authentication and sharing flows.
3. Redesign payment tokenization around a supported Stripe SDK and backend contract before enabling charges.
4. Replace PaymentKit and migrate Swift/UIKit syntax in focused stages.
5. Raise the deployment target only after login, verification, payment, keyboard, motion, and sharing flows pass current XCTest and device verification.

Until that work is scheduled, do not use real identity or payment data and do
not describe the static Linux gate as a current-SDK build.

## Verification

- `python3 -m py_compile scripts/check_workoutpact_contracts.py` passed.
- `make check` passed the portable contracts and explicitly reported that
  `xcodebuild` was unavailable on this Linux host.
- Hostile Stripe-version, deployment-target, and documentation-baseline
  mutations were rejected by the contract checker.
- `git diff --check` passed.
