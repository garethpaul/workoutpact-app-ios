# WorkoutPact Shake Motion Subtype Guard

## Status: Completed

## Context

The shake-to-share handler receives the detected `UIEventSubtype` as its
`motion` argument, but it checked `event.subtype` before showing the share
confirmation prompt. That made the gate depend on the event object instead of
the callback value UIKit already provides for this override.

## Objectives

- Preserve the explicit confirmation prompt before Twitter composition.
- Gate the share prompt on the delivered `motion` subtype.
- Avoid reading `event.subtype` in the shake handler.
- Cover the motion-subtype guard in dependency-free static checks.

## Work Completed

- Updated `motionEnded` to return unless `motion` is `.MotionShake`.
- Left the confirmation alert and tweet composer flow unchanged for real shake
  callbacks.
- Added static checker coverage for the delivered motion subtype guard.
- Updated README, VISION, and CHANGES.

## Verification

- `python3 scripts/check_workoutpact_contracts.py`
- `make check`
- `git diff --check`
