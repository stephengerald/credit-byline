# Architecture

## State machine

The owner invites contributors, each contributor submits a signed-in-role statement, the roster locks, consensus assesses roles, and contributors unanimously approve the proposed byline.

The relevant roles are project owner and at least two contributors. Write methods enforce role, phase, uniqueness, and bounded-storage rules before any state transition.

## Consensus boundary

Validators map natural-language contribution statements to a fixed six-role mask while independently replaying the same stored record. The leader returns a small JSON schema; validators independently rerun the same decision function and accept only exact enum or bitmask values. Malformed model output raises a tagged model error and writes no decision.

## Deterministic boundary

Enrollment, authorization, commitments, counters, phase changes, caps, masks, and any score or credit arithmetic are deterministic contract logic. Only semantic interpretation of the stored evidence occurs inside `run_nondet_unsafe`.

## Off-chain boundary

Wallet custody, identity verification, indexing, notifications, private file storage, source authentication, money movement, legal process, and user-interface behavior are outside this repository. Self-statements can be dishonest. Production editorial use needs source-control history, human dispute handling, and a privacy review before storing sensitive contribution details.
