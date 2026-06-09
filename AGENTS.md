# AGENTS.md

## Repository purpose

`garethpaul/workoutpact-app-ios` is an Apple platform application or Swift sample. Donation app if you miss a workout.

## Project structure

- `Makefile` - repository verification targets
- `scripts` - baseline checks and helper scripts
- `docs` - plans, notes, and generated README assets
- `Podfile` - CocoaPods dependency definition
- `workoutpact.xcodeproj` - Xcode project
- `workoutpact.xcworkspace` - Xcode workspace
- `DigitsKit.framework` - repository source or sample assets
- `Fabric.framework` - repository source or sample assets
- `TwitterCore.framework` - repository source or sample assets
- `TwitterKit.framework` - repository source or sample assets
- `workoutpact` - repository source or sample assets
- `workoutpactTests` - repository source or sample assets

## Development commands

- Install dependencies: `pod install`
- Full baseline: `make check`
- Combined verification: `make verify`
- Lint/static checks: `make lint`
- Tests: `make test`
- Build: `make build`
- Local Apple development: `open workoutpact.xcworkspace`
- If a command above skips because a platform toolchain is missing, verify on a machine with that SDK before claiming platform behavior is tested.

## Coding conventions

- Language mix noted in the README: C/C++ headers (40), Swift (8).
- Use the CocoaPods workspace when present; update `Podfile.lock` only with an intentional dependency change.
- Preserve legacy Xcode project settings and signing assumptions unless the change is explicitly about modernization.

## Testing guidance

- Test-related files detected: `workoutpactTests/workoutpactTests.swift`
- Start with the narrowest relevant test or Make target, then run `make check` before handing off if the change is not documentation-only.
- Keep README verification notes in sync when commands, fixtures, or supported toolchains change.

## PR / change guidance

- Keep diffs focused on the requested repository and avoid unrelated modernization or formatting churn.
- Preserve public APIs, sample behavior, file formats, and documented environment variables unless the task explicitly changes them.
- Update tests, README notes, or docs/plans when behavior, security posture, or validation commands change.
- Call out skipped platform validation, legacy toolchain assumptions, and any risky files touched in the final summary.

## Safety and gotchas

- Detected references to Twitter. Keep API keys, OAuth credentials, tokens, and account-specific values in local configuration only.
- `workoutpact/Info.plist` contains placeholder URL scheme metadata only. Replace placeholder Twitter/Digits/Fabric values locally when running the legacy prototype, and do not commit real credentials.
- `workoutpact/Info.plist` contains an empty `StripePublishableKey` placeholder. Configure a real `pk_` publishable key locally and keep billing disabled unless a backend contract and tests exist.
- The shake-to-share flow should always require explicit user confirmation before opening Twitter composition.
- The shake-to-share flow should gate on the delivered motion subtype before presenting the confirmation prompt.
- This looks like an Apple platform project or sample. Xcode, Swift, CocoaPods, and deployment target versions may need to match the original project era.

## Agent workflow

1. Inspect the README, Makefile, manifests, and the files directly related to the request.
2. Make the smallest source or docs change that satisfies the task; avoid generated, vendored, or local-environment files unless required.
3. Run the narrowest useful validation first, then `make check` or the documented package/platform gate when available.
4. If a required SDK, service credential, or external runtime is unavailable, record the skipped command and why.
5. Summarize changed files, commands run, and remaining risks or follow-up validation.
