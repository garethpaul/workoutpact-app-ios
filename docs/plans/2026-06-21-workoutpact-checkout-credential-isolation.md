# WorkoutPact Checkout Credential Isolation

Status: Completed

## Problem

Hosted verification used read-only repository permissions but allowed
`actions/checkout` to retain the GitHub token in local Git configuration.
Later static-contract steps do not need repository authentication.

## Change

- Set `persist-credentials: false` on the immutable checkout step.
- Bind credential isolation to that exact checkout block.
- Reject missing, writable, decoy-only, duplicate, and additional-checkout
  configurations in the portable contract.

## Verification Results

- Repository and external-directory `make check` passed.
- Five hostile checkout-credential mutations were rejected.
- The Linux build gate continued to report the unavailable Xcode boundary
  truthfully without loading provider credentials.
