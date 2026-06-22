# WorkoutPact Make Authority Isolation

## Status: Completed

## Context

The repository rooted its file arguments, but GNU Make still accepted caller-
controlled Python and Xcode expressions, shell state, startup files, unsafe
modes, and later public recipe replacement. Those inputs could redirect cleanup
or make verification execute different commands than the checked-in gate.

## Implementation

- Froze literal Python and Xcode executable values, `/bin/sh`, and the canonical
  repository root for every public verification target.
- Rejected startup files, replaced Makefile lists, executable Make syntax,
  non-executing or error-ignoring modes, and later single-colon recipes.
- Added an adversarial authority harness and bound hosted verification to
  `/usr/bin/make check`.

## Verification

- Repository-root and external-directory `make check` run the static contract
  suite, 35 focused lifecycle/ownership/presentation/async-flow mutations,
  cleanup, the authority harness, and the truthful legacy Xcode boundary.
- The authority harness covers 35 target/root/shell combinations, hostile
  literal Python and Xcode paths, ten raw Make-syntax controls, startup and
  Makefile-list boundaries, seven later recipe replacements, caller-added
  double-colon recipes, cleanup containment, PATH-Xcode rejection, and ten
  unsupported execution modes.

## Trust Boundary

GNU Make parses an earlier startup file before this Makefile can reject it, and
an explicit later `override` directive remains caller authority. A caller who
chooses the default `python3` still controls `PATH`; hosted verification installs
the reviewed Python runtime before invoking the fixed system Make executable.
The caller-added double-colon recipes from an additional later `-f` file are also
caller authority: GNU Make appends those recipes after the checked-in target
body, so the repository harness proves and documents that behavior instead of
claiming the checked-in Makefile can prevent it.
Make syntax in an explicit `-f` path is version-sensitive before the repository Makefile loads. The harness proves pre-load execution on GNU Make 3.81 and 4.2.1 and non-execution on the hosted GNU Make 4.3 gate; checkout paths containing literal `$(` must be invoked from inside the checkout without an explicit Makefile path.

## Scope Boundary

This change does not alter Swift source, pods, vendored frameworks, storyboards,
assets, Xcode project settings, deployment targets, signing, credentials, or
application behavior. Native compilation and physical-device validation still
require the documented compatible macOS/Xcode environment.
