#!/usr/bin/env python3
from pathlib import Path

from check_workoutpact_contracts import validate_login_lifecycle, validate_login_transition


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

guard = """                    if !controller.loginContextActive {
                        return
                    }
"""
transition_guard = """                    if controller.loginTransitionInFlight {
                        return
                    }
"""
transition_claim = "                    controller.loginTransitionInFlight = true\n"
storyboard_lookup = "                    if let storyboard = controller.storyboard {"
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
        guard + transition_guard + transition_claim + storyboard_lookup,
        transition_guard + transition_claim + storyboard_lookup + "\n" + guard,
    ),
}
for description, source in mutations.items():
    reject(description, source)


def reject_transition(description, source):
    failures = []
    try:
        validate_login_transition(source, failures)
    except (IndexError, ValueError):
        return
    if not failures:
        raise AssertionError("{0} mutation was accepted".format(description))


transition_failures = []
validate_login_transition(BASELINE, transition_failures)
if transition_failures:
    raise AssertionError("baseline login transition invalid: {0}".format(transition_failures))

transition_mutations = {
    "missing transition state": mutate("missing transition state", "    var loginTransitionInFlight = false\n", ""),
    "missing transition reset": mutate("missing transition reset", "        loginTransitionInFlight = false\n", ""),
    "missing transition guard": mutate("missing transition guard", transition_guard, ""),
    "missing transition claim": mutate(
        "missing transition claim",
        transition_claim,
        "",
    ),
    "claim before lifecycle guard": mutate(
        "claim before lifecycle guard",
        guard + transition_guard + transition_claim,
        transition_claim + guard + transition_guard,
    ),
    "claim after storyboard lookup": mutate(
        "claim after storyboard lookup",
        transition_claim + storyboard_lookup,
        storyboard_lookup + "\n                        controller.loginTransitionInFlight = true",
    ),
}
for description, source in transition_mutations.items():
    reject_transition(description, source)

print(
    "login lifecycle contract tests passed ({0} mutations rejected).".format(
        len(mutations) + len(transition_mutations)
    )
)
