# Audio/video model results (2026-09-28)

Model output for the audio/video meta-analysis. Extraction was checked against sources and missing values recovered as logged in deviation D6. Code: `analysis/av_preliminary.py`; full output: `output/av_preliminary.json`. Scorecard: `output/av_results.md`.

Data: 125 groups from 58 studies after verification, targeted recovery, the browser pass and the user-supplied PDF pass of 2026-09-28 (audio 58 groups / 27 studies; video and audiovisual 67 / 32). Recovery methods are logged per value (deviation D6). Sensitivity analyses: `output/av_sensitivity.md`.

| | Audio | Video |
|---|---|---|
| Mean above chance at 2020 generators | +17.7 | +16.8 |
| H1 GenDate slope (alone) | −1.3 [−3.7, +1.2] | −0.1 [−1.2, +1.0] |
| H1, untrained public only | −0.1 [−3.0, +2.8] | +0.1 [−1.1, +1.3] |
| H1, full model | −1.6 [−5.9, +2.8] | +0.1 [−1.3, +1.6] |
| H1 in d′ per year | −0.23 [−0.43, −0.04] | −0.01 [−0.10, +0.08] |
| H3 year run, generator fixed | −0.3 [−9.5, +8.8] | +1.8 [−0.8, +4.4] |

Pooled H1: −1.2 [−3.2, +0.8] points per year (one-sided p = .11). H6 (video minus audio slope): +1.1 [−1.3, +3.5].

Change from the 52-study run: five audio studies added (ST039, ST062, ST119, ST127, ST132) and one video study (ST112). Two of the audio studies use recent generators with listeners judging their own or a friend's voice, and score high (ST062, ST119). The audio accuracy slope weakened from −2.1 to −1.3; the d′ slope stays below zero. Excluding familiar-voice rows gives −1.6 [−4.3, +1.2] (audio), so familiarity does not explain the change.

Open issues:
- ST035 scores 'no idea' answers as wrong, so its groups fall below chance; kept and flagged.
- 54 included studies lack usable numbers.
- Dataset rows (DFDC, Celeb-DF, ASVspoof) pool their constituent generators under one date.
- 18 of 51 generator additions carry medium or low date confidence.
