---
title: WorkoutPact Build And Privacy Contract Hardening
status: completed
date: 2026-06-08
origin: user-requested continuous engineering quality loop
execution: code
---

# WorkoutPact Build And Privacy Contract Hardening

## Problem Frame

The Xcode project references `workoutpact/Info.plist`, but the file is missing from the repository. It also configures the Swift bridging header with an absolute path from the original author's machine. Those two issues make the project non-portable and leave authentication/payment/privacy metadata without a tracked contract.

This pass keeps the legacy Swift 1-era prototype intact and adds only enough build metadata and static verification to make future maintenance safer.

## Scope Boundaries

- Preserve the existing Fabric, Digits, TwitterKit, Stripe, and PaymentKit prototype flow.
- Do not modernize Swift syntax or replace legacy SDKs in this pass.
- Do not add real payment credentials, Twitter credentials, Fabric credentials, or backend billing behavior.
- Do not attempt a full simulator build unless the local Xcode/CocoaPods toolchain is present.

## Requirements Traceability

- Improve engineering quality by adding repeatable checks and documentation.
- Fix a concrete portability issue in the checked-in build configuration.
- Make payment, social auth, and contact/privacy boundaries explicit without adding secrets.
- Commit and push the completed work to the default branch.

## Implementation Units

### U1: Restore App Metadata

Files:

- Modify `workoutpact/Info.plist`
- Modify `workoutpact.xcodeproj/project.pbxproj`

Approach:

- Add minimal tracked app and test `Info.plist` files with bundle metadata, storyboard references, iOS deployment compatibility, URL type placeholders for Twitter/Digits, a local-only Stripe publishable key placeholder, and contact/privacy usage copy tied to Digits contact flows.
- Replace the absolute `SWIFT_OBJC_BRIDGING_HEADER[arch=*]` value with the repo-relative `workoutpact/BridgeHeader.h`.

Test scenarios:

- Static check fails if `workoutpact/Info.plist` is missing.
- Static check fails if the project references an absolute bridging header path.
- Static check confirms privacy metadata exists for contact access when Digits contact APIs are bundled.

### U2: Add Verification Harness

Files:

- Create `scripts/check_workoutpact_contracts.py`
- Create `Makefile`

Approach:

- Implement dependency-free static checks using Python's plist parser and straightforward source inspection.
- Add `make lint`, `make test`, `make build`, `make verify`, and `make check` targets. Build should use `xcodebuild` only when available and otherwise emit a clear skip.

Test scenarios:

- `make verify` runs the static contract script.
- `make check` runs lint, tests, build, and verification without requiring a local iOS simulator.
- The verification script catches missing payment/social/privacy metadata before runtime.

### U3: Update Maintenance Documentation

Files:

- Modify `README.md`
- Create `CHANGES.md`
- Modify this plan status to `completed` when implementation and verification are done.

Approach:

- Document the new make targets, the local-only Stripe publishable key placeholder, and the fact that no real credentials should be committed.
- Capture this pass in a short changelog entry.

Test scenarios:

- README names `make check` as the local static verification path.
- CHANGES records the app metadata and contract harness additions.

## Verification

- `make lint`
- `make test`
- `make build`
- `make verify`
- `make check`
- `git diff --check`
