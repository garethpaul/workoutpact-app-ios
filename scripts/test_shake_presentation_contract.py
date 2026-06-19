#!/usr/bin/env python3
"""Mutation checks for shake confirmation presentation ownership."""

from pathlib import Path

from check_workoutpact_contracts import validate_shake_presentation


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "workoutpact/ShakeViewContorller.swift"
GUARD = "        if shareFlowInFlight || self.presentedViewController != nil {\n            return\n        }\n"
CLAIM = "        shareFlowInFlight = true\n"
ALERT = '        let alert = UIAlertController(title: "Share workout", message: "Post your completed workout to Twitter?", preferredStyle: UIAlertControllerStyle.Alert)'
PRESENTATION = "        self.presentViewController(alert, animated: true, completion: nil)"


def rejects(source):
    failures = []
    try:
        validate_shake_presentation(source, failures)
    except (IndexError, ValueError):
        return True
    return bool(failures)


def main():
    baseline = SOURCE.read_text(encoding="utf-8")
    failures = []
    validate_shake_presentation(baseline, failures)
    if failures:
        raise SystemExit("baseline contract failed: " + "; ".join(failures))

    mutations = {
        "missing guard": baseline.replace(GUARD, "", 1),
        "inverted guard": baseline.replace(
            "if shareFlowInFlight || self.presentedViewController != nil",
            "if !shareFlowInFlight && self.presentedViewController == nil",
            1,
        ),
        "missing claim": baseline.replace(CLAIM, "", 1),
        "guard after alert construction": baseline.replace(GUARD, "", 1).replace(
            ALERT,
            ALERT + "\n\n" + GUARD.rstrip(),
            1,
        ),
        "guard after alert presentation": baseline.replace(GUARD, "", 1).replace(
            PRESENTATION,
            PRESENTATION + "\n\n" + GUARD.rstrip(),
            1,
        ),
    }
    accepted = [name for name, source in mutations.items() if not rejects(source)]
    if accepted:
        raise SystemExit("mutations unexpectedly passed: " + ", ".join(accepted))

    print(f"shake-presentation contract passed; {len(mutations)} mutations rejected")


if __name__ == "__main__":
    main()
