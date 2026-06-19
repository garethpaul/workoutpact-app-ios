PYTHON ?= python3
override ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
CHECK_SCRIPT := $(ROOT)/scripts/check_workoutpact_contracts.py
LOGIN_CONTRACT_SCRIPT := $(ROOT)/scripts/test_login_lifecycle_contract.py
LOGIN_OWNERSHIP_CONTRACT_SCRIPT := $(ROOT)/scripts/test_login_callback_ownership_contract.py
SHAKE_PRESENTATION_CONTRACT_SCRIPT := $(ROOT)/scripts/test_shake_presentation_contract.py
ASYNC_FLOW_SAFETY_CONTRACT_SCRIPT := $(ROOT)/scripts/test_async_flow_safety_contract.py
WORKSPACE := $(ROOT)/workoutpact.xcworkspace

.PHONY: lint test build verify check

lint:
	$(PYTHON) -m py_compile "$(CHECK_SCRIPT)" "$(LOGIN_CONTRACT_SCRIPT)" "$(LOGIN_OWNERSHIP_CONTRACT_SCRIPT)" "$(SHAKE_PRESENTATION_CONTRACT_SCRIPT)" "$(ASYNC_FLOW_SAFETY_CONTRACT_SCRIPT)"

test:
	$(PYTHON) "$(CHECK_SCRIPT)"
	$(PYTHON) "$(LOGIN_CONTRACT_SCRIPT)"
	$(PYTHON) "$(LOGIN_OWNERSHIP_CONTRACT_SCRIPT)"
	$(PYTHON) "$(SHAKE_PRESENTATION_CONTRACT_SCRIPT)"
	$(PYTHON) "$(ASYNC_FLOW_SAFETY_CONTRACT_SCRIPT)"

build:
	@if ! command -v xcodebuild >/dev/null 2>&1; then \
		echo "xcodebuild unavailable; skipping legacy iOS build"; \
	elif [ ! -d "$(ROOT)/Pods" ]; then \
		echo "Pods directory missing; run pod install on macOS before xcodebuild"; \
	else \
		xcodebuild -workspace "$(WORKSPACE)" -scheme workoutpact -sdk iphonesimulator build CODE_SIGNING_ALLOWED=NO; \
	fi

verify: lint test build

check: verify
