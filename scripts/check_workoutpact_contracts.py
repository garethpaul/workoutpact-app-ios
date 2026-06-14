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
    DOCS_PLANS / "2026-06-09-workoutpact-shake-motion-subtype-guard.md",
    DOCS_PLANS / "2026-06-10-workoutpact-hosted-static-verification.md",
    DOCS_PLANS / "2026-06-10-workoutpact-no-backend-billing-notice.md",
    DOCS_PLANS / "2026-06-10-workoutpact-keyboard-lifecycle-reset.md",
    DOCS_PLANS / "2026-06-10-workoutpact-legacy-sdk-modernization-boundary.md",
    DOCS_PLANS / "2026-06-13-workoutpact-stale-payment-callback.md",
    DOCS_PLANS / "2026-06-13-workoutpact-stale-digits-callback.md",
    DOCS_PLANS / "2026-06-13-workoutpact-callback-generation-guards.md",
    DOCS_PLANS / "2026-06-14-workoutpact-make-root-override-protection.md",
    DOCS_PLANS / "2026-06-14-workoutpact-stale-payment-ui-state.md",
]
WORKFLOW = ROOT / ".github/workflows/check.yml"
MAKEFILE = ROOT / "Makefile"


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
    podfile_lock = read_text("Podfile.lock")
    readme = read_text("README.md")
    security = read_text("SECURITY.md")
    vision = read_text("VISION.md")
    changes = read_text("CHANGES.md")
    workflow = read_text(".github/workflows/check.yml") if WORKFLOW.is_file() else ""
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
    authentication_request = two_factor.split("func twoFactor()", 1)[1].split(
        "override func didReceiveMemoryWarning", 1
    )[0]
    authentication_appearance = two_factor.split(
        "override func viewWillAppear", 1
    )[1].split("override func viewWillDisappear", 1)[0]
    authentication_disappearance = two_factor.split(
        "override func viewWillDisappear", 1
    )[1].split("func twoFactor()", 1)[0]
    authentication_request_guard = "if !authenticationContextActive"
    authentication_completion_guard = "!self.authenticationContextActive"
    authentication_call = "digits.authenticateWithDigitsAppearance"
    protected_segue = 'self.performSegueWithIdentifier("protected", sender: self)'
    require(
        "var authenticationContextActive = false" in two_factor
        and "authenticationContextActive = true" in authentication_appearance
        and "self.isBeingDismissed()" in authentication_disappearance
        and "self.isMovingFromParentViewController()" in authentication_disappearance
        and "authenticationContextActive = false" in authentication_disappearance
        and authentication_disappearance.index("self.isBeingDismissed()")
        < authentication_disappearance.index("authenticationContextActive = false"),
        "two-factor screen lifecycle must track whether callbacks may reveal protected content",
        failures,
    )
    require(
        authentication_request_guard in authentication_request
        and authentication_request.index(authentication_request_guard)
        < authentication_request.index(authentication_call),
        "inactive two-factor screens must be rejected before Digits authentication",
        failures,
    )
    require(
        authentication_completion_guard in authentication_request
        and authentication_request.index("error != nil || session == nil")
        < authentication_request.index("dispatch_async(dispatch_get_main_queue()")
        < authentication_request.index(authentication_completion_guard)
        < authentication_request.index(protected_segue),
        "stale Digits success callbacks must be rejected on the main queue before the protected segue",
        failures,
    )
    require(
        "var authenticationGeneration = 0" in two_factor
        and "authenticationGeneration += 1" in authentication_disappearance
        and authentication_disappearance.index("authenticationGeneration += 1")
        < authentication_disappearance.index("authenticationContextActive = false"),
        "two-factor dismissal must invalidate the prior authentication generation",
        failures,
    )
    require(
        "let authenticationRequestGeneration = authenticationGeneration" in authentication_request
        and authentication_request.index("let authenticationRequestGeneration = authenticationGeneration")
        < authentication_request.index(authentication_call)
        and "authenticationRequestGeneration != self.authenticationGeneration" in authentication_request
        and authentication_request.index("authenticationRequestGeneration != self.authenticationGeneration")
        < authentication_request.index(protected_segue),
        "Digits completion must reject requests from a prior controller generation",
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
    payment_request = payment.split("func createToken()", 1)[1].split(
        "func handleToken", 1
    )[0]
    appearance_method = payment.split("override func viewWillAppear", 1)[1].split(
        "override func viewWillDisappear", 1
    )[0]
    disappearance_method = payment.split("override func viewWillDisappear", 1)[1].split(
        "func paymentView", 1
    )[0]
    lifecycle_guard = "if !paymentViewVisible"
    completion_guard = "!self.paymentViewVisible"
    require(
        "paymentViewVisible = true" in appearance_method
        and "paymentViewVisible = false" in disappearance_method,
        "payment screen lifecycle must track whether callbacks may present UI",
        failures,
    )
    require(
        lifecycle_guard in payment_request
        and payment_request.index(lifecycle_guard)
        < payment_request.index("STPAPIClient.sharedClient().createTokenWithCard"),
        "inactive payment screens must be rejected before Stripe tokenization",
        failures,
    )
    require(
        "paymentRequestGeneration != self.paymentGeneration" in payment_request
        and completion_guard in payment_request
        and payment_request.index("dispatch_async(dispatch_get_main_queue()")
        < payment_request.index("paymentRequestGeneration != self.paymentGeneration")
        < payment_request.index("if let button = self.payButton")
        < payment_request.index("error != nil || token == nil")
        < payment_request.index("self.handleToken(token)"),
        "stale Stripe completions must be rejected before button, error, or billing UI handling",
        failures,
    )
    require(
        "var paymentGeneration = 0" in payment
        and "paymentGeneration += 1" in disappearance_method
        and disappearance_method.index("paymentGeneration += 1")
        < disappearance_method.index("paymentViewVisible = false"),
        "payment disappearance must invalidate the prior tokenization generation",
        failures,
    )
    require(
        "let paymentRequestGeneration = paymentGeneration" in payment_request
        and payment_request.index("let paymentRequestGeneration = paymentGeneration")
        < payment_request.index("STPAPIClient.sharedClient().createTokenWithCard")
        and "paymentRequestGeneration != self.paymentGeneration" in payment_request
        and payment_request.index("paymentRequestGeneration != self.paymentGeneration")
        < payment_request.index("self.handleToken(token)"),
        "Stripe completion must reject requests from a prior payment generation",
        failures,
    )
    require(
        "create charge" not in payment.lower(),
        "payment comments must not imply the prototype creates charges",
        failures,
    )
    token_handler = payment.split("func handleToken", 1)[1]
    require(
        'title: "Billing unavailable"' in token_handler,
        "successful tokenization must disclose that billing is unavailable",
        failures,
    )
    require(
        'message: "Your card was tokenized, but no donation or charge was created."'
        in token_handler,
        "successful tokenization must not imply a donation or charge was created",
        failures,
    )
    require(
        'title: "Continue without billing"' in token_handler,
        "payment continuation must explicitly state that billing is disabled",
        failures,
    )
    require(
        'self.presentViewController(alert, animated: true, completion: nil)' in token_handler
        and 'self.performSegueWithIdentifier("shake", sender: self)' in token_handler
        and token_handler.index('title: "Continue without billing"')
        < token_handler.index('self.performSegueWithIdentifier("shake", sender: self)')
        < token_handler.index('self.presentViewController(alert, animated: true, completion: nil)'),
        "payment segue must be scoped to the explicit no-billing continuation action",
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
        "if motion != UIEventSubtype.MotionShake" in shake
        and "event.subtype" not in shake
        and shake.index("if motion != UIEventSubtype.MotionShake") < shake.index("let alert = UIAlertController"),
        "shake sharing must use the delivered motion subtype before presenting confirmation",
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
    has_restore_method = "func restoreKeyboardShiftIfNeeded()" in workout
    require(
        has_restore_method,
        "protected screen must centralize keyboard-shift restoration",
        failures,
    )
    restore_method = ""
    if has_restore_method:
        restore_method = workout.split("func restoreKeyboardShiftIfNeeded()", 1)[1].split(
            "func textFieldShouldReturn", 1
        )[0]
    require(
        "if !keyboardIsVisible {\n            return\n        }" in restore_method,
        "keyboard restoration must be idempotent when the view is not shifted",
        failures,
    )
    require(
        "keyboardIsVisible = false" in restore_method
        and "self.view.frame = CGRectOffset(self.view.frame, 0, kbHeight)" in restore_method
        and "kbHeight = 0" in restore_method,
        "keyboard restoration must reset state, frame offset, and cached height",
        failures,
    )
    disappearance_method = workout.split("override func viewWillDisappear", 1)[1].split(
        "func restoreKeyboardShiftIfNeeded()", 1
    )[0]
    restores_keyboard_shift = "restoreKeyboardShiftIfNeeded()" in disappearance_method
    require(
        restores_keyboard_shift,
        "view disappearance must restore any active keyboard shift",
        failures,
    )
    require(
        restores_keyboard_shift
        and "removeObserver(self)" in disappearance_method
        and disappearance_method.index("restoreKeyboardShiftIfNeeded()")
        < disappearance_method.index("removeObserver(self)"),
        "keyboard shift must be restored before keyboard observers are removed",
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
    require(
        project.count("IPHONEOS_DEPLOYMENT_TARGET = 8.3;") >= 2,
        "project must retain the documented iOS 8.3 archival deployment target",
        failures,
    )
    require(
        "PaymentKit (1.1.1)" in podfile_lock and "Stripe (4.0.3)" in podfile_lock,
        "Podfile.lock must match the documented PaymentKit 1.1.1 and Stripe 4.0.3 boundary",
        failures,
    )
    retired_frameworks = [
        "Fabric.framework",
        "DigitsKit.framework",
        "TwitterCore.framework",
        "TwitterKit.framework",
    ]
    missing_frameworks = [name for name in retired_frameworks if not (ROOT / name).is_dir()]
    require(
        not missing_frameworks,
        "documented retired frameworks are missing: " + ", ".join(missing_frameworks),
        failures,
    )
    boundary_terms = [
        "iOS 8.3",
        "Stripe 4.0.3",
        "PaymentKit 1.1.1",
        "Fabric",
        "DigitsKit",
        "TwitterCore",
        "TwitterKit",
    ]
    for document_name, document in [
        ("README.md", readme),
        ("SECURITY.md", security),
        ("VISION.md", vision),
        ("CHANGES.md", changes),
    ]:
        missing_terms = [term for term in boundary_terms if term not in document]
        require(
            not missing_terms,
            f"{document_name} must document the legacy SDK boundary: "
            + ", ".join(missing_terms),
            failures,
        )
    require(WORKFLOW.is_file(), "hosted verification workflow must exist", failures)
    require(
        "permissions:\n  contents: read" in workflow,
        "hosted verification permissions must be read-only",
        failures,
    )
    require(
        "python-version: ['3.10', '3.12', '3.14']" in workflow,
        "hosted verification must cover Python 3.10, 3.12, and 3.14",
        failures,
    )
    require(
        "workflow_dispatch:" in workflow,
        "hosted verification must support manual dispatch",
        failures,
    )
    require(
        "actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10" in workflow,
        "checkout must use an immutable revision",
        failures,
    )
    require(
        "actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405" in workflow,
        "setup-python must use an immutable revision",
        failures,
    )
    require("timeout-minutes: 5" in workflow, "hosted verification must have a timeout", failures)
    require("run: make check" in workflow, "hosted verification must run make check", failures)
    require("concurrency:" in workflow, "hosted verification must define concurrency", failures)
    require(
        "cancel-in-progress: true" in workflow,
        "hosted verification must cancel superseded runs",
        failures,
    )
    require(
        "runs-on: ubuntu-24.04" in workflow,
        "hosted verification must use a fixed Ubuntu runner",
        failures,
    )
    require("ubuntu-latest" not in workflow, "hosted verification must not use a floating runner", failures)
    makefile = MAKEFILE.read_text(encoding="utf-8")
    makefile_lines = set(makefile.splitlines())
    require(
        "override ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))" in makefile_lines,
        "Makefile must protect the repository root",
        failures,
    )
    require("PYTHON ?= python3" in makefile_lines, "Makefile must preserve the Python command override", failures)
    require(
        "CHECK_SCRIPT := $(ROOT)/scripts/check_workoutpact_contracts.py" in makefile,
        "Makefile must use the rooted checker path",
        failures,
    )
    require(
        "WORKSPACE := $(ROOT)/workoutpact.xcworkspace" in makefile,
        "Makefile must resolve the Xcode workspace from the repository root",
        failures,
    )
    require(
        '-workspace "$(WORKSPACE)"' in makefile,
        "Xcode build must use the rooted workspace path",
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
