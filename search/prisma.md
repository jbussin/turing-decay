# PRISMA 2020 flow (audio and video meta-analysis)

Counts as of 2026-09-27. Sources: `search/search_log.csv`, `search/screening.csv`, `search/stage3.csv`, `data/av_extraction.csv`, `data/verification_log.csv`, `output/av_analysis_rows.csv`.

## Identification

- Records from databases: 9,963 (OpenAlex 7,814; PubMed 359; IEEE Xplore 1,790)
- Records from citation searching: 255 (cited-by Diel 2024: 53; cited-by Stockner 2026: 1; references of Diel 2024: 103; references of Stockner 2026: 98)
- Total retrieved: 10,218
- Duplicates removed (DOI, then normalized title): 2,609
- Unique records: 7,609 (166 found only through citation searching)

## Screening (titles and abstracts)

- Records screened: 7,609
- Excluded by automatic rule S1 (no audio, video or deepfake term): 2,954
- Excluded by automatic rule S1b (no human-study term): 1,043
- Excluded at Stage 2 (assistant, title and abstract): 3,348
- Reports sought for full-text retrieval: 264

## Eligibility (full text)

- Reports not retrieved: 23
- Reports assessed: 241
- Reports excluded: 75
  - E4, no real-vs-fake judgment (quality, credibility or attitude ratings only): 31
  - E2, not audio or video (images, text, other): 25
  - E3, not an empirical primary study: 11
  - E1, no human judgment: 7
  - E5, non-generative manipulation: 1

## Included

- Reports included: 166, forming 148 studies (preprints, abstracts, datasets and journal versions of one study merged)
- Excluded after extraction: 3 ineligible (ST128; ST012 fake-only after warning; ST026 still images); 3 dropped at verification (ST065 majority-vote metric; ST071 duplicate of ST056; ST124 point-light stimuli)
- Studies with no usable numbers after the full-text, open-data, figure and user-supplied PDF passes: 54
- Studies with numbers but outside the quantitative model:
  - Generator unnamed, undated or non-generative: 13
  - Only hit rate, d′, AUC, % judged real or Likert (no accuracy): 10
  - Music, non-speech audio or non-face video (exploratory only): 6
  - Minors not separable: 1
- **Studies in the quantitative synthesis: 58 (125 participant groups: 58 audio, 67 video or audiovisual)**
