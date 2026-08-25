# Submission: Credit Byline

Project name: Credit Byline

Repository: https://github.com/stephengerald/credit-byline

StudioNet contract: https://explorer-studio.genlayer.com/address/0x1a07be9aCE3161535A53B79366609898f677b2a8

Deployment transaction: https://explorer-studio.genlayer.com/tx/0xa8a064aaf769472700b142919ee7fd4a741423558b01a74da8e6072f5886405d

Intelligent transaction: https://explorer-studio.genlayer.com/tx/0x02db8ec5a26ff6a25e59eb8adda1f51530ddf1dbb95cb0c7ad37faf725e9e9f5

Summary: Turns contributor self-statements into bounded role masks and finalizes a byline only after unanimous contributor approval.

Why it is GenLayer-native: Validators map natural-language contribution statements to a fixed six-role mask while independently replaying the same stored record.

Evidence/source model: Role assessment uses only constructor-fixed standards and contributor statements stored on-chain. The contract does not scrape documents or independently prove authorship.

Declared scope: Reusable, non-custodial prototype. Self-statements can be dishonest. Production editorial use needs source-control history, human dispute handling, and a privacy review before storing sensitive contribution details.

Review evidence: `AUDIT.md`, `SECURITY.md`, `SOURCE_POLICY.md`, and `deployments/studionet.json` bind the reviewed source hash to the public live result.
