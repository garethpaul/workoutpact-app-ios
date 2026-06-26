# WorkoutPact Legacy Setup And Status

Status: Completed

## Problem

The README described the project as archival only inside the verification
section. Its setup path also ran `pod install` but later told readers to open the
standalone Xcode project, even though the checked-in CocoaPods workspace is the
container that includes both the app and Pods projects. The payment boundary was
spread across configuration bullets rather than tracing where tokenization
stops without a backend.

## Requirements

- Put the archival, non-production status before setup instructions.
- Keep current source verification independent of CocoaPods and credentials.
- Direct historical reconstruction through `workoutpact.xcworkspace` after
  installing Pods, not through the standalone project.
- Document the client tokenization flow and the explicit no-charge boundary.
- State the minimum backend contract required before real billing can exist.
- Preserve the Swift 1, iOS 8.3, Stripe 4.0.3, PaymentKit 1.1.1, Fabric,
  DigitsKit, TwitterCore, and TwitterKit compatibility boundary.

## Verification

- RED: the static contract failed because the README lacked a project-status
  section, a production-readiness warning, the CocoaPods workspace path, and the
  standalone-project warning.
- Python 3.14.6 / Ruby 3.1.2 container `make check` passed Make authority,
  Python compilation, the full static contract, checker tests, and every
  lifecycle/async mutation suite; the legacy Xcode build skipped as expected.
- `git diff --check` verifies patch formatting.
