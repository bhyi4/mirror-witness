#!/usr/bin/env python3
"""👁 declare — append a witness declaration of your ledger's current head.

Operators run this, then commit + PR the changed ledger_heads/<operator>.jsonl.
Publishes only head + counts (not ledger contents) — privacy-preserving by default.

usage: declare.py --operator NAME --ledger LABEL --head SEAL --entries N [--anchor-hash H] [--ts ISO]
   or: declare.py --operator NAME --from-anchor path/to/anchor.json --ledger LABEL
"""
import argparse
import hashlib
import json
import time
from pathlib import Path

HEADS = Path(__file__).resolve().parent / "ledger_heads"


def decl_seal(rec):
    body = {k: rec[k] for k in sorted(rec) if k != "decl_seal"}
    return hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()[:16]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--operator", required=True)
    ap.add_argument("--ledger", required=True)
    ap.add_argument("--head"); ap.add_argument("--entries", type=int)
    ap.add_argument("--anchor-hash", default=None)
    ap.add_argument("--from-anchor", default=None)
    ap.add_argument("--ts", default=None)
    a = ap.parse_args()

    if a.from_anchor:
        an = json.loads(Path(a.from_anchor).read_text())
        head, entries = an["head_seal"], an["entry_count"]
        anchor_hash = an.get("anchor_hash"); ts = a.ts or an.get("ts")
    else:
        head, entries, anchor_hash = a.head, a.entries, a.anchor_hash
        ts = a.ts or time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    HEADS.mkdir(exist_ok=True)
    path = HEADS / f"{a.operator}.jsonl"
    prev = "genesis"
    if path.exists():
        lines = [l for l in path.read_text().splitlines() if l.strip()]
        if lines:
            prev = json.loads(lines[-1])["decl_seal"]
    rec = {"operator": a.operator, "ts": ts, "ledger": a.ledger,
           "entry_count": entries, "head_seal": head,
           "anchor_hash": anchor_hash, "prev_decl_seal": prev}
    rec["decl_seal"] = decl_seal(rec)
    with path.open("a") as f:
        f.write(json.dumps(rec) + "\n")
    print(f"👁 declared: {a.operator}/{a.ledger} head={head[:12]} "
          f"entries={entries} decl_seal={rec['decl_seal']}")


if __name__ == "__main__":
    main()
