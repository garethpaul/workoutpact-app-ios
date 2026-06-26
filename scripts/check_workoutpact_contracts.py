#!/usr/bin/env python3
"""Static contracts for the legacy WorkoutPact iOS project."""

from pathlib import Path
import json
import plistlib
import re
import subprocess
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
    DOCS_PLANS / "2026-06-15-workoutpact-stale-twitter-login-callback.md",
    DOCS_PLANS / "2026-06-16-workoutpact-weak-twitter-login-callback.md",
    DOCS_PLANS / "2026-06-16-workoutpact-twitter-transition-guard.md",
    DOCS_PLANS / "2026-06-16-workoutpact-shake-presentation-guard.md",
    DOCS_PLANS / "2026-06-19-workoutpact-async-flow-safety-review.md",
    DOCS_PLANS / "2026-06-21-workoutpact-checkout-credential-isolation.md",
    DOCS_PLANS / "2026-06-21-workoutpact-make-authority-isolation.md",
    DOCS_PLANS / "2026-06-25-workoutpact-logout-transition.md",
    DOCS_PLANS / "2026-06-25-workoutpact-legacy-setup-status.md",
    DOCS_PLANS / "2026-06-26-workoutpact-payment-validity-state.md",
]
WORKFLOW = ROOT / ".github/workflows/check.yml"
MAKEFILE = ROOT / "Makefile"
MAKE_AUTHORITY_SCRIPT = ROOT / "scripts/test-makefile-root.sh"
CHECKOUT_CREDENTIAL_ISOLATION_BLOCK = """      - name: Check out repository
        uses: actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10 # v6.0.3
        with:
          persist-credentials: false"""
CHECKOUT_ACTION = "actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10"
SETUP_PYTHON_ACTION = "actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405"
WORKFLOW_YAML_PARSER = r"""
require "json"
require "psych"

def node_location(node)
  if node.respond_to?(:start_line) && node.start_line
    "line #{node.start_line + 1}, column #{node.start_column + 1}"
  else
    "unknown location"
  end
end

def remember_anchor(node, value, anchors)
  if node.respond_to?(:anchor) && node.anchor && !node.anchor.empty?
    anchors[node.anchor] = value
  end
end

def duplicate_safe_key(node, errors)
  unless node.is_a?(Psych::Nodes::Scalar)
    errors << "workflow mapping key at #{node_location(node)} is not a scalar"
    return nil
  end
  node.value
end

def deep_copy(value)
  Marshal.load(Marshal.dump(value))
end

def convert_node(node, anchors, errors)
  case node
  when Psych::Nodes::Document
    return convert_node(node.root, anchors, errors)
  when Psych::Nodes::Mapping
    result = {}
    remember_anchor(node, result, anchors)
    seen = {}
    node.children.each_slice(2) do |key_node, value_node|
      key = duplicate_safe_key(key_node, errors)
      next if key.nil?

      normalized_key = key.downcase
      if seen.key?(normalized_key)
        errors << "duplicate YAML key #{key.inspect} at #{node_location(key_node)}; first seen at #{seen[normalized_key]}"
      else
        seen[normalized_key] = node_location(key_node)
      end

      if key == "<<"
        errors << "YAML merge key is not supported at #{node_location(key_node)}"
      end

      result[key] = convert_node(value_node, anchors, errors)
    end
    result
  when Psych::Nodes::Sequence
    result = []
    remember_anchor(node, result, anchors)
    node.children.each do |child|
      result << convert_node(child, anchors, errors)
    end
    result
  when Psych::Nodes::Scalar
    remember_anchor(node, node.value, anchors)
    node.value
  when Psych::Nodes::Alias
    if anchors.key?(node.anchor)
      deep_copy(anchors[node.anchor])
    else
      errors << "unknown YAML alias #{node.anchor.inspect} at #{node_location(node)}"
      nil
    end
  else
    errors << "unsupported YAML node #{node.class} at #{node_location(node)}"
    nil
  end
end

errors = []
begin
  document = Psych.parse(STDIN.read)
  data = convert_node(document, {}, errors)
rescue Psych::Exception => error
  data = nil
  errors << "workflow YAML parse failed: #{error.message}"
end

puts JSON.generate({"data" => data, "errors" => errors})
"""


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


