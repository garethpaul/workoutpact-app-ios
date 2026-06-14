# WorkoutPact Make Root Override Protection

Status: Planned

## Problem

The Makefile derives an absolute repository root for the portable checker and
legacy Xcode workspace, but an ordinary assignment can be replaced by a
command-line `ROOT` value. Verification can therefore be redirected away from
the checked-out project.

## Requirements

1. Protect the Makefile-derived repository root with GNU Make's `override`
   directive.
2. Preserve the configurable Python command and every existing verification
   target.
3. Require exact protected-root, Python-override, checker, workspace, and Xcode
   path contracts in the portable checker.
4. Pass local, external-working-directory, and hostile-root full gates.
5. Reject focused mutations covering root derivation, tool override semantics,
   rooted paths, and completed-plan status.

## Verification

- Compile and run the portable checker first.
- Run bounded local, external-working-directory, and hostile `ROOT` full
  `make check` gates.
- Run focused static mutations and structured plist/XML/workflow checks.
- Inspect the exact diff and scan changed lines for credentials and generated
  artifacts before committing only intended paths.
- Record the unavailable Linux `xcodebuild` boundary without claiming native
  simulator or device validation.

## Scope Boundaries

- Do not change Swift behavior, dependencies, workflows, project/storyboard
  metadata, vendored SDKs, or deployment configuration.
- Do not merge or close any pull request without explicit owner authorization.
