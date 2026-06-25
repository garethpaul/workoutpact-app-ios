# Changes

## 2026-06-25 16:30 PDT - P1 - Restore logout Digits module import

### Summary

Restored the protected logout controller's direct access to the Digits SDK by
importing `DigitsKit` in the Swift file that clears the Digits session.

### Work completed

- Added the missing file-scoped `DigitsKit` import without widening the
  Objective-C bridging header.
- Extended the async-flow mutation suite from twelve to thirteen rejected
  mutations with a missing-import control.
- Documented the retained SDK module boundary and implementation evidence.

### Threads

- None. Source tracing, the checked-in bridging header, sibling Swift imports,
  and Swift's official import semantics converged on the same focused repair.

### Files changed

- `workoutpact/ViewController.swift` — imported the DigitsKit module used by
  logout session clearing.
- `scripts/test_async_flow_safety_contract.py` — required and mutation-tested
  the direct module import.
- `README.md`, `VISION.md`, and
  `docs/plans/2026-06-25-workoutpact-digits-import.md` — documented the build
  boundary and validation plan.

### Validation

- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_async_flow_safety_contract.py`
  — failed before the Swift change with the missing DigitsKit import finding,
  then passed with thirteen hostile mutations rejected.
- Host `/usr/bin/make check` — Make authority and Python compilation passed,
  then the workflow contract stopped because Ruby is not installed.
- Ruby 3.3.11 container `/usr/bin/make check` with Python 3.11.2 and GNU Make
  4.3 — passed the complete portable contract and mutation gate; Xcode was
  unavailable and skipped as designed.

### Bugs / findings

- `ViewController.swift` called `Digits.sharedInstance()` without importing the
  external module that defines `Digits`; imports in other Swift files do not
  expose those symbols to this file.

### Blockers

- Compatible legacy Xcode and SDK validation is unavailable on this Linux host.
- The nested Codex CLI remains unauthenticated, so required branch review may
  fail before analysis with HTTP 401.

### Next action

- Run `/usr/bin/make check`, open a focused pull request, require hosted checks
  and Codex review, and merge only after both are clean.

## 2026-06-25 - P2 - Reserve logout navigation ownership

- Rejected repeated logout taps and overlapping modal presentation before
  queueing another login controller.
- Claimed logout transition ownership before clearing Digits and Twitter
  sessions, then weakly revalidated it on the main queue.
- Released the reservation when login storyboard lookup or casting fails.
- Extended the async-flow mutation suite from ten to twelve rejected mutations.

## 2026-06-24 22:58 PDT - P2 - Surface workflow parser failures truthfully

### Summary

Completed the legacy SDK boundary revalidation note, then corrected the hosted
workflow checker so unavailable Ruby/Psych infrastructure cannot masquerade as
credential-policy failures or satisfy hostile mutation checks.

### Work completed

- Required `make check` plus compatible Xcode/device verification after future
  legacy SDK boundary or referenced dependency changes.
- Preserved YAML parser errors separately from semantic workflow rejection.
- Added missing-parser and mutation-parser regression coverage.
- Kept the Make authority synthetic checkout aligned with every invoked script.

### Threads

- Started and reviewed: code trace, history, blast-radius, and independent
  hypothesis investigations — all converged on parser error-state loss.
- Started and reviewed: TDD implementer — completed the focused repair.
- Started and reviewed: correctness, quality, and security reviewers — all
  approved after two targeted review findings were resolved.

### Files changed

- `docs/plans/2026-06-10-workoutpact-legacy-sdk-modernization-boundary.md` —
  documented required revalidation after boundary changes.
- `scripts/check_workoutpact_contracts.py` — separated parser infrastructure
  errors from semantic workflow results.
- `scripts/test_check_workoutpact_contracts.py` — added two parser-failure
  regression tests.
- `scripts/test-makefile-root.sh` — included the new test in the synthetic
  authority checkout.
- `Makefile` — compiled and executed the regression test.
- `docs/plans/2026-06-24-workflow-parser-diagnostics.md` — recorded the repair
  plan and acceptance evidence.
- `docs/fixes/2026-06-24-workflow-parser-diagnostics.md` — documented the
  diagnosis, repair, testing, and review verdicts.

### Validation

- `python3 scripts/test_check_workoutpact_contracts.py` — two tests passed.
- Pre-fix mutation control — the mutation-parser regression failed against the
  old checker, proving it detects continued evaluation after parser failure.
- `/bin/sh scripts/test-makefile-root.sh` — all 35 authority cases passed.
- Ubuntu 24.04 container `/usr/bin/make check` with Ruby 3.2.3, Psych 5.0.1,
  Python 3.12.3, and GNU Make 4.3 — passed all contracts and mutations; Xcode
  was unavailable and skipped as designed.
- Fixer review — correctness, quality, and security approved.
- Codex review helper against `origin/master` — attempted three times after
  push; each run stopped before analysis with HTTP 401 because the nested Codex
  CLI identity was not authenticated.
- Hosted push and pull-request checks at `996de28` — all Python 3.10, 3.12, and
  3.14 static-contract jobs plus CodeQL passed.

### Bugs / findings

- Fixed a P2 verification defect where missing parser infrastructure produced
  false checkout-policy diagnostics and could make mutation rejection pass
  without semantic parsing.

### Blockers

- Compatible macOS Xcode and device verification remains required before a
  release that changes the retained legacy SDK boundary or dependencies.
- The required Codex review cannot run until the local nested Codex CLI identity
  is authenticated; no merge should occur before that review completes cleanly.

### Next action

- Authenticate the nested Codex CLI, rerun branch review against `master`, and
  merge PR #18 only if the review reports no accepted actionable findings.

## 2026-06-21

- Isolated repository verification from caller-controlled Make startup files,
  shell state, execution modes, root overrides, Python/Xcode expressions, and
  later public recipe replacement.
- Documented and tested caller-added double-colon recipes from additional
  later `-f` files as outside the repository Make trust boundary.
- Documented and tested version-specific explicit `-f` Make-syntax paths as pre-load caller authority.
- Covered GNU Make 4.2.1's explicit `-f` pre-load behavior in the portable authority regression harness.
- Added adversarial Make authority coverage and bound hosted verification to
  `/usr/bin/make` without changing Swift, pods, frameworks, or Xcode settings.
- Disabled persisted Git credentials in hosted verification and bound that
  guarantee to the immutable checkout step with hostile contract mutations.
- Parse the hosted workflow semantically so block-scalar decoys, aliases,
  duplicate keys, extra checkout steps, and run-command decoys cannot satisfy
  the static contract.

## 2026-06-19

- Reserved Stripe tokenization and Digits authentication before provider calls,
  rejected duplicate completions, and weakly owned their callbacks.
- Kept successful Twitter transition ownership consumed across resumed login
  appearances and claimed it only after the two-factor destination exists.
- Reserved the complete shake confirmation/composer flow until cancel or
  provider completion so presentation transitions cannot overlap.
- Restricted Stripe configuration to non-empty test-mode `pk_test_` values
  without embedded whitespace, rejected live-mode keys, and documented
  server-authoritative amount and ISO 4217 currency validation for any future
  billing backend.
- Added ten mutation-sensitive async-flow contracts to the portable gate.

## 2026-06-16

- Rejected overlapping shake confirmation while the workout controller already
  presents another modal view; the June 19 flow reservation extends this across
  alert dismissal and Twitter composer presentation.
- Added a single Twitter login transition guard so duplicate successful
  callbacks cannot present multiple two-factor screens from one appearance;
  the June 19 guard remains consumed after the login screen resumes.
- Broke the Twitter login button retain cycle with weak provider and queued
  main-thread callback captures while preserving stale-lifecycle rejection.

## 2026-06-15

- Rejected successful Twitter login callbacks after the login controller is
  dismissed or removed, before storyboard lookup or phone-verification UI.
- Added lifecycle and ordering contracts for stale Twitter login completions.

## 2026-06-14

- Moved the Stripe generation and visibility guard ahead of payment-button and
  tokenization-error handling so stale completions cannot mutate current UI.
- Added mutation-sensitive ordering coverage for the complete payment callback.

## 2026-06-13

- Bound Stripe and Digits requests to controller lifecycle generations so
  pre-dismissal callbacks remain invalid after a later appearance.
- Rejected Stripe tokenization requests and asynchronous completions after the
  payment screen is covered, before billing UI can be presented.
- Added portable lifecycle ordering contracts for both payment visibility
  guards.

## 2026-06-10

- Restored any active protected-screen keyboard offset before navigation
  removes observers, clearing stale visibility and height state for the next
  appearance.
- Documented and enforced the versioned legacy SDK modernization boundary for
  Swift 1-era syntax, iOS 8.3, Stripe 4.0.3, PaymentKit 1.1.1, and retired
  Fabric, DigitsKit, TwitterCore, and TwitterKit SDKs.
- Added immutable, read-only GitHub Actions verification on Python 3.10, 3.12,
  and 3.14 for the credential, payment, authentication, and sharing contracts,
  with manual dispatch for maintenance runs.
- Added static protection for workflow permissions, action revisions, matrix
  versions, timeout, and the `make check` entry point.
- Documented that hosted Linux checks intentionally skip the legacy Xcode build.
- Added an explicit post-tokenization notice that no donation or charge was
  created and requires `Continue without billing` before sharing.
- Pinned hosted verification to Ubuntu 24.04 with superseded-run cancellation
  and made static and optional workspace checks root-independent.

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
