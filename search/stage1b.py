"""Stage 1b human-study rule, as written in screening_rules.md."""
import csv, re, importlib.util
from pathlib import Path
csv.field_size_limit(10**9)
D = Path(__file__).parent
src = open(D / "stage2_view.py").read()
HUM = re.compile(re.search(r'HUM = re.compile\(r"(.*?)", re.I\)', src).group(1), re.I)
recs = {r["record_id"]: r for r in csv.DictReader(open(D / "records.csv", encoding="utf-8"))}
rows = list(csv.DictReader(open(D / "screening.csv")))
n = 0
for s in rows:
    if s["decision"] != "to_S2": continue
    r = recs[s["record_id"]]
    cit = any(x.startswith(("cited_by", "references_of")) for x in r["sources"].split(";"))
    if r["abstract"].strip() and not cit and not HUM.search(r["title"] + " " + r["abstract"]):
        s.update(stage="S1b", decision="exclude", reason="S1b: no human-study term in title or abstract"); n += 1
with open(D / "screening.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["record_id", "stage", "decision", "reason"]); w.writeheader(); w.writerows(rows)
print("excluded at S1b:", n, "| to Stage 2:", sum(s["decision"] == "to_S2" for s in rows))
