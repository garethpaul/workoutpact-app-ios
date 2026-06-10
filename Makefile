PYTHON ?= python3
ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
CHECK_SCRIPT := $(ROOT)/scripts/check_workoutpact_contracts.py
WORKSPACE := $(ROOT)/workoutpact.xcworkspace

.PHONY: lint test build verify check

lint:
	$(PYTHON) -m py_compile "$(CHECK_SCRIPT)"

test:
	$(PYTHON) "$(CHECK_SCRIPT)"

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
