#!/usr/bin/env python3
"""Static contracts for the legacy WorkoutPact iOS project."""

from pathlib import Path
import plistlib
import re
import sys


ROOT = Path(__file__).resolve().parents[1]


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
        "error != nil || session == nil" in login,
        "Twitter login must not advance to phone verification on cancelled or failed login",
        failures,
    )
    require(
        "error != nil || session == nil" in two_factor,
        "Digits verification must not advance to protected content on cancelled or failed verification",
        failures,
    )
    require(
        "payButton!.enabled = false" in payment,
        "payment submit button must start disabled until PaymentKit validates card input",
        failures,
    )
    require(
        "paymentView == nil || paymentView!.card == nil" in payment,
        "payment flow must guard missing PaymentKit card input before tokenization",
        failures,
    )
    require(
        "error != nil || token == nil" in payment,
        "payment flow must not advance when Stripe tokenization fails",
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
        "var kbHeight: CGFloat = 0" in workout,
        "keyboard animation state must not use an implicitly unwrapped height",
        failures,
    )

    if failures:
        print("WorkoutPact contract check failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("WorkoutPact contract check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
