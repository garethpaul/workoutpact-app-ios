# WorkoutPact Digits Import Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use executing-plans to implement this plan task-by-task.

**Goal:** Restore the protected logout controller's direct access to the Digits SDK by importing the module in the Swift source file that calls it.

**Architecture:** Keep framework ownership explicit at the file boundary. Add a mutation-sensitive portable contract requiring `import DigitsKit` in `ViewController.swift`, then add the one missing import without widening the Objective-C bridging header or changing logout behavior.

**Tech Stack:** Swift 1-era UIKit application, DigitsKit binary framework, Python 3 mutation contracts, GNU Make verification.

---

## Status: Completed

## Evidence And Decision

- `workoutpact/ViewController.swift` calls `Digits.sharedInstance().logOut()` but imports only `UIKit` and `TwitterKit`.
- `workoutpact/BridgeHeader.h` exposes Stripe and PaymentKit only; it does not expose DigitsKit declarations.
- Every other Swift source file that uses Digits imports `DigitsKit` explicitly.
- Swift's language reference states that an import declaration makes external module symbols available in the current file.
- Adding `DigitsKit` to the bridging header would broaden SDK visibility across every Swift file. Removing the Digits logout call would leave a retained authentication session. A direct source-file import is the smallest correct repair.

### Task 1: Add the failing module contract

**Files:**
- Modify: `scripts/test_async_flow_safety_contract.py`

**Step 1: Require the direct import**

Extend `validate_logout(...)` to require `import DigitsKit` before the logout
controller declaration. Add a hostile mutation that removes the import.

**Step 2: Verify RED**

Run: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_async_flow_safety_contract.py`

Expected: FAIL because `ViewController.swift` uses Digits without importing
DigitsKit.

### Task 2: Add the missing import

**Files:**
- Modify: `workoutpact/ViewController.swift`

**Step 1: Implement minimal repair**

Add:

```swift
import DigitsKit
```

beside the existing UIKit and TwitterKit imports.

**Step 2: Verify GREEN**

Run the focused mutation contract again.

Expected: PASS, including the missing-import mutation.

### Task 3: Document and validate

**Files:**
- Modify: `README.md`
- Modify: `VISION.md`
- Modify: `CHANGES.md`
- Modify: `docs/plans/2026-06-25-workoutpact-digits-import.md`

**Step 1: Record the module boundary**

Document that Swift files directly using retained legacy SDK symbols must
import their defining modules and that the bridging header remains limited to
Objective-C payment dependencies.

**Step 2: Run repository verification**

Run: `make check`

Expected: all portable contracts pass; `xcodebuild` may skip when the legacy
macOS toolchain is unavailable.

**Step 3: Commit**

```bash
git add workoutpact/ViewController.swift scripts/test_async_flow_safety_contract.py \
  README.md VISION.md CHANGES.md \
  docs/plans/2026-06-25-workoutpact-digits-import.md
git commit -m "fix: import Digits in logout controller"
```

## Validation Evidence

- The focused async-flow contract failed against the original source because
  `ViewController.swift` did not import DigitsKit.
- The focused contract passed after the direct import was added and rejected
  all thirteen hostile mutations, including removal of that import.
- Host `/usr/bin/make check` passed Make authority and Python compilation, then
  stopped because Ruby is not installed for semantic workflow parsing.
- Ruby 3.3.11 container `/usr/bin/make check` with Python 3.11.2 and GNU Make
  4.3 passed the complete portable contract and mutation gate; Xcode was
  unavailable and skipped as designed.
- Legacy Xcode compilation remains conditional on a compatible macOS
  environment with the retained Pods and SDKs available.
