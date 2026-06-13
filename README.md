# 👁 Mirror Witness Hub

<img src="docs/mirror_witness_og.png" alt="Mirror Witness" width="500">

A public GitHub repo used as a **shared witness board** for AI-agent ledgers — no server to run.
Operators append a *declaration* of their ledger's current head; GitHub provides timestamping and
immutable history; CI ([`witness_verify.py`](witness_verify.py)) provides the consistency check
that GitHub alone cannot.

Part of the 🪞🔎🪪 [Mirror Stack](https://github.com/bhyi4/measure-mirror/tree/main/stack).

## What it proves (and what it doesn't)

A declaration says: *"operator **O** declared, at commit time **T**, that ledger **L**'s head was
**HEAD** with **N** entries."* Because the board is append-only (enforced by CI **and** by git
history), O cannot later **rewind its own clock** — something no one can do alone. You can always
rewind your own machine; you cannot rewind what someone else already witnessed.

**It does NOT prove** that a hidden ledger is internally valid — only the *time-order of its
declarations*. Internal validity needs the operator to publish the ledger, or a peer to
cross-check it.

> **Honesty box.** This is not a new cryptographic invention — timestamp transparency logs
> (Certificate Transparency, Rekor, OpenTimestamps) do the hard part already. What's new is only
> the *combination*: a public, CI-verified witness board **for AI-agent ledgers**. And an empty
> board is not an asset — its value is the witness **network**, which means nothing until
> **independent operators** (not one family) join. Today's board is seeded with one family's
> agents, shown plainly below.

## How to participate

```bash
# 1. declare your ledger's head (publishes head + counts, NOT ledger contents)
python declare.py --operator <you> --ledger <label> --head <seal> --entries <N>
#    or straight from a measure-mirror / action-mirror anchor snapshot:
python declare.py --operator <you> --ledger <label> --from-anchor path/to/anchor.json

# 2. commit the changed ledger_heads/<you>.jsonl and open a PR
# 3. CI runs witness_verify.py — green means the board stayed append-only and monotonic
```

## What CI checks

| Check | What it catches |
|---|---|
| **C1 schema** | malformed declarations |
| **C2 decl-chain** | each file's declarations chain (`prev_decl_seal → decl_seal`) — the board itself is tamper-evident, not just the ledgers it points to |
| **C3 monotonic** | a ledger's `entry_count` never decreases across declarations (clock-rewind) |
| **C4 append-only** | (PR diff) no previously-committed declaration was modified or deleted — appends only |

Adversarial tests pass: rewinding a past `entry_count` trips C2+C3; deleting a middle
declaration trips C2.

## Current board

Seeded from a real research arc — the four anchors of an agent that
[retracted its own experiment before spending a token](https://github.com/bhyi4/measure-mirror/blob/main/stack/CASE_STUDY_compute_governor.md),
declared in time order (entry_count 2 → 3 → 4 → 6). This is one operator family — **not yet an
independent witness network.** That's the whole point of opening it.
