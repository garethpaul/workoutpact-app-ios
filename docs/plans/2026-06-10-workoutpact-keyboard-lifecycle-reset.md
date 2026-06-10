# WorkoutPact Keyboard Lifecycle Reset

Status: Completed

## Goal

Keep the protected screen in its original position when navigation occurs while
the keyboard is visible.

## Scope

- Add an idempotent keyboard-shift restoration method.
- Move the view back by the cached keyboard height when it is shifted.
- Clear the keyboard visibility flag and cached height after restoration.
- Restore the frame before removing keyboard notification observers during
  view disappearance.
- Enforce the lifecycle ordering and reset state in portable contracts.

## Verification

- `make check`
- Mutation check: removing the disappearance-time restoration call causes the
  contract checker to fail.
- Xcode build skipped locally because `xcodebuild` is unavailable; hosted
  Linux verification intentionally exercises the portable contracts.

## Outcome

Leaving the protected screen with an open keyboard no longer leaves its frame
shifted or its keyboard state stale. Returning to the screen starts from a
stable layout and can process the next keyboard notification normally.
