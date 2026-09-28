# Deviations from the preregistration

Each entry records the date, what changed, why, and whether it was decided before or after seeing outcome data. The registered plan is `preregistration.md` in release v0.1.0 (doi:10.5281/zenodo.22989632).

## D1. Database substitution

- **Date:** 2026-09-27
- **Registered:** Scopus, Web of Science, PubMed, PsycInfo, IEEE Xplore, ACL Anthology, arXiv.
- **Change:** Scopus, Web of Science and PsycInfo are replaced by OpenAlex, which also covers arXiv and the ACL Anthology. PubMed and IEEE Xplore are kept.
- **Reason:** The author has no institutional subscription to Scopus, Web of Science or PsycInfo. OpenAlex indexes a comparable journal set and allows full, free export, which makes the search reproducible by anyone.
- **Timing:** Before any search was run and before any outcome data were seen.
- **Expected impact:** Some records indexed only by the subscription databases may be missed. Citation searching (backward and forward from Diel et al., 2024 and Stockner et al., 2026) is kept as a check. A study found only through citation searching is noted in the screening log, so the size of the gap can be reported.

## D2. AI-performed screening and extraction

- **Date:** 2026-09-27 (amended the same day, before any record was screened)
- **Registered:** A single author screens and extracts all records.
- **Change:** An AI assistant (Claude, Anthropic) screens every record and extracts the data. The author does not review each decision. Records the assistant cannot decide from the title and abstract are not excluded: their full text is checked, and the record is included or excluded on that basis.
- **Reason:** The search returned 7,609 unique records, too many for one person to review in a reasonable time.
- **Safeguards:** Every decision is logged in `search/screening.csv` with a one-line reason and the stage at which it was made (rule, title/abstract, full text). Any rule applied to many records at once is written in `search/screening_rules.md` before it is run. The screening is fully reproducible from these files.
- **Timing:** Before any record was screened and before any outcome data were seen.
- **Reporting:** The paper states that screening and extraction were performed by an AI assistant without per-record human review. This is a limitation. If the author later checks a random sample, agreement is reported.

## D3. Search run through database APIs rather than manual export

- **Date:** 2026-09-27
- **Registered:** Searches exported from each database's website (`search/search_protocol.md`).
- **Change:** The same query strings were run through each database's search API (OpenAlex API, NCBI E-utilities, the IEEE Xplore search service) from a web browser, and the results saved as CSV.
- **Reason:** API retrieval returns every record with full abstracts and records the exact query, so the search can be rerun exactly.
- **Timing:** Before screening and before any outcome data were seen.
- **Expected impact:** None on which records are retrieved. OpenAlex's count changed from 7,812 to 7,814 during retrieval as its index updated.

## D4. Full-text screening and extraction through a summarizing web tool

- **Date:** 2026-09-27
- **Registered:** Full texts read and data extracted by one coder.
- **Change:** Stage 3 screening and data extraction were done by several AI assistant instances working in parallel (see D2), each reading full texts through a web-fetch tool that returns a model-written rendering of the page rather than the raw text. Many publisher sites blocked or rate-limited the tool, so some decisions rest on abstracts (marked in `search/stage3.csv` and `data/av_extraction.csv`).
- **Safeguards:** Every extracted number carries a quote and location in `outcome_quote`; quotes marked "as rendered" must be checked against the source before analysis. `extraction_confidence` records how each value was read. Generator coding against the lookup table is done in a separate pass from `generator_verbatim` only.
- **Timing:** Before any analysis was run.

## D5. Coding conventions added after the lookup freeze

- **Date:** 2026-09-27
- **Change:** (1) A TTS pipeline (acoustic model + vocoder) is dated by its newest component. (2) Audiovisual groups are analysed with video. (3) Rows pooling generators are dropped when per-generator rows exist (rule 5). (4) Non-speech audio and music are coded but analysed only as exploratory. (5) Generator additions were dated from the assistant's knowledge of the cited primary sources and flagged medium/low confidence pending verification.
- **Timing:** Decided during generator coding, after some outcome values had been seen in extraction summaries; the coding script reads only generator columns. A preliminary analysis (output/av_preliminary_summary.md) has been run on unverified data; it is labelled preliminary and will be rerun after verification.
- **Update 2026-09-28:** 49 generator additions checked against primary records (arXiv v1 dates via OpenAlex, GitHub repository and release dates via the GitHub API, one product announcement). 33 are now high confidence; 7 dates were corrected by 1–3 days or refined from month to day. None of the corrections moved any H1 estimate by more than 0.01 points per year. 16 remain medium or low confidence, 5 of them music or non-speech audio used only in exploratory analyses.

## D6. Missing values recovered without contacting authors

- **Date:** 2026-09-28
- **Registered:** Authors contacted when a study reports no usable values.
- **Change:** Authors were not contacted. Instead, missing values were recovered by (a) reading full texts, preprints and repository copies through a web browser; (b) computing accuracy from the authors' posted trial-level data where available (ST091, Kaggle); (c) reading values printed in figures or figure tables where the text gave none (ST013, ST028, ST043, ST126), marked "FIGURE VALUES" and low or medium confidence; and (d) computing balanced accuracy, (hit rate + correct-rejection rate) / 2, where only per-class rates were reported. Every recovered value records its source and method in `data/av_extraction.csv` (pre-pass copy kept as `data/av_extraction_before_browserpass.csv`).
- **Reason:** To keep the review self-contained and reproducible from public materials, and to avoid a multi-week wait for replies.
- **Timing:** After the preliminary analysis had been run on 91 groups (see D5).
- **Effect:** 12 more studies entered the model (52 studies, 110 groups). 60 included studies still report no usable values and are marked "NUMBERS MISSING" in `data/av_extraction.csv`; several are behind publisher bot checks (ScienceDirect, OUP, ACM, SSRN, Wiley) and could be recovered by a manual visit.
- **Update 2026-09-28 (second pass):** Full texts obtained through the ACM Digital Library in the browser (ST039, ST119, ST134) and PDFs downloaded by the author from open-access or preprint pages (ST026, ST062, ST112, ST125, ST127, ST132). Two further methods were used: (e) accuracy computed from posted trial data on OSF (ST062, osf.io/prv6e); (f) for ST132, hit and false-alarm rates were first solved from the reported A′ and B″D means, then replaced by exact values computed from the authors' OSF trial data (osf.io/uzh78) once the author downloaded it; the solved values were within 1.3 points of the exact ones. ST026 was found to use still images and was excluded as ineligible. **Effect:** 58 studies and 125 groups in the model; 54 included studies still report no usable values. Pre-pass copy: `data/av_extraction_before_pass2.csv`.
