#!/usr/bin/env python3
"""Static contracts for the legacy WorkoutPact iOS project."""

from pathlib import Path
import plistlib
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
DOCS_PLANS = ROOT / "docs/plans"
CANONICAL_PLANS = [
    DOCS_PLANS / "2026-06-08-workoutpact-build-privacy-contracts.md",
    DOCS_PLANS / "2026-06-08-workoutpact-auth-payment-sharing-guards.md",
    DOCS_PLANS / "2026-06-08-workoutpact-logout-navigation-guard.md",
    DOCS_PLANS / "2026-06-08-workoutpact-payment-button-guard.md",
    DOCS_PLANS / "2026-06-09-workoutpact-payment-input-guard.md",
    DOCS_PLANS / "2026-06-09-workoutpact-storyboard-cast-guards.md",
    DOCS_PLANS / "2026-06-09-workoutpact-payment-error-log.md",
    DOCS_PLANS / "2026-06-09-workoutpact-payment-key-guard.md",
    DOCS_PLANS / "2026-06-09-workoutpact-textfield-outlet-guard.md",
    DOCS_PLANS / "2026-06-09-workoutpact-share-result-log.md",
    DOCS_PLANS / "2026-06-09-workoutpact-keyboard-shift-guard.md",
]


def read_text(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8")


def read_plist(relative_path, failures):
    path = ROOT / relative_path
    if not path.exists():
        failures.append(f"{relative_path} is missing")
        return {}

    try:
        with path.open("rb") as plist_file:
            return plistlib.load(plist_file)
    except Exception as exc:
        failures.append(f"{relative_path} is not a valid plist: {exc}")
        return {}


def require(condition, message, failures):
    if not condition:
        failures.append(message)


def plist_url_schemes(plist):
    schemes = []
    for entry in plist.get("CFBundleURLTypes", []):
        schemes.extend(entry.get("CFBundleURLSchemes", []))
    return schemes


def main():
    failures = []

    app_plist = read_plist("workoutpact/Info.plist", failures)
    test_plist = read_plist("workoutpactTests/Info.plist", failures)
    gitignore = read_text(".gitignore")
    project = read_text("workoutpact.xcodeproj/project.pbxproj")
    app_delegate = read_text("workoutpact/AppDelegate.swift")
    login = read_text("workoutpact/LoginViewController.swift")
    two_factor = read_text("workoutpact/TwoFactorViewController.swift")
    payment = read_text("workoutpact/PaymentViewController.swift")
    shake = read_text("workoutpact/ShakeViewContorller.swift")
    workout = read_text("workoutpact/ViewController.swift")
    plans = sorted(DOCS_PLANS.glob("*.md")) if DOCS_PLANS.is_dir() else []

    required_app_keys = [
        "CFBundleDisplayName",
        "CFBundleExecutable",
        "CFBundleIdentifier",
        "CFBundleName",
        "CFBundleShortVersionString",
        "CFBundleVersion",
        "LSRequiresIPhoneOS",
        "UILaunchStoryboardName",
        "UIMainStoryboardFile",
    ]
    missing_app_keys = [key for key in required_app_keys if not app_plist.get(key)]
    require(
        not missing_app_keys,
        "app Info.plist missing required keys: " + ", ".join(missing_app_keys),
        failures,
    )
    require(
        app_plist.get("CFBundlePackageType") == "APPL",
        "app Info.plist must describe an application bundle",
        failures,
    )
    require(
        app_plist.get("NSContactsUsageDescription"),
        "app Info.plist must document contact permission use for legacy Digits flows",
        failures,
    )
    require(
        app_plist.get("StripePublishableKey", None) == "",
        "app Info.plist must include an empty StripePublishableKey placeholder only",
        failures,
    )
    schemes = plist_url_schemes(app_plist)
    invalid_schemes = [
        scheme for scheme in schemes if not re.match(r"^[A-Za-z][A-Za-z0-9+.-]*$", scheme)
    ]
    require(
        not invalid_schemes,
        "app Info.plist has invalid URL schemes: " + ", ".join(invalid_schemes),
        failures,
    )
    require("workoutpact" in schemes, "app Info.plist must declare the workoutpact URL scheme", failures)
    require(
        any(scheme.startswith("twitterkit-") for scheme in schemes),
        "app Info.plist must declare a twitterkit-* callback URL scheme",
        failures,
    )
    require(
        test_plist.get("CFBundlePackageType") == "BNDL",
        "test Info.plist must describe a bundle",
        failures,
    )
    require(
        "!workoutpact/Info.plist" in gitignore
        and "!workoutpactTests/Info.plist" in gitignore,
        ".gitignore must allow the project plist files to be tracked",
        failures,
    )

    require(
        "INFOPLIST_FILE = workoutpact/Info.plist;" in project,
        "project file must point the app target at workoutpact/Info.plist",
        failures,
    )
    require(
        not re.search(r"/Users/|[A-Za-z]:\\\\", project),
        "project file must not contain machine-local absolute paths",
        failures,
    )
    require(
        project.count("SWIFT_OBJC_BRIDGING_HEADER = workoutpact/BridgeHeader.h;") == 2,
        "Debug and Release builds must use the checked-in bridging header",
        failures,
    )
    require(
        "SWIFT_OBJC_BRIDGING_HEADER[arch=*]" not in project,
        "Swift bridging header must not use architecture-specific absolute overrides",
        failures,
    )

    require(
        "let StripePublishableKey" not in app_delegate
        and 'objectForInfoDictionaryKey("StripePublishableKey")' in app_delegate
        and "Stripe.setDefaultPublishableKey(publishableKey)" in app_delegate,
        "Stripe publishable key must be read from Info.plist and applied only when configured",
        failures,
    )
    require(
        'hasPrefix("pk_")' in app_delegate,
        "Stripe publishable key loader must validate configured values as pk_* keys",
        failures,
    )
    require(
        not re.search(r"pk_(?:test|live)_[A-Za-z0-9]{8,}", app_delegate + str(app_plist)),
        "Stripe publishable keys must not be committed to source",
        failures,
    )
    require(
        "error != nil || session == nil" in login,
        "Twitter login must not advance to phone verification on cancelled or failed login",
        failures,
    )
    require(
        "if let storyboard = self.storyboard" in login,
        "Twitter login must guard storyboard lookup before presenting phone verification",
        failures,
    )
    require(
        "as! TwoFactorViewController" not in login
        and "as? TwoFactorViewController" in login,
        "Twitter login must safely cast the phone verification controller",
        failures,
    )
    require(
        "error != nil || session == nil" in two_factor,
        "Digits verification must not advance to protected content on cancelled or failed verification",
        failures,
    )
    require(
        "dispatch_async(dispatch_get_main_queue()" in two_factor,
        "Digits verification must perform protected segue on the main queue",
        failures,
    )
    require(
        "payButton!.enabled" not in payment,
        "payment button state updates must not force-unwrap payButton",
        failures,
    )
    require(
        "if let button = payButton" in payment
        and "button.enabled = false" in payment
        and "button.enabled = valid" in payment
        and "if let button = self.payButton" in payment
        and "button.enabled = true" in payment,
        "payment submit button state must be guarded while preserving validation and token callback behavior",
        failures,
    )
    require(
        "paymentView!" not in payment
        and "if let paymentInput = paymentView" in payment
        and "paymentInput.card == nil" in payment
        and "let paymentCard = paymentInput.card" in payment,
        "payment flow must guard PaymentKit input without force-unwrapping paymentView",
        failures,
    )
    require(
        "configuredStripePublishableKey() == nil" in payment,
        "payment flow must stop before tokenization when Stripe publishable key is missing",
        failures,
    )
    require(
        'NSLog("Stripe publishable key is not configured; payment tokenization is disabled.")' in payment,
        "payment flow must log a non-sensitive missing Stripe key message",
        failures,
    )
    require(
        "configuredStripePublishableKey() == nil" in payment
        and payment.index("configuredStripePublishableKey() == nil")
        < payment.index("STPAPIClient.sharedClient().createTokenWithCard"),
        "Stripe publishable key guard must run before token creation",
        failures,
    )
    require(
        "error != nil || token == nil" in payment,
        "payment flow must not advance when Stripe tokenization fails",
        failures,
    )
    require(
        'NSLog("Stripe tokenization failed.")' in payment
        and "Stripe tokenization failed: \\(error)" not in payment
        and "\\(error)" not in payment,
        "payment tokenization failures must not log raw Stripe error objects",
        failures,
    )
    require(
        "dispatch_async(dispatch_get_main_queue()" in payment,
        "payment token callback must return to the main queue before UI updates",
        failures,
    )
    require(
        "create charge" not in payment.lower(),
        "payment comments must not imply the prototype creates charges",
        failures,
    )
    require(
        "UIAlertController" in shake
        and "presentTweetComposer" in shake
        and "Just finished my workout via #workoutpact" in shake
        and "Just finshed" not in shake,
        "shake sharing must require explicit confirmation and use the corrected share text",
        failures,
    )
    require(
        "println(" not in shake
        and "Tweet composition cancelled" not in shake
        and "Sending tweet!" not in shake,
        "shake sharing must not log Twitter composer outcomes",
        failures,
    )
    require(
        "var kbHeight: CGFloat = 0" in workout,
        "keyboard animation state must not use an implicitly unwrapped height",
        failures,
    )
    require(
        "var keyboardIsVisible = false" in workout,
        "keyboard animation state must track whether the view is already shifted",
        failures,
    )
    require(
        "if keyboardIsVisible {\n            return\n        }" in workout,
        "keyboardWillShow must ignore duplicate show notifications",
        failures,
    )
    require(
        "if !keyboardIsVisible {\n            return\n        }" in workout,
        "keyboardWillHide must ignore hide notifications when the view is not shifted",
        failures,
    )
    require(
        "keyboardIsVisible = true" in workout
        and workout.index("keyboardIsVisible = true") < workout.index("self.animateTextField(true)"),
        "keyboardWillShow must mark the view shifted before animating upward",
        failures,
    )
    require(
        "keyboardIsVisible = false" in workout
        and workout.index("keyboardIsVisible = false") < workout.index("self.animateTextField(false)"),
        "keyboardWillHide must clear shifted state before animating downward",
        failures,
    )
    require(
        "if let workoutTextField = textField" in workout
        and "workoutTextField.delegate = self" in workout
        and "textField.delegate = self" not in workout,
        "protected screen must guard the text-field outlet before assigning its delegate",
        failures,
    )
    require(
        "if let storyboard = self.storyboard" in workout and "self.storyboard!" not in workout,
        "logout navigation must guard storyboard lookup before presenting login",
        failures,
    )
    require(
        "as! LoginViewController" not in workout
        and "as? LoginViewController" in workout,
        "logout navigation must safely cast the login controller",
        failures,
    )
    require(DOCS_PLANS.is_dir(), "docs/plans must exist", failures)
    require(plans, "docs/plans must contain completed maintenance plans", failures)
    for plan in CANONICAL_PLANS:
        require(plan in plans, f"{plan.relative_to(ROOT)} must be present", failures)

    for plan in plans:
        text = plan.read_text(encoding="utf-8")
        require(
            "status: completed" in text.lower() or "Status: Completed" in text,
            f"{plan.relative_to(ROOT)} must be completed",
            failures,
        )
        require("make check" in text, f"{plan.relative_to(ROOT)} must document make check verification", failures)

    if failures:
        print("WorkoutPact contract check failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("WorkoutPact contract check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
