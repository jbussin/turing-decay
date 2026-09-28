"""Compact view of Stage 2 records for reading: title + the abstract sentence richest in human-study terms."""
import csv, re, sys
from pathlib import Path
csv.field_size_limit(10**9)
D = Path(__file__).parent
HUM = re.compile(r"listening|subjective|abx|turing test|\bmos\b|opinion score|judg|behavio|psycholog|cognit|human-in|\bhumans?\b.{0,40}(?:identif|distinguish|discriminat|tell|recogni|spot|fool|decei)|participant|listener|viewer|subject|respondent|rater|annotator|crowd|survey|experiment|user study|human (?:perform|detect|evaluat|judg|percept|listen|ability|accura|observer|subject|particip|study)|perceptual|perceiv|people|naive|expert|mturk|prolific|forced.choice|2afc|accuracy of human|humans (?:were|are|could|can|cannot)", re.I)
recs = {r["record_id"]: r for r in csv.DictReader(open(D / "records.csv", encoding="utf-8"))}
todo = [s["record_id"] for s in csv.DictReader(open(D / "screening.csv")) if s["decision"] == "to_S2"]
def best(abs_):
    ss = re.split(r"(?<=[.!?])\s+", abs_)
    s = max(ss, key=lambda x: len(HUM.findall(x))) if ss else ""
    return s[:190]
start, end = int(sys.argv[1]), int(sys.argv[2])
for rid in todo[start:end]:
    r = recs[rid]; a = r["abstract"]; m = sorted({x.lower()[:10] for x in HUM.findall(r["title"] + " " + a)})
    print(f"{rid}|{r['year']}|{r['title'][:120]}|H={len(m)}|{best(a) if m else a[:140]}")