def parse_workflow_yaml(workflow):
    try:
        parsed = subprocess.run(
            ["ruby", "-e", WORKFLOW_YAML_PARSER],
            input=workflow,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return None, [], [f"workflow YAML parser unavailable: {exc}"]

    if parsed.returncode != 0:
        detail = parsed.stderr.strip() or parsed.stdout.strip()
        return None, [], [f"workflow YAML parser failed: {detail}"]

    try:
        payload = json.loads(parsed.stdout)
    except json.JSONDecodeError as exc:
        return None, [], [f"workflow YAML parser returned invalid JSON: {exc}"]

    return payload.get("data"), payload.get("errors", []), []


def has_exact_keys(value, expected):
    return isinstance(value, dict) and set(value.keys()) == set(expected)


def normalized_mapping(value):
    if not isinstance(value, dict):
        return None
    return {key.lower(): item for key, item in value.items()}


def scalar_equals(value, expected, case_sensitive=True):
    if not isinstance(value, str):
        return False
    if case_sensitive:
        return value == expected
    return value.lower() == expected.lower()


def trigger_map_is_reviewed(value):
    if not has_exact_keys(value, {"push", "pull_request", "workflow_dispatch"}):
        return False
    return all(value[trigger] == "" for trigger in value)


def checkout_step_is_reviewed(step):
    if not has_exact_keys(step, {"name", "uses", "with"}):
        return False
    inputs = normalized_mapping(step["with"])
    return (
        scalar_equals(step["name"], "Check out repository")
        and scalar_equals(step["uses"], CHECKOUT_ACTION)
        and inputs is not None
        and set(inputs.keys()) == {"persist-credentials"}
        and scalar_equals(inputs["persist-credentials"], "false", case_sensitive=False)
    )


def setup_python_step_is_reviewed(step):
    if not has_exact_keys(step, {"name", "uses", "with"}):
        return False
    inputs = normalized_mapping(step["with"])
    return (
        scalar_equals(step["name"], "Set up Python")
        and scalar_equals(step["uses"], SETUP_PYTHON_ACTION)
        and inputs is not None
        and set(inputs.keys()) == {"python-version"}
        and scalar_equals(inputs["python-version"], "${{ matrix.python-version }}")
    )


def run_step_is_reviewed(step):
    return (
        has_exact_keys(step, {"name", "run"})
        and scalar_equals(step["name"], "Run portable verification")
        and scalar_equals(step["run"], "/usr/bin/make check")
    )


def static_contract_job_is_reviewed(job):
    if not has_exact_keys(job, {"runs-on", "timeout-minutes", "strategy", "steps"}):
        return False

    strategy = job["strategy"]
    if not has_exact_keys(strategy, {"fail-fast", "matrix"}):
        return False
    matrix = strategy["matrix"]
    if not has_exact_keys(matrix, {"python-version"}):
        return False

    steps = job["steps"]
    return (
        scalar_equals(job["runs-on"], "ubuntu-24.04")
        and scalar_equals(job["timeout-minutes"], "5")
        and scalar_equals(strategy["fail-fast"], "false", case_sensitive=False)
        and matrix["python-version"] == ["3.10", "3.12", "3.14"]
        and isinstance(steps, list)
        and len(steps) == 3
        and checkout_step_is_reviewed(steps[0])
        and setup_python_step_is_reviewed(steps[1])
        and run_step_is_reviewed(steps[2])
    )


def hosted_workflow_is_reviewed(workflow):
    document, document_errors, parser_errors = parse_workflow_yaml(workflow)
    if parser_errors:
        return False, parser_errors
    if document_errors or not has_exact_keys(
        document, {"name", "on", "permissions", "concurrency", "jobs"}
    ):
        return False, []

    permissions = document["permissions"]
    concurrency = document["concurrency"]
    jobs = document["jobs"]
    return (
        scalar_equals(document["name"], "Check")
        and trigger_map_is_reviewed(document["on"])
        and has_exact_keys(permissions, {"contents"})
        and scalar_equals(permissions["contents"], "read")
        and has_exact_keys(concurrency, {"group", "cancel-in-progress"})
        and scalar_equals(concurrency["group"], "check-${{ github.workflow }}-${{ github.ref }}")
        and scalar_equals(concurrency["cancel-in-progress"], "true", case_sensitive=False)
        and has_exact_keys(jobs, {"static-contracts"})
        and static_contract_job_is_reviewed(jobs["static-contracts"])
    ), []


def checkout_credentials_are_isolated(workflow):
    return hosted_workflow_is_reviewed(workflow)


def workflow_mutations_are_rejected(mutations):
    for mutated in mutations:
        reviewed, parser_errors = checkout_credentials_are_isolated(mutated)
        if parser_errors:
            return False, parser_errors
        if reviewed:
            return False, []
    return True, []


def validate_login_lifecycle(login, failures):
    login_appearance = login.split("override func viewWillAppear", 1)[1].split(
        "override func viewWillDisappear", 1
    )[0]
    login_disappearance = login.split("override func viewWillDisappear", 1)[1].split(
        "override func viewDidLoad", 1
    )[0]
    login_completion = login.split("let logInButton = TWTRLogInButton", 1)[1].split(
        "logInButton.center", 1
    )[0]
    login_lifecycle_guard = "if !controller.loginContextActive"
    login_storyboard_lookup = "if let storyboard = controller.storyboard"
    require(
        "var loginContextActive = false" in login
        and "loginContextActive = true" in login_appearance
        and "self.isBeingDismissed()" in login_disappearance
        and "self.isMovingFromParentViewController()" in login_disappearance
        and "self.navigationController?.isBeingDismissed() == true" in login_disappearance
        and "loginContextActive = false" in login_disappearance,
        "login screen lifecycle must track whether Twitter callbacks may present phone verification",
        failures,
    )
    require(
        "error != nil || session == nil" in login_completion
        and login_lifecycle_guard in login_completion
        and login_completion.index("error != nil || session == nil")
        < login_completion.index("dispatch_async(dispatch_get_main_queue()")
        < login_completion.index(login_lifecycle_guard)
        < login_completion.index(login_storyboard_lookup)
        < login_completion.index("controller.presentViewController"),
        "stale Twitter success callbacks must be rejected on the main queue before presentation",
        failures,
    )


def validate_login_callback_ownership(login, failures):
    login_completion = login.split("let logInButton = TWTRLogInButton", 1)[1].split(
        "logInButton.center", 1
    )[0]
    outer_capture = "TWTRLogInButton(logInCompletion: { [weak self]"
    dispatch_capture = "dispatch_async(dispatch_get_main_queue(), { [weak self] in"
    promotion = "if let controller = self"
    lifecycle_guard = "if !controller.loginContextActive"
    storyboard_lookup = "if let storyboard = controller.storyboard"
    presentation = "controller.presentViewController"
    require(
        outer_capture in login
        and dispatch_capture in login_completion
        and promotion in login_completion,
        "Twitter login callbacks must capture the controller weakly and promote it only on the main queue",
        failures,
    )
    require(
        dispatch_capture in login_completion
        and promotion in login_completion
        and lifecycle_guard in login_completion
        and storyboard_lookup in login_completion
        and presentation in login_completion
        and login_completion.index(dispatch_capture)
        < login_completion.index(promotion)
        < login_completion.index(lifecycle_guard)
        < login_completion.index(storyboard_lookup)
        < login_completion.index(presentation),
        "weak Twitter login ownership must preserve lifecycle and presentation ordering",
        failures,
    )
    require(
        "self.loginContextActive" not in login_completion
        and "self.storyboard" not in login_completion
        and "self.presentViewController" not in login_completion,
        "Twitter login completion must use only the promoted controller for UI state",
        failures,
    )


def validate_login_transition(login, failures):
    login_appearance = login.split("override func viewWillAppear", 1)[1].split(
        "override func viewWillDisappear", 1
    )[0]
    login_completion = login.split("let logInButton = TWTRLogInButton", 1)[1].split(
        "logInButton.center", 1
    )[0]
    lifecycle_guard = "if !controller.loginContextActive"
    transition_guard = "if controller.loginTransitionInFlight"
    presentation_guard = "if controller.presentedViewController != nil"
    transition_claim = "controller.loginTransitionInFlight = true"
    storyboard_lookup = "if let storyboard = controller.storyboard"
    destination_lookup = 'instantiateViewControllerWithIdentifier("TwoFactorViewController")'
    require(
        "var loginTransitionInFlight = false" in login
        and "loginTransitionInFlight = false" not in login_appearance,
        "Twitter login transition ownership must remain consumed across resumed appearances",
        failures,
    )
    require(
        lifecycle_guard in login_completion
        and transition_guard in login_completion
        and presentation_guard in login_completion
        and transition_claim in login_completion
        and storyboard_lookup in login_completion
        and destination_lookup in login_completion
        and login_completion.index(lifecycle_guard)
        < login_completion.index(transition_guard)
        < login_completion.index(presentation_guard)
        < login_completion.index(storyboard_lookup)
        < login_completion.index(destination_lookup)
        < login_completion.index(transition_claim)
        < login_completion.index("controller.presentViewController"),
        "Twitter login success must validate its destination before claiming exactly one presentation",
        failures,
    )


def validate_shake_presentation(shake, failures):
    handler = shake.split("override func motionEnded", 1)[1].split(
        "func presentTweetComposer", 1
    )[0]
    motion_guard = "if motion != UIEventSubtype.MotionShake"
    presentation_guard = "if shareFlowInFlight || self.presentedViewController != nil"
    presentation_claim = "shareFlowInFlight = true"
    alert_construction = "let alert = UIAlertController"
    alert_presentation = "self.presentViewController(alert"
    require(
        motion_guard in handler
        and presentation_guard in handler
        and presentation_claim in handler
        and alert_construction in handler
        and alert_presentation in handler
        and handler.index(motion_guard)
        < handler.index(presentation_guard)
        < handler.index(presentation_claim)
        < handler.index(alert_construction)
        < handler.index(alert_presentation),
        "shake confirmation must reserve one share flow before constructing its alert",
        failures,
    )


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
        'hasPrefix("pk_test_")' in app_delegate
        and 'pk_live_' not in app_delegate
        and "rangeOfCharacterFromSet(NSCharacterSet.whitespaceAndNewlineCharacterSet()) == nil"
        in app_delegate,
        "Stripe publishable key loader must enforce test mode and reject embedded whitespace",
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
        "if let storyboard = controller.storyboard" in login,
        "Twitter login must guard storyboard lookup before presenting phone verification",
        failures,
    )
    documentation = {
        "README.md": "Queued presentation callbacks capture the controller weakly",
        "SECURITY.md": "Twitter login callbacks use weak controller ownership",
        "VISION.md": "Keep Twitter login callbacks weakly owned",
        "CHANGES.md": "Broke the Twitter login button retain cycle",
    }
    for document_name, phrase in documentation.items():
        require(
            phrase in read_text(document_name),
            f"{document_name} must document weak Twitter login callback ownership",
            failures,
        )
    for document_name in ("README.md", "SECURITY.md", "VISION.md", "CHANGES.md"):
        require(
            "single twitter login transition" in read_text(document_name).lower(),
            f"{document_name} must document the single Twitter login transition guard",
            failures,
        )
    require(
        "as! TwoFactorViewController" not in login
        and "as? TwoFactorViewController" in login,
        "Twitter login must safely cast the phone verification controller",
        failures,
    )
    validate_login_lifecycle(login, failures)
    validate_login_callback_ownership(login, failures)
    validate_login_transition(login, failures)
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
    authentication_completion_guard = "!controller.authenticationContextActive"
    authentication_call = "digits.authenticateWithDigitsAppearance"
    protected_segue = 'controller.performSegueWithIdentifier("protected", sender: controller)'
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
        and authentication_request.index("dispatch_async(dispatch_get_main_queue()")
        < authentication_request.index(authentication_completion_guard)
        < authentication_request.index("error != nil || session == nil")
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
        and "authenticationRequestGeneration != controller.authenticationGeneration" in authentication_request
        and authentication_request.index("authenticationRequestGeneration != controller.authenticationGeneration")
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
        and "var paymentInputValid = false" in payment
        and "paymentInputValid = valid" in payment
        and "button.enabled = paymentSubmissionEnabled()" in payment
        and "if let button = controller.payButton" in payment,
        "payment submit button state must be guarded by validation, configuration, and token callback behavior",
        failures,
    )
    require(
        "func paymentSubmissionEnabled() -> Bool" in payment
        and "paymentInputValid && !paymentFlowInFlight && configuredStripePublishableKey() != nil" in payment,
        "payment Submit availability must remain disabled without a configured Stripe test key",
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
    lifecycle_guard = "if !paymentViewVisible || paymentFlowInFlight || !paymentInputValid"
    completion_guard = "!controller.paymentViewVisible"
    require(
        "button.enabled = controller.paymentSubmissionEnabled()" in payment_request,
        "Stripe failure handling must restore submit from current validity and key availability",
        failures,
    )
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
        "paymentRequestGeneration != controller.paymentGeneration" in payment_request
        and completion_guard in payment_request
        and "!controller.paymentFlowInFlight" in payment_request
        and payment_request.index("dispatch_async(dispatch_get_main_queue()")
        < payment_request.index("paymentRequestGeneration != controller.paymentGeneration")
        < payment_request.index("error != nil || token == nil")
        < payment_request.index("controller.handleToken(token)"),
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
        and "paymentRequestGeneration != controller.paymentGeneration" in payment_request
        and payment_request.index("paymentRequestGeneration != controller.paymentGeneration")
        < payment_request.index("controller.handleToken(token)"),
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
        and 'controller.performSegueWithIdentifier("shake", sender: controller)' in token_handler
        and token_handler.index('title: "Continue without billing"')
        < token_handler.index('controller.performSegueWithIdentifier("shake", sender: controller)')
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
    validate_shake_presentation(shake, failures)
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
        "if let storyboard = controller.storyboard" in workout and "self.storyboard!" not in workout,
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
        "var logoutTransitionInFlight = false" in workout
        and "if logoutTransitionInFlight || self.presentedViewController != nil" in workout,
        "logout navigation must reserve one non-overlapping transition",
        failures,
    )
    require(
        workout.index("logoutTransitionInFlight = true")
        < workout.index("Digits.sharedInstance().logOut()")
        and "dispatch_async(dispatch_get_main_queue(), { [weak self] in" in workout,
        "logout navigation must claim before clearing sessions and weakly queue presentation",
        failures,
    )
    require(
        "if !controller.logoutTransitionInFlight || controller.presentedViewController != nil" in workout
        and "controller.logoutTransitionInFlight = false" in workout,
        "queued logout navigation must revalidate and release failed ownership",
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
    normalized_readme = " ".join(readme.split())
    for phrase in (
        "## Project Status",
        "not production-ready",
        "`workoutpact.xcworkspace`",
        "Do not open `workoutpact.xcodeproj` after installing Pods",
    ):
        require(
            phrase in normalized_readme,
            f"README.md must preserve the legacy setup/status guidance: {phrase}",
            failures,
        )
    require(WORKFLOW.is_file(), "hosted verification workflow must exist", failures)
    require(
        "permissions:\n  contents: read" in workflow,
        "hosted verification permissions must be read-only",
        failures,
    )
    workflow_reviewed, workflow_parser_errors = checkout_credentials_are_isolated(workflow)
    failures.extend(workflow_parser_errors)
    workflow_checks_available = not workflow_parser_errors
    if workflow_checks_available:
        require(
            workflow_reviewed,
            "checkout must disable persisted credentials on the immutable checkout step",
            failures,
        )
    checkout_mutations = {
        "writable credentials": workflow.replace(
            CHECKOUT_CREDENTIAL_ISOLATION_BLOCK,
            CHECKOUT_CREDENTIAL_ISOLATION_BLOCK.replace("false", "true"),
            1,
        ),
        "missing setting": workflow.replace(
            CHECKOUT_CREDENTIAL_ISOLATION_BLOCK,
            CHECKOUT_CREDENTIAL_ISOLATION_BLOCK.replace(
                "        with:\n          persist-credentials: false", ""
            ),
            1,
        ),
        "decoy setting": workflow.replace(
            CHECKOUT_CREDENTIAL_ISOLATION_BLOCK,
            CHECKOUT_CREDENTIAL_ISOLATION_BLOCK.replace(
                "          persist-credentials: false", ""
            )
            + "\n      - run: echo 'persist-credentials: false'",
            1,
        ),
        "additional checkout": workflow.replace(
            CHECKOUT_CREDENTIAL_ISOLATION_BLOCK,
            CHECKOUT_CREDENTIAL_ISOLATION_BLOCK
            + "\n      - name: Unsafe second checkout"
            + "\n        uses: actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10",
            1,
        ),
        "duplicate setting": workflow.replace(
            CHECKOUT_CREDENTIAL_ISOLATION_BLOCK,
            CHECKOUT_CREDENTIAL_ISOLATION_BLOCK
            + "\n          persist-credentials: true",
            1,
        ),
        "mixed-case duplicate setting": workflow.replace(
            CHECKOUT_CREDENTIAL_ISOLATION_BLOCK,
            CHECKOUT_CREDENTIAL_ISOLATION_BLOCK
            + "\n          PERSIST-CREDENTIALS: true",
            1,
        ),
        "mixed-case duplicate with block": workflow.replace(
            CHECKOUT_CREDENTIAL_ISOLATION_BLOCK,
            CHECKOUT_CREDENTIAL_ISOLATION_BLOCK
            + "\n        With:\n          persist-credentials: true",
            1,
        ),
    }
    if workflow_checks_available:
        checkout_mutations_rejected, mutation_parser_errors = (
            workflow_mutations_are_rejected(checkout_mutations.values())
        )
        failures.extend(mutation_parser_errors)
        workflow_checks_available = not mutation_parser_errors
        if workflow_checks_available:
            require(
                checkout_mutations_rejected,
                "checkout credential isolation mutations must be rejected",
                failures,
            )
    checkout_missing = workflow.replace(CHECKOUT_CREDENTIAL_ISOLATION_BLOCK + "\n", "")
    checkout_block_scalar_decoy = workflow.replace(CHECKOUT_CREDENTIAL_ISOLATION_BLOCK + "\n", "")
    checkout_block_scalar_decoy = (
        checkout_block_scalar_decoy.rstrip()
        + "\n\nenv:\n  CHECKOUT_DECOY: |\n"
        + CHECKOUT_CREDENTIAL_ISOLATION_BLOCK
        + "\n"
    )
    checkout_alias_additional = workflow.replace(
        "      - name: Check out repository\n",
        "      - &checkout_step\n        name: Check out repository\n",
        1,
    ).replace(
        "          persist-credentials: false\n",
        "          persist-credentials: false\n      - *checkout_step\n",
        1,
    )
    checkout_input_mixed_case = workflow.replace(
        "          persist-credentials: false",
        "          PERSIST-CREDENTIALS: FALSE",
        1,
    )
    hostile_workflow_mutations = {
        "missing checkout": checkout_missing,
        "writable checkout": workflow.replace(
            "          persist-credentials: false",
            "          persist-credentials: true",
            1,
        ),
        "decoy checkout setting": workflow.replace(
            "          persist-credentials: false\n",
            "",
            1,
        )
        + "      - run: echo 'persist-credentials: false'\n",
        "additional checkout": workflow.replace(
            CHECKOUT_CREDENTIAL_ISOLATION_BLOCK,
            CHECKOUT_CREDENTIAL_ISOLATION_BLOCK
            + "\n      - name: Unsafe second checkout"
            + "\n        uses: actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10",
            1,
        ),
        "anchor additional checkout": checkout_alias_additional,
        "block scalar checkout decoy": checkout_block_scalar_decoy,
        "duplicate checkout input": workflow.replace(
            "          persist-credentials: false",
            "          persist-credentials: false\n          persist-credentials: true",
            1,
        ),
        "mixed-case duplicate checkout input": workflow.replace(
            "          persist-credentials: false",
            "          persist-credentials: false\n          PERSIST-CREDENTIALS: true",
            1,
        ),
        "duplicate checkout step key": workflow.replace(
            "        uses: "
            "actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10 # v6.0.3",
            "        uses: actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10 # v6.0.3"
            + "\n        uses: actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10",
            1,
        ),
        "duplicate workflow key": (
            workflow.rstrip() + "\n\npermissions:\n  contents: write\n"
        ),
        "decoy run command": workflow.replace(
            "        run: /usr/bin/make check",
            "        run: echo skipped",
            1,
        )
        + "\nenv:\n  RUN_DECOY: |\n      - name: Run portable verification\n        run: /usr/bin/make check\n",
    }
    if workflow_checks_available:
        mixed_case_reviewed, mixed_case_parser_errors = (
            checkout_credentials_are_isolated(checkout_input_mixed_case)
        )
        failures.extend(mixed_case_parser_errors)
        workflow_checks_available = not mixed_case_parser_errors
        if workflow_checks_available:
            require(
                mixed_case_reviewed,
                "checkout credential input must be normalized case-insensitively",
                failures,
            )
    if workflow_checks_available:
        hostile_mutations_rejected, mutation_parser_errors = (
            workflow_mutations_are_rejected(hostile_workflow_mutations.values())
        )
        failures.extend(mutation_parser_errors)
        if not mutation_parser_errors:
            require(
                hostile_mutations_rejected,
                "hostile workflow mutations must be rejected",
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
    require(
        "run: /usr/bin/make check" in workflow,
        "hosted verification must run the trusted system Make authority",
        failures,
    )
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
    for contract in (
        ".DEFAULT_GOAL := check",
        ".SECONDEXPANSION:",
        "PYTHON ?= python3",
        "override PYTHON := $(value PYTHON)",
        "XCODEBUILD ?= /usr/bin/xcodebuild",
        "override XCODEBUILD := $(value XCODEBUILD)",
        "override SHELL := /bin/sh",
        "override .SHELLFLAGS := -c",
        "override MAKEFILES :=",
        "ifneq ($(origin MAKEFILE_LIST),file)",
        "export ROOT",
        "root-test::",
        "\t/bin/sh '$(REPOSITORY_ROOT_LITERAL)/scripts/test-makefile-root.sh'",
        "verify:: root-test lint test build",
    ):
        require(
            contract in makefile_lines,
            "Makefile authority contract is missing {0!r}".format(contract),
            failures,
        )
    require("MAKEFLAGS must not be overridden" in makefile, "Makefile must reject caller MAKEFLAGS", failures)
    require("MAKEFILES must be empty" in makefile, "Makefile must reject startup files", failures)
    require("MAKEFILE_LIST must not be overridden" in makefile, "Makefile must reject Makefile-list replacement", failures)
    require("PYTHON must be a literal executable path" in makefile, "Makefile must reject Python Make syntax", failures)
    require("XCODEBUILD must be a literal executable path" in makefile, "Makefile must reject Xcode Make syntax", failures)
    for script_name in (
        "check_workoutpact_contracts.py",
        "test_login_lifecycle_contract.py",
        "test_login_callback_ownership_contract.py",
        "test_shake_presentation_contract.py",
        "test_async_flow_safety_contract.py",
    ):
        require(
            "'$(REPOSITORY_ROOT_LITERAL)/scripts/{0}'".format(script_name) in makefile,
            "Makefile must use the rooted {0} path".format(script_name),
            failures,
        )
    require(
        "'$(REPOSITORY_ROOT_LITERAL)/workoutpact.xcworkspace'" in makefile,
        "Xcode build must use the rooted workspace path",
        failures,
    )
    require(
        "/usr/bin/find '$(REPOSITORY_ROOT_LITERAL)'" in makefile,
        "Makefile cleanup must stay inside the repository",
        failures,
    )
    require(
        MAKE_AUTHORITY_SCRIPT.is_file() and MAKE_AUTHORITY_SCRIPT.stat().st_mode & 0o111,
        "Make authority harness must exist and be executable",
        failures,
    )
    authority_source = MAKE_AUTHORITY_SCRIPT.read_text(encoding="utf-8")
    require(
        '"GNU Make 4.2.1"' in authority_source,
        "Make authority harness must retain the GNU Make 4.2.1 explicit -f boundary",
        failures,
    )
    for contract in (
        "35 target/authority cases",
        "literal hostile Python path",
        "10 raw Make-syntax controls",
        "2 MAKEFILE_LIST rejections",
        "2 startup-boundary cases",
        "1 version-specific explicit -f path boundary proof",
        "7 later recipe-replacement rejections",
        "1 later double-colon append boundary proof",
        "PATH-Xcode rejection",
        "cleanup containment",
        "10 mode rejections",
    ):
        require(
            contract in authority_source,
            "Make authority harness must retain {0}".format(contract),
            failures,
        )
    for relative_path in (
        "README.md",
        "SECURITY.md",
        "docs/plans/2026-06-21-workoutpact-make-authority-isolation.md",
    ):
        document = read_text(relative_path)
        require(
            "caller-added double-colon recipes" in document,
            f"{relative_path} must document caller-added double-colon recipes as outside trust",
            failures,
        )
        require(
            "Make syntax in an explicit `-f` path is version-sensitive before the repository Makefile loads" in document,
            f"{relative_path} must document explicit -f Make-syntax paths as pre-load caller authority",
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

    transition_plan = read_text("docs/plans/2026-06-16-workoutpact-twitter-transition-guard.md")
    require(
        "Status: Completed" in transition_plan
        and "14 lifecycle mutations were rejected" in transition_plan
        and "Repository and external-directory `make check` passed" in transition_plan
        and "generated-artifact and credential-pattern audits passed" in transition_plan,
        "Twitter transition guard plan must record completed verification evidence",
        failures,
    )

    shake_presentation_plan = read_text(
        "docs/plans/2026-06-16-workoutpact-shake-presentation-guard.md"
    )
    require(
        "Status: Completed" in shake_presentation_plan
        and "five shake-presentation mutations were rejected" in shake_presentation_plan
        and "Repository and external-directory `make check` passed" in shake_presentation_plan
        and "generated-artifact and credential-pattern audits passed" in shake_presentation_plan,
        "shake presentation guard plan must record completed verification evidence",
        failures,
    )

    for doc in ("README.md", "SECURITY.md", "VISION.md", "CHANGES.md"):
        require(
            "overlapping shake confirmation" in read_text(doc).lower(),
            f"{doc} must document the overlapping shake confirmation guard",
            failures,
        )

    payment_validity_plan = read_text(
        "docs/plans/2026-06-26-workoutpact-payment-validity-state.md"
    )
    require(
        "Status: Completed" in payment_validity_plan
        and "17 hostile mutations rejected" in payment_validity_plan
        and "decoy weakness" in payment_validity_plan
        and "make check" in payment_validity_plan,
        "payment validity plan must record completed mutation and gate evidence",
        failures,
    )
    for document_name, document, phrase in (
        ("README.md", readme, "Submit tracks the latest PaymentKit validity"),
        ("SECURITY.md", security, "restore Submit from the latest"),
        ("VISION.md", vision, "Preserve the latest PaymentKit validity"),
        ("CHANGES.md", changes, "payment input validity"),
    ):
        require(
            phrase in document,
            f"{document_name} must document retained payment input validity",
            failures,
        )

    payment_submit_plan = read_text(
        "docs/plans/2026-06-26-workoutpact-payment-submit-configuration.md"
    )
    require(
        "Status: Completed" in payment_submit_plan
        and "paymentSubmissionEnabled()" in payment_submit_plan
        and "configured Stripe test-key" in payment_submit_plan,
        "payment Submit configuration plan must record the shared availability boundary",
        failures,
    )
    for document_name, document, phrase in (
        ("README.md", readme, "Submit remains disabled until"),
        ("SECURITY.md", security, "Stripe Submit availability"),
        ("VISION.md", vision, "Keep Submit disabled when Stripe test-key"),
        ("CHANGES.md", changes, "unconfigured payment submission"),
    ):
        require(
            phrase in document,
            f"{document_name} must document configuration-aware Submit availability",
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
