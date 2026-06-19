#!/usr/bin/env python3
from pathlib import Path

from check_workoutpact_contracts import validate_login_callback_ownership


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
        validate_login_callback_ownership(source, failures)
    except (IndexError, ValueError):
        return
    if not failures:
        raise AssertionError("{0} mutation was accepted".format(description))


failures = []
validate_login_callback_ownership(BASELINE, failures)
if failures:
    raise AssertionError("baseline login callback ownership invalid: {0}".format(failures))

mutations = {
    "strong provider capture": mutate(
        "strong provider capture",
        "TWTRLogInButton(logInCompletion: { [weak self]",
        "TWTRLogInButton(logInCompletion: {",
    ),
    "strong dispatch capture": mutate(
        "strong dispatch capture",
        "dispatch_async(dispatch_get_main_queue(), { [weak self] in",
        "dispatch_async(dispatch_get_main_queue(), {",
    ),
    "missing controller promotion": mutate(
        "missing controller promotion",
        "if let controller = self",
        "if self != nil",
    ),
    "controller promotion before dispatch": mutate(
        "controller promotion before dispatch",
        "dispatch_async(dispatch_get_main_queue(), { [weak self] in\n                if let controller = self {",
        "if let controller = self {\n            dispatch_async(dispatch_get_main_queue(), { [weak self] in",
    ),
    "presentation through self": mutate(
        "presentation through self",
        "controller.presentViewController",
        "self?.presentViewController",
    ),
}
for description, source in mutations.items():
    reject(description, source)

print("login callback ownership contract tests passed ({0} mutations rejected).".format(len(mutations)))
