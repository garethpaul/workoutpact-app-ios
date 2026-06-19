#!/usr/bin/env python3
"""Mutation-sensitive contracts for legacy async payment/auth/share flows."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8")


def require(condition, message, failures):
    if not condition:
        failures.append(message)


def before(source, first, second):
    return first in source and second in source and source.index(first) < source.index(second)


def validate_payment(source, failures):
    require("var paymentFlowInFlight = false" in source, "payment flow needs one in-flight owner", failures)
    require(
        "button.enabled = valid && !paymentFlowInFlight" in source,
        "card validation must not re-enable submit during an active flow",
        failures,
    )
    require(
        "if !paymentViewVisible || paymentFlowInFlight" in source,
        "payment entry must reject hidden or duplicate submissions",
        failures,
    )
    require(
        before(source, "paymentFlowInFlight = true", "createTokenWithCard"),
        "payment flow must be claimed before tokenization starts",
        failures,
    )
    require(
        "createTokenWithCard(card, completion: { [weak self]" in source,
        "Stripe completion must not retain the payment controller",
        failures,
    )
    require(
        "dispatch_async(dispatch_get_main_queue(), { [weak self] in" in source,
        "payment main-queue hop must preserve weak ownership",
        failures,
    )
    require(
        "!controller.paymentFlowInFlight" in source,
        "Stripe completion must reject duplicate completion delivery",
        failures,
    )
    require(
        "controller.paymentFlowInFlight = false" in source,
        "failed or cancelled payment flows must release their reservation",
        failures,
    )
    require(
        "handler: { [weak self] action in" in source,
        "payment alert actions must not retain the controller",
        failures,
    )


def validate_two_factor(source, failures):
    require(
        "var authenticationRequestInFlight = false" in source,
        "Digits flow needs one in-flight owner",
        failures,
    )
    require(
        "if !authenticationContextActive || authenticationRequestInFlight" in source,
        "Digits entry must reject inactive or duplicate requests",
        failures,
    )
    require(
        before(source, "authenticationRequestInFlight = true", "authenticateWithDigitsAppearance"),
        "Digits flow must be claimed before provider presentation",
        failures,
    )
    require(
        "authenticateWithDigitsAppearance(digitsAppearance, viewController: nil, title: \"Two Factor Authentication\") { [weak self]" in source,
        "Digits completion must not retain the controller",
        failures,
    )
    require(
        "dispatch_async(dispatch_get_main_queue(), { [weak self] in" in source,
        "Digits result handling must be weakly owned on the main queue",
        failures,
    )
    require(
        "!controller.authenticationRequestInFlight" in source,
        "Digits completion must reject duplicate delivery",
        failures,
    )
    require(
        "controller.authenticationRequestInFlight = false" in source,
        "failed Digits attempts must release their reservation",
        failures,
    )


def validate_login(source, failures):
    appearance = source.split("override func viewWillAppear", 1)[1].split(
        "override func viewWillDisappear", 1
    )[0]
    completion = source.split("TWTRLogInButton", 1)[1]
    require(
        "loginTransitionInFlight = false" not in appearance,
        "a resumed login screen must not forget an already-consumed success callback",
        failures,
    )
    require(
        "if controller.presentedViewController != nil" in completion,
        "Twitter success must not overlap another presentation",
        failures,
    )
    require(
        before(
            completion,
            'instantiateViewControllerWithIdentifier("TwoFactorViewController")',
            "controller.loginTransitionInFlight = true",
        ),
        "Twitter transition must only be claimed after the destination exists",
        failures,
    )
    require(
        before(
            completion,
            "controller.loginTransitionInFlight = true",
            "controller.presentViewController",
        ),
        "Twitter transition must be claimed immediately before presentation",
        failures,
    )


def validate_shake(source, failures):
    require("var shareFlowInFlight = false" in source, "share flow needs one in-flight owner", failures)
    require(
        "if shareFlowInFlight || self.presentedViewController != nil" in source,
        "shake handling must reject duplicate or overlapping presentation",
        failures,
    )
    require(
        before(source, "shareFlowInFlight = true", "let alert = UIAlertController"),
        "share flow must be claimed before constructing the alert",
        failures,
    )
    require(
        "style: UIAlertActionStyle.Cancel, handler: { [weak self]" in source,
        "cancelling share confirmation must weakly release the reservation",
        failures,
    )
    require(
        "style: UIAlertActionStyle.Default, handler: { [weak self]" in source,
        "share confirmation must not retain the controller",
        failures,
    )
    require(
        "composer.showWithCompletion { [weak self]" in source,
        "Twitter composer completion must not retain the controller",
        failures,
    )
    require(
        source.count("controller.shareFlowInFlight = false") >= 2,
        "cancel and composer completion must both release the share reservation",
        failures,
    )


def validate_config(source, documentation, failures):
    require(
        'trimmedKey.hasPrefix("pk_test_")' in source and 'pk_live_' not in source,
        "the legacy prototype must accept only Stripe test-mode publishable keys",
        failures,
    )
    require(
        "rangeOfCharacterFromSet(NSCharacterSet.whitespaceAndNewlineCharacterSet()) == nil" in source,
        "Stripe configuration must reject embedded whitespace",
        failures,
    )
    require(
        "server-authoritative integer minor units" in documentation
        and "ISO 4217 allowlist" in documentation,
        "billing boundary must require server-side amount and currency validation",
        failures,
    )


def validate_all(sources):
    failures = []
    validate_payment(sources["payment"], failures)
    validate_two_factor(sources["two_factor"], failures)
    validate_login(sources["login"], failures)
    validate_shake(sources["shake"], failures)
    validate_config(sources["app_delegate"], sources["documentation"], failures)
    return failures


def mutate(source, target, replacement):
    changed = source.replace(target, replacement, 1)
    if changed == source:
        raise AssertionError("mutation target missing: {0}".format(target))
    return changed


def main():
    sources = {
        "payment": read("workoutpact/PaymentViewController.swift"),
        "two_factor": read("workoutpact/TwoFactorViewController.swift"),
        "login": read("workoutpact/LoginViewController.swift"),
        "shake": read("workoutpact/ShakeViewContorller.swift"),
        "app_delegate": read("workoutpact/AppDelegate.swift"),
        "documentation": read("SECURITY.md"),
    }
    failures = validate_all(sources)
    if failures:
        raise SystemExit("baseline async-flow contract failed:\n- " + "\n- ".join(failures))

    mutations = {
        "payment duplicate guard": ("payment", " || paymentFlowInFlight", ""),
        "payment weak provider capture": ("payment", "completion: { [weak self]", "completion: {"),
        "Digits duplicate guard": ("two_factor", " || authenticationRequestInFlight", ""),
        "Digits weak provider capture": ("two_factor", ") { [weak self]", ") {"),
        "login resume consumption": ("login", "        loginContextActive = true\n", "        loginContextActive = true\n        loginTransitionInFlight = false\n"),
        "login presentation overlap": ("login", "                    if controller.presentedViewController != nil {\n                        return\n                    }\n", ""),
        "shake duplicate guard": ("shake", "shareFlowInFlight || ", ""),
        "shake weak composer capture": ("shake", "composer.showWithCompletion { [weak self]", "composer.showWithCompletion {"),
        "publishable key class": ("app_delegate", 'trimmedKey.hasPrefix("pk_test_")', 'trimmedKey.hasPrefix("pk_")'),
        "billing amount boundary": ("documentation", "server-authoritative integer minor units", "client-provided amount"),
    }
    accepted = []
    for description, (key, target, replacement) in mutations.items():
        candidate = dict(sources)
        candidate[key] = mutate(candidate[key], target, replacement)
        if not validate_all(candidate):
            accepted.append(description)
    if accepted:
        raise SystemExit("mutations unexpectedly passed: " + ", ".join(accepted))

    print("async-flow safety contract passed ({0} mutations rejected).".format(len(mutations)))


if __name__ == "__main__":
    main()
