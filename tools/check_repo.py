"""Consistency and leak check for this showcase repository.

1. Every text file is scanned for generic leak patterns: absolute paths and secret-looking words.
2. Every .json file must parse.
3. evidence/runs.json is checked against the invariants and the figures the documents state: verdicts, byte
   equality, identities across rounds, agent minutes, wall clock, the walkthrough timeline and test outcomes.
4. Every relative link in every Markdown file must resolve.

The receipts behind runs.json are private, so this checks that the published data and the published text agree
with each other, not that the data agrees with the receipts.

Exit code 0 = clean, 1 = findings. Usage: python tools/check_repo.py
"""
import json
import re
import sys
from datetime import datetime
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


def check_links():
    errs = []
    for p in ROOT.rglob("*.md"):
        for m in re.finditer(r"\]\(([^)#\s]+)\)", p.read_text(encoding="utf-8")):
            t = m.group(1)
            if t.startswith(("http://", "https://", "mailto:")):
                continue
            if not (p.parent / t).resolve().exists():
                errs.append(f"{p.relative_to(ROOT)} links to missing {t}")
    return errs


def hhmmss(s):
    return datetime.fromisoformat(s).strftime("%H:%M:%S")


def check_runs():
    errs = []
    runs = json.loads((ROOT / "evidence" / "runs.json").read_text(encoding="utf-8"))
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    walk = (ROOT / "docs" / "04-walkthrough-not-pass-to-pass.md").read_text(encoding="utf-8")
    ev = (ROOT / "docs" / "05-evidence-four-closures.md").read_text(encoding="utf-8")
    ids = [r["run"] for r in runs]
    if ids != ["A", "B", "C", "D"]:
        errs.append(f"run ids are {ids}, expected A B C D")
    for r in runs:
        rid = r["run"]
        if not r["receipts_available"]:
            if rid != "D":
                errs.append(f"{rid}: only D may lack receipts")
            continue
        rounds = r["rounds"]
        if rounds[-1]["verdict"] != "PASS":
            errs.append(f"{rid}: last round is not PASS")
        if not r["reviewed_bytes_equal_committed_bytes"]:
            errs.append(f"{rid}: reviewed bytes differ from committed bytes")
        if not (r["reviewed_subject_equals_candidate"] and r["closure_candidate_equals_candidate"]):
            errs.append(f"{rid}: subject / candidate identity mismatch")
        if r["anchor_check"] != "[AUDIT_ANCHOR_OK]":
            errs.append(f"{rid}: anchor check is {r['anchor_check']}")
        mp = r["final_round_mutation_probes"]
        if mp["killed_nonzero_exit"] != mp["total"]:
            errs.append(f"{rid}: not every mutation probe was killed")
        # identities across rounds
        for rd in rounds:
            if rd["candidate_id"] != rd["verdict_subject_id"]:
                errs.append(f"{rid} round {rd['round']}: verdict names another candidate")
            if f"`{rd['candidate_id']}`" not in ev:
                errs.append(f"docs/05 does not list candidate {rd['candidate_id']} of run {rid}")
        cands = [rd["candidate_id"] for rd in rounds]
        if len(set(cands)) != len(cands):
            errs.append(f"{rid}: two rounds share a candidate id")
        if len(rounds) > 1:
            first, last = rounds[0]["file_hashes"], rounds[-1]["file_hashes"]
            if set(first) & set(last):
                errs.append(f"{rid}: a file hash is identical in the rejected and the passing round")
        # times
        tl = r["agent_jobs_timeline"]
        agent_s = sum(j["duration_s"] for j in tl)
        minutes = round(agent_s / 60, 1)
        if f"{minutes} min" not in readme:
            errs.append(f"README does not show {minutes} min agent time for run {rid}")
        if str(r["wall_clock_minutes"]) not in readme or str(r["wall_clock_minutes"]) not in ev:
            errs.append(f"README or docs/05 does not show wall clock {r['wall_clock_minutes']} for run {rid}")
        if any(j["exit_code"] != 0 for j in tl):
            errs.append(f"{rid}: an agent job exited non-zero")
        # verify jobs: PASS polarity in the final round
        for v in rounds[-1]["verify_jobs"]:
            want = 1 if (v["kind"] == "red" and v["target"] == "baseline") else 0
            if v["exit_code"] != want:
                errs.append(f"{rid}: {v['kind']}/{v['target']} exit {v['exit_code']}, expected {want}")
        if rid == "A":
            for j in tl:
                name = {"planner": "Preparer", "builder": "Builder", "reviewer": "Reviewer"}[j["role"]]
                rng = f"{hhmmss(j['started'])} to {hhmmss(j['ended'])}"
                if rng not in walk:
                    errs.append(f"walkthrough lacks time range {rng} ({name} round {j['round']})")
                mins = round(j["duration_s"] / 60, 1)
                if f"{mins} min" not in walk:
                    errs.append(f"walkthrough lacks {mins} min ({name} round {j['round']})")
            for rd in rounds:
                s = round(sum(v["seconds"] for v in rd["verify_jobs"]))
                if f"({s} s in total)" not in walk:
                    errs.append(f"walkthrough lacks verify total {s} s for round {rd['round']}")
            total = round(sum(v["seconds"] for rd in rounds for v in rd["verify_jobs"]), 1)
            if f"{total} seconds" not in walk:
                errs.append(f"walkthrough lacks verify total {total} seconds")
            last = {(v["kind"], v["target"], v["summary"]) for v in rounds[-1]["verify_jobs"]}
            for want in [("green", "candidate", "9 passed"), ("red", "baseline", "8 failed, 1 deselected"),
                         ("regress", "candidate", "2 passed")]:
                if want not in last:
                    errs.append(f"run A final round lacks {want}")
            if "9 passed" not in walk or "8 failed" not in walk:
                errs.append("walkthrough does not state 9 passed / 8 failed")
        if rid in ("B", "C"):
            summ = {v["summary"] for v in rounds[-1]["verify_jobs"]}
            need = {"B": {"26 passed", "25 failed, 1 deselected", "8 passed"}, "C": {"5 passed", "1 failed"}}[rid]
            if not need <= summ:
                errs.append(f"run {rid}: final round summaries {summ} lack {need - summ}")
            for s in need:
                n = s.split()[0]
                if n not in ev:
                    errs.append(f"docs/05 lacks {n} for run {rid}")
    return errs


def main():
    ok = True
    for p, line, label, hit in scan():
        ok = False
        print(f"LEAK  {p.relative_to(ROOT)}:{line}  [{label}]  {hit!r}")
    for p, e in check_json():
        ok = False
        print(f"JSON  {p.relative_to(ROOT)}: {e}")
    for e in check_links():
        ok = False
        print(f"LINK  {e}")
    for e in check_runs():
        ok = False
        print(f"DATA  {e}")
    print("CLEAN" if ok else "FINDINGS")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
