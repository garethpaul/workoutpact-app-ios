PYTHON ?= python3

.PHONY: lint test build verify check

lint:
	$(PYTHON) -m py_compile scripts/check_workoutpact_contracts.py

test:
	$(PYTHON) scripts/check_workoutpact_contracts.py

build:
	@if ! command -v xcodebuild >/dev/null 2>&1; then \
		echo "xcodebuild unavailable; skipping legacy iOS build"; \
	elif [ ! -d Pods ]; then \
		echo "Pods directory missing; run pod install on macOS before xcodebuild"; \
	else \
		xcodebuild -workspace workoutpact.xcworkspace -scheme workoutpact -sdk iphonesimulator build CODE_SIGNING_ALLOWED=NO; \
	fi

verify: test

check: lint test build verify
