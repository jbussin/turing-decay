"""Stage 1 modality rule, as written in screening_rules.md."""
import csv, re
from pathlib import Path
csv.field_size_limit(10**9)
D = Path(__file__).parent
TERMS = r"audio|speech|voice|vocal|speaker|spoken|sound|acoustic|listen|\btts\b|text-to-speech|vocoder|song|singing|\bphone|\bcall|podcast|utteran|prosod|spoof|video|face ?swap|face-swap|talking[ -]head|\blip|movie|\bfilm|footage|\bclip|reenact|animat|avatar|livestream|stream|deep ?fake|deep-fake|synthetic media|multi-?modal|audio-?visual"
pat = re.compile(TERMS, re.I)
recs = list(csv.DictReader(open(D / "records.csv", encoding="utf-8")))
out = []
for r in recs:
    if r["abstract"].strip() and not pat.search(r["title"] + " " + r["abstract"]):
        out.append(dict(record_id=r["record_id"], stage="S1", decision="exclude", reason="S1: no audio, video or deepfake term in title or abstract"))
    else:
        out.append(dict(record_id=r["record_id"], stage="S1", decision="to_S2", reason=""))
with open(D / "screening.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["record_id", "stage", "decision", "reason"]); w.writeheader(); w.writerows(out)
n_ex = sum(o["decision"] == "exclude" for o in out)
print("excluded at S1:", n_ex, "| to Stage 2:", len(out) - n_ex)
