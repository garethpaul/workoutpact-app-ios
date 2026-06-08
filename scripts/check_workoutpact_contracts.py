#!/usr/bin/env python3
"""Static contracts for the legacy WorkoutPact iOS project."""

from pathlib import Path
import plistlib
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
APP_PLIST = ROOT / "workoutpact" / "Info.plist"
PROJECT = ROOT / "workoutpact.xcodeproj" / "project.pbxproj"
APP_DELEGATE = ROOT / "workoutpact" / "AppDelegate.swift"
PAYMENT_CONTROLLER = ROOT / "workoutpact" / "PaymentViewController.swift"
TWO_FACTOR_CONTROLLER = ROOT / "workoutpact" / "TwoFactorViewController.swift"
SHAKE_CONTROLLER = ROOT / "workoutpact" / "ShakeViewContorller.swift"
LOGIN_CONTROLLER = ROOT / "workoutpact" / "LoginViewController.swift"


def fail(message):
    print(f"contract failure: {message}", file=sys.stderr)
    return 1


def read_text(path):
    return path.read_text(encoding="utf-8")


def plist_url_schemes(plist):
    schemes = []
    for entry in plist.get("CFBundleURLTypes", []):
        schemes.extend(entry.get("CFBundleURLSchemes", []))
    return schemes


def main():
    failures = []
    plist_text = read_text(APP_PLIST) if APP_PLIST.exists() else ""

    if not APP_PLIST.exists():
        failures.append(f"{APP_PLIST.relative_to(ROOT)} is missing")
    else:
        with APP_PLIST.open("rb") as plist_file:
            plist = plistlib.load(plist_file)

        required_plist_keys = [
            "CFBundleDisplayName",
            "CFBundleExecutable",
            "CFBundleIdentifier",
            "CFBundleName",
            "CFBundleShortVersionString",
            "CFBundleVersion",
            "LSRequiresIPhoneOS",
            "UIMainStoryboardFile",
        ]
        missing_keys = [key for key in required_plist_keys if not plist.get(key)]
        if missing_keys:
            failures.append("Info.plist missing required keys: " + ", ".join(missing_keys))

        if not plist.get("NSContactsUsageDescription"):
            failures.append("Info.plist must declare NSContactsUsageDescription for bundled Digits contact flows")

        schemes = plist_url_schemes(plist)
        invalid_schemes = [
            scheme for scheme in schemes if not re.match(r"^[A-Za-z][A-Za-z0-9+.-]*$", scheme)
        ]
        if invalid_schemes:
            failures.append("Info.plist has invalid URL schemes: " + ", ".join(invalid_schemes))
        if "workoutpact" not in schemes:
            failures.append("Info.plist must declare the workoutpact URL scheme")
        if not any(scheme.startswith("twitterkit-") for scheme in schemes):
            failures.append("Info.plist must declare a twitterkit-* callback URL scheme")

    project_text = read_text(PROJECT)
    if "INFOPLIST_FILE = workoutpact/Info.plist;" not in project_text:
        failures.append("project file must point the app target at workoutpact/Info.plist")
    if re.search(r"/Users/|[A-Za-z]:\\\\", project_text):
        failures.append("project file must not contain machine-local absolute paths")
    if 'SWIFT_OBJC_BRIDGING_HEADER = workoutpact/BridgeHeader.h;' not in project_text:
        failures.append("Swift bridging header must use the repo-relative path")
    if "SWIFT_OBJC_BRIDGING_HEADER[arch=*]" in project_text:
        failures.append("Swift bridging header must not use architecture-specific absolute overrides")

    app_delegate = read_text(APP_DELEGATE)
    payment_controller = read_text(PAYMENT_CONTROLLER)
    if "STPAPIClient" in payment_controller:
        match = re.search(r'StripePublishableKey\s*=\s*"([^"]*)"', app_delegate)
        if not match:
            failures.append("AppDelegate must define the Stripe publishable key boundary")
        elif match.group(1):
            failures.append("Stripe publishable key must stay empty in source; configure it locally")
        if "createTokenWithCard" not in payment_controller:
            failures.append("payment flow must tokenize cards instead of handling raw card data directly")
        if "handleToken(token" not in payment_controller:
            failures.append("payment flow must route Stripe tokens through handleToken before any backend work")

    social_sources = "\n".join(
        read_text(path)
        for path in (APP_DELEGATE, LOGIN_CONTROLLER, TWO_FACTOR_CONTROLLER, SHAKE_CONTROLLER)
    )
    if "Fabric.with([Digits(), Twitter()])" not in social_sources:
        failures.append("Fabric startup must include the legacy Digits and Twitter kits")
    if "TWTRComposer" in social_sources and "showWithCompletion" not in social_sources:
        failures.append("Twitter sharing must use the composer confirmation flow")
    if "authenticateWithDigitsAppearance" in social_sources and "NSContactsUsageDescription" not in plist_text:
        failures.append("Digits authentication requires contact privacy copy in Info.plist")

    if failures:
        for failure in failures:
            fail(failure)
        return 1

    print("WorkoutPact static contracts passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
