# WorkoutPact Callback Generation Guards

Status: Planned

## Problem

The Stripe and Digits callbacks reject work while their controllers are
inactive. If a controller later becomes active again, however, a completion
created before the prior disappearance can pass the restored boolean guard and
present billing UI or navigate to protected content in the wrong lifecycle.

## Requirements

1. Bind each Stripe tokenization request to the current payment-controller
   generation and invalidate that generation whenever the screen disappears.
2. Bind each Digits authentication request to the current two-factor-controller
   generation and invalidate it only when that controller is actually dismissed
   or removed, not when the Digits overlay appears.
3. Require both the retained generation and existing active-state condition on
   each main-thread completion before UI presentation or navigation.
4. Preserve input/key guards, generic errors, no-backend billing disclosure,
   Digits appearance, cancellation behavior, and storyboard identifiers.
5. Add portable ordering contracts and hostile mutations for both controllers.

## Verification

- Run focused payment and Digits generation contracts and hostile mutations.
- Run local and external-working-directory `make check` with explicit timeouts.
- Compile the Python checker and audit exact paths, artifacts, credentials,
  conflict markers, and whitespace.
- Record the unavailable Linux `xcodebuild` boundary without claiming simulator
  or physical-device validation.

## Scope Boundaries

- Do not modernize Swift, update vendored SDKs, change billing behavior, or
  alter storyboard/project metadata.
- Do not merge or close any pull request without explicit owner authorization.
