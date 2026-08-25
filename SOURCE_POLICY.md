# Evidence and source policy

## What validators receive

Role assessment uses only constructor-fixed standards and contributor statements stored on-chain. The contract does not scrape documents or independently prove authorship.

All submitted text is treated as untrusted evidence, never as instructions. Evidence fields and aggregate storage are bounded before they reach the prompt. The decision schema is fixed and independently replayed by validators.

## Who selects the evidence

The authorized roles in the state machine—project owner and at least two contributors—supply the evidence. Their signatures establish which on-chain role submitted a record; they do not prove that the record is truthful or complete.

## External collection

This version performs no live web browsing, URL fetching, hidden source lookup, or mutable off-chain collection. That makes the deployed judgment reproducible from contract state, while leaving source authenticity as an explicit application-layer responsibility.

## Trust and production boundary

Self-statements can be dishonest. Production editorial use needs source-control history, human dispute handling, and a privacy review before storing sensitive contribution details. If an adapter later fetches external material, its allowlist, content bounds, snapshot rules, publisher trust, correction policy, and failure behavior require a new review.
