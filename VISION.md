## WorkoutPact App iOS Vision

WorkoutPact App iOS is a legacy iOS prototype combining Twitter login, Digits
phone verification, Stripe-style card tokenization, and a shake-to-share workout
flow.

The repository is useful as a historical mobile prototype for social login,
two-factor style onboarding, payment token creation, and social sharing after a
workout.

The goal is to preserve the prototype while making payment, authentication, and
health/behavior privacy boundaries explicit.

The current focus is:

Priority:

- Preserve login, verification, payment-token, and shake-to-share screens
- Keep Twitter login callbacks weakly owned by the active controller lifecycle
- Keep a single Twitter login transition per visible login appearance
- Keep a single queued logout-to-login transition and reject modal overlap
- Keep API keys and payment credentials out of source control
- Keep retained SDK imports explicit in every Swift file that uses their symbols
- Keep payment UI state guarded while tokenization is in flight
- Reject payment requests and callbacks after the payment screen is covered
- Keep pre-dismissal Stripe and Digits callbacks invalid after reappearance
- Keep PaymentKit input guarded before tokenization
- Keep Stripe tokenization disabled until a local publishable key is configured
- Keep payment failure logs non-sensitive
- Require explicit disclosure that tokenization creates no donation or charge
- Keep social-share result logs out of the prototype
- Gate shake-to-share prompts on the delivered motion subtype
- Reserve one shake confirmation/composer flow until cancellation or provider
  completion, rejecting overlapping shake confirmation and any overlapping
  modal presentation
- Keep storyboard navigation casts guarded
- Guard protected-screen outlets before setup work
- Keep protected-screen keyboard movement bounded to one active shift
- Restore protected-screen keyboard offsets before the view leaves the screen
- Treat Fabric/Digits/TwitterKit and Swift versions as legacy
- Avoid implying real charges or workout enforcement without backend contracts
- Keep portable credential, payment, and sharing contracts running in hosted CI

Next priorities:

- Add README setup notes and archive status
- Document payment-token flow and backend requirements
- Add a real backend contract and tests before enabling billing
- Modernize SDKs only in a dedicated compatibility pass

The modernization boundary is version-specific: Swift 1-era syntax, iOS 8.3,
Stripe 4.0.3, PaymentKit 1.1.1, and retired Fabric, DigitsKit, TwitterCore, and
TwitterKit components must be replaced in staged authentication, payment,
language, and device-verification passes rather than through a bulk project
upgrade.

Contribution rules:

- One PR = one focused auth, payment, sharing, UI, or documentation change.
- Do not commit payment credentials, card data, or tokens.
- Keep real charges disabled unless a backend and tests exist.
- Include device verification notes for motion and sharing behavior.
- Keep shake-to-share prompts tied to explicit shake-motion callbacks.

## Security And Responsible Use

Canonical security policy and reporting:

- [`SECURITY.md`](SECURITY.md)

The app touches identity, payment cards, phone verification, and workout claims.
It should never store raw card data, should keep sharing explicit, and should
avoid logging social-share outcomes or collecting health or behavior data
without a privacy model.

## What We Will Not Merge (For Now)

- Raw card storage
- Checked-in payment or social credentials
- Automatic social posts
- Real billing behavior without backend safeguards

This list is a roadmap guardrail, not a permanent rule.
Strong user demand and strong technical rationale can change it.
