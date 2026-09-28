# Search protocol (v0.2.x)

Implements "Search strategy and eligibility" in `preregistration.md`. Every search is run on its database's website and exported, so the record set can be reproduced. Log each run in `search_log.csv` on the day it is run.

The registered string is kept as written. Only the syntax is adapted per database.

## 1. OpenAlex (replaces Scopus, Web of Science, PsycInfo; also covers arXiv and ACL Anthology)

OpenAlex indexes Scopus-scale journals plus arXiv and the ACL Anthology, and exports for free. See deviation D1.

1. Go to <https://openalex.org>, open the search, and switch to **advanced / filter** mode.
2. Filter **Title & abstract** search with:
   ```
   (deepfake OR "synthetic speech" OR "voice cloning" OR "voice clone" OR "AI-generated" OR "machine-generated" OR "text-to-speech" OR "generated video") AND (human OR participant OR participants OR listener OR listeners OR viewer OR viewers) AND (detect OR detection OR discriminate OR discrimination OR distinguish OR "real or fake")
   ```
   OpenAlex stems words and ignores `*`, so the wildcard terms are written out.
3. Add filter **Publication year ≥ 2016**.
4. Export → **CSV** (all results). Save as `openalex_YYYY-MM-DD.csv`.

## 2. PubMed

1. Go to <https://pubmed.ncbi.nlm.nih.gov/advanced/> and paste:
   ```
   (deepfake*[tiab] OR "synthetic speech"[tiab] OR "voice clon*"[tiab] OR "AI-generated"[tiab] OR "machine-generated"[tiab] OR "text-to-speech"[tiab] OR "generated video"[tiab]) AND (human*[tiab] OR participant*[tiab] OR listener*[tiab] OR viewer*[tiab]) AND (detect*[tiab] OR discriminat*[tiab] OR distinguish*[tiab] OR "real or fake"[tiab]) AND 2016:3000[dp]
   ```
2. Save → **All results**, format **CSV**. Save as `pubmed_YYYY-MM-DD.csv`.

## 3. IEEE Xplore

1. Go to <https://ieeexplore.ieee.org/search/advanced/command> and paste:
   ```
   ("All Metadata":deepfake* OR "All Metadata":"synthetic speech" OR "All Metadata":"voice clon*" OR "All Metadata":"AI-generated" OR "All Metadata":"machine-generated" OR "All Metadata":"text-to-speech" OR "All Metadata":"generated video") AND ("All Metadata":human* OR "All Metadata":participant* OR "All Metadata":listener* OR "All Metadata":viewer*) AND ("All Metadata":detect* OR "All Metadata":discriminat* OR "All Metadata":distinguish* OR "All Metadata":"real or fake")
   ```
2. Set year range 2016 to the current year.
3. **Export → Search Results → CSV** (up to 2,000 per export; split by year range if more). Save as `ieee_YYYY-MM-DD.csv`.

## 4. Citation searching

- **Backward:** the reference lists of Diel et al. (2024) and Stockner et al. (2026).
- **Forward:** works citing either paper. In OpenAlex, open each paper and click **Cited by**, then export CSV. Save as `openalex_citedby_diel2024.csv` and `openalex_citedby_stockner2026.csv`.

## What happens next

Upload the exports. The records are then merged, deduplicated by DOI and normalized title, and screened on title and abstract against the eligibility criteria. Screening decisions are recorded in `screening.csv` with one reason per exclusion, following deviation D2.
