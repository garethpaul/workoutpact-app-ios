#!/usr/bin/env python3
from pathlib import Path

from check_workoutpact_contracts import validate_login_lifecycle


ROOT = Path(__file__).resolve().parents[1]
BASELINE = (ROOT / "workoutpact/LoginViewController.swift").read_text(encoding="utf-8")


def mutate(description, target, replacement):
    changed = BASELINE.replace(target, replacement, 1)
    if changed == BASELINE:
        raise AssertionError("{0} mutation did not alter the source".format(description))
    return changed


def reject(description, source):
    failures = []
    try:
        validate_login_lifecycle(source, failures)
    except (IndexError, ValueError):
        return
    if not failures:
        raise AssertionError("{0} mutation was accepted".format(description))


failures = []
validate_login_lifecycle(BASELINE, failures)
if failures:
    raise AssertionError("baseline login lifecycle invalid: {0}".format(failures))

guard = """                if !self.loginContextActive {
                    return
                }
"""
mutations = {
    "missing lifecycle state": mutate("missing lifecycle state", "    var loginContextActive = false\n", ""),
    "missing activation": mutate("missing activation", "        loginContextActive = true\n", ""),
    "missing dismissal invalidation": mutate("missing dismissal invalidation", "            loginContextActive = false\n", ""),
    "missing dismissal boundary": mutate("missing dismissal boundary", "self.isBeingDismissed() || ", ""),
    "missing navigation boundary": mutate("missing navigation boundary", " || self.isMovingFromParentViewController()", ""),
    "missing navigation-controller dismissal": mutate(
        "missing navigation-controller dismissal",
        " || self.navigationController?.isBeingDismissed() == true",
        "",
    ),
    "missing completion guard": mutate("missing completion guard", guard, ""),
    "guard after storyboard lookup": mutate(
        "guard after storyboard lookup",
        guard + "                if let storyboard = self.storyboard {",
        "                if let storyboard = self.storyboard {\n" + guard,
    ),
}
for description, source in mutations.items():
    reject(description, source)

print("login lifecycle contract tests passed ({0} mutations rejected).".format(len(mutations)))
