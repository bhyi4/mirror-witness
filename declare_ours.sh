#!/usr/bin/env bash
# Declare our family's current ledger heads to the witness board (no push — that's manual).
# Reads each ledger's last seal and appends a declaration under operator "seara".
set -euo pipefail
L=/data/seara/mirror_ledgers
HERE=/data/seara/mirror_witness
head_of() { tail -1 "$1" | /usr/bin/python -c "import json,sys;print(json.loads(sys.stdin.read())['seal'])"; }
count_of() { grep -c . "$1"; }

declare_one() {  # label  ledger_path
  local label="$1" path="$2"
  [ -f "$path" ] || { echo "skip $label (no ledger)"; return; }
  /usr/bin/python "$HERE/declare.py" --operator seara --ledger "$label" \
    --head "$(head_of "$path")" --entries "$(count_of "$path")"
}

declare_one compute_governor_mm "$L/compute_governor.jsonl"
declare_one seara_action        "$L/seara.jsonl"
declare_one provenance          "$L/provenance.jsonl"

echo "--- verify board ---"
/usr/bin/python "$HERE/witness_verify.py" | tail -1
echo "→ to publish: git -C $HERE add ledger_heads && git -C $HERE commit -m 'declare: seara heads' && git -C $HERE push"
