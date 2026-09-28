"""Record Stage 2 decisions for a batch. Usage: stage2_record.py START END decisions.txt
decisions.txt lines: RID|include|reason  or  RID|full_text|reason  or  RID|exclude|CODE (overrides).
Records in the batch not listed are excluded with code E1."""
import csv, sys
from pathlib import Path
D = Path(__file__).parent
CODES = {"E1": "no human real-vs-fake judgment of AI-generated stimuli (detector, generator, dataset or other study)",
         "E2": "stimuli are not audio or video (text or still images)",
         "E3": "not an empirical study (review, survey of methods, commentary, legal or policy analysis)",
         "E4": "humans rate quality or naturalness only, no real-vs-fake judgment",
         "E5": "manipulation is not generative (splicing, editing, cheap-fake)"}
rows = list(csv.DictReader(open(D / "screening.csv")))
todo = [r["record_id"] for r in rows if r["decision"] == "to_S2"]
start, end = int(sys.argv[1]), int(sys.argv[2])
batch = set(todo[start:end]) if start >= 0 else set()
dec = {}
for line in open(sys.argv[3]):
    line = line.strip()
    if not line: continue
    rid, d, why = line.split("|", 2)
    dec[rid] = (d, CODES.get(why, why))
for r in rows:
    if r["record_id"] in dec:
        d, why = dec[r["record_id"]]; r.update(stage="S2", decision=d, reason=(why if d != "exclude" else "S2 " + why))
    elif r["record_id"] in batch:
        r.update(stage="S2", decision="exclude", reason="S2 " + CODES["E1"])
with open(D / "screening.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["record_id", "stage", "decision", "reason"]); w.writeheader(); w.writerows(rows)
from collections import Counter
print(Counter(r["decision"] for r in rows))
