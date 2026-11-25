"""Consistency and leak check for this showcase repository.

1. Every text file is scanned for generic leak patterns: absolute paths and secret-looking words.
2. evidence/runs.json is checked against the invariants the documents state.
3. Every .json file must parse.

Exit code 0 = clean, 1 = findings. Usage: python tools/check_repo.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FORBIDDEN = {
    "absolute path": r"([A-Za-z]:[\\/]|\\\\|/Users/|/home/)",
    "secret-looking word": r"(hmac|api[_-]?key|secret|password|passwd|bearer|private key)",
}

SKIP_DIRS = {".git"}


def text_files():
    for p in sorted(ROOT.rglob("*")):
        if p.is_file() and not (set(p.relative_to(ROOT).parts) & SKIP_DIRS):
            yield p


def scan():
    findings = []
    for p in text_files():
        if p.name == "check_repo.py":
            continue  # this file defines the patterns
        try:
            txt = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            findings.append((p, 0, "binary", "non-text file"))
            continue
        for i, line in enumerate(txt.splitlines(), 1):
            for label, pat in FORBIDDEN.items():
                m = re.search(pat, line, re.I)
                if m:
                    findings.append((p, i, label, m.group(0)))
    return findings


def check_json():
    bad = []
    for p in ROOT.rglob("*.json"):
        try:
            json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            bad.append((p, str(e)))
    return bad


def check_runs():
    errs = []
    runs = json.loads((ROOT / "evidence" / "runs.json").read_text(encoding="utf-8"))
    ids = [r["run"] for r in runs]
    if ids != ["A", "B", "C", "D"]:
        errs.append(f"run ids are {ids}, expected A B C D")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for r in runs:
        if r["receipts_available"]:
            if r["rounds"][-1]["verdict"] != "PASS":
                errs.append(f"{r['run']}: last round is not PASS")
            if not r["reviewed_bytes_equal_committed_bytes"]:
                errs.append(f"{r['run']}: reviewed bytes differ from committed bytes")
            if not (r["reviewed_subject_equals_candidate"] and r["closure_candidate_equals_candidate"]):
                errs.append(f"{r['run']}: subject / candidate identity mismatch")
            if r["anchor_check"] != "[AUDIT_ANCHOR_OK]":
                errs.append(f"{r['run']}: anchor check is {r['anchor_check']}")
            mp = r["final_round_mutation_probes"]
            if mp["killed_nonzero_exit"] != mp["total"]:
                errs.append(f"{r['run']}: not every mutation probe was killed")
            agent = sum(v["seconds"] for k, v in r["agent_jobs"].items() if k in ("planner", "builder", "reviewer"))
            minutes = round(agent / 60, 1)
            if f"{minutes} min" not in readme:
                errs.append(f"README does not show {minutes} min agent time for run {r['run']}")
            if str(r["wall_clock_minutes"]) not in readme:
                errs.append(f"README does not show wall clock {r['wall_clock_minutes']} for run {r['run']}")
        elif r["run"] != "D":
            errs.append(f"{r['run']}: only D may lack receipts")
    return errs


def main():
    ok = True
    for p, line, label, hit in scan():
        ok = False
        print(f"LEAK  {p.relative_to(ROOT)}:{line}  [{label}]  {hit!r}")
    for p, e in check_json():
        ok = False
        print(f"JSON  {p.relative_to(ROOT)}: {e}")
    for e in check_runs():
        ok = False
        print(f"DATA  {e}")
    print("CLEAN" if ok else "FINDINGS")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
