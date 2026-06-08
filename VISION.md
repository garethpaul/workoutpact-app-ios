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
- Keep API keys and payment credentials out of source control
- Treat Fabric/Digits/TwitterKit and Swift versions as legacy
- Avoid implying real charges or workout enforcement without backend contracts

Next priorities:

- Add README setup notes and archive status
- Document payment-token flow and backend requirements
- Add explicit confirmation before social sharing
- Modernize SDKs only in a dedicated compatibility pass

Contribution rules:

- One PR = one focused auth, payment, sharing, UI, or documentation change.
- Do not commit payment credentials, card data, or tokens.
- Keep real charges disabled unless a backend and tests exist.
- Include device verification notes for motion and sharing behavior.

## Security And Responsible Use

The app touches identity, payment cards, phone verification, and workout claims.
It should never store raw card data, should keep sharing explicit, and should
avoid collecting health or behavior data without a privacy model.

## What We Will Not Merge (For Now)

- Raw card storage
- Checked-in payment or social credentials
- Automatic social posts
- Real billing behavior without backend safeguards

This list is a roadmap guardrail, not a permanent rule.
Strong user demand and strong technical rationale can change it.
