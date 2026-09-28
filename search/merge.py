"""Merge database exports, deduplicate, write search/records.csv and a PRISMA-style count."""
import csv, re, sys
from pathlib import Path
csv.field_size_limit(10**9)
EX = Path(__file__).parent / "exports"
def load(name):
    return list(csv.DictReader(open(EX / name, encoding="utf-8")))
def ndoi(d):
    d = (d or "").lower().strip()
    return re.sub(r"^https?://(dx\.)?doi\.org/", "", d)
def ntitle(t):
    return re.sub(r"[^a-z0-9]", "", (t or "").lower())[:120]
recs = []
for r in load("openalex_2026-09-27.csv"):
    recs.append(dict(source="openalex", source_id=r["openalex_id"], doi=ndoi(r["doi"]), title=r["title"], year=r["year"], venue=r["venue"], first_author=r["first_author"], abstract=r["abstract"]))
for r in load("pubmed_2026-09-27.csv"):
    recs.append(dict(source="pubmed", source_id="PMID:" + r["pmid"], doi=ndoi(r["doi"]), title=r["title"], year=r["year"], venue=r["venue"], first_author=r["first_author"], abstract=r["abstract"]))
for r in load("ieee_2026-09-27.csv"):
    recs.append(dict(source="ieee", source_id="IEEE:" + r["article_number"], doi=ndoi(r["doi"]), title=r["title"], year=r["year"], venue=r["venue"], first_author=r["first_author"], abstract=r["abstract"]))
for r in load("citations_2026-09-27.csv"):
    recs.append(dict(source=r["source"], source_id=r["openalex_id"], doi=ndoi(r["doi"]), title=r["title"], year=r["year"], venue=r["venue"], first_author=r["first_author"], abstract=r["abstract"]))
by_source = {}
for r in recs: by_source[r["source"]] = by_source.get(r["source"], 0) + 1
# dedupe: DOI first, then normalized title; keep longest abstract, union of sources
merged, key_of = [], {}
for r in recs:
    keys = [k for k in (("doi:" + r["doi"]) if r["doi"] else None, ("t:" + ntitle(r["title"])) if len(ntitle(r["title"])) > 20 else None) if k]
    hit = next((key_of[k] for k in keys if k in key_of), None)
    if hit is None:
        hit = len(merged); merged.append(dict(r, sources=r["source"], source_ids=r["source_id"]))
    else:
        m = merged[hit]
        if r["source"] not in m["sources"].split(";"): m["sources"] += ";" + r["source"]
        m["source_ids"] += ";" + r["source_id"]
        for f in ("doi", "title", "year", "venue", "first_author"):
            if not m[f] and r[f]: m[f] = r[f]
        if len(r["abstract"]) > len(m["abstract"]): m["abstract"] = r["abstract"]
    for k in keys: key_of.setdefault(k, hit)
for i, m in enumerate(merged): m["record_id"] = f"R{i+1:05d}"
cols = ["record_id", "sources", "source_ids", "doi", "title", "year", "venue", "first_author", "abstract"]
with open(Path(__file__).parent / "records.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(merged)
only_cit = sum(1 for m in merged if all(s.startswith(("cited_by", "references_of")) for s in m["sources"].split(";")))
print("records by source:", by_source)
print("total retrieved:", len(recs), "| unique after dedup:", len(merged), "| duplicates removed:", len(recs) - len(merged))
print("found only via citation searching:", only_cit, "| no abstract:", sum(1 for m in merged if not m["abstract"]))
