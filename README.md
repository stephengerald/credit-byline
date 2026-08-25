# Credit Byline

Turns contributor self-statements into bounded role masks and finalizes a byline only after unanimous contributor approval.

## Why GenLayer

Validators map natural-language contribution statements to a fixed six-role mask while independently replaying the same stored record.

## Reusable workflow

The owner invites contributors, each contributor submits a signed-in-role statement, the roster locks, consensus assesses roles, and contributors unanimously approve the proposed byline. Constructor parameters create a new independent instance, so the code is reusable; state is not shared between deployments.

The contract is deliberately non-custodial. It records a decision, entitlement, score, or approval signal and never transfers GEN.

## Evidence boundary

Role assessment uses only constructor-fixed standards and contributor statements stored on-chain. The contract does not scrape documents or independently prove authorship.

## Verify locally

```powershell
genvm-lint check contracts/credit_byline.py
genvm-lint typecheck contracts/credit_byline.py
pytest tests/direct -q
python tests/run_glsim.py --validators 5
```

With GLSim running in another terminal:

```powershell
gltest tests/integration/test_glsim_consensus.py --network localnet -q
```

The live smoke test requires fresh test-only keys in `GENLAYER_PRIVATE_KEY`, `GENLAYER_SECONDARY_PRIVATE_KEY`, `GENLAYER_TERTIARY_PRIVATE_KEY`. Never commit a `.env` file or use a production wallet.

```powershell
gltest tests/integration/test_studionet_smoke.py --network studionet -s -q --default-wait-interval=6000 --default-wait-retries=240
```

Use the documented 6-second StudioNet polling interval to stay comfortably below public endpoint limits.

See `ARCHITECTURE.md`, `SOURCE_POLICY.md`, `SECURITY.md`, `AUDIT.md`, and `deployments/studionet.json` for the review boundary and exact public evidence.
