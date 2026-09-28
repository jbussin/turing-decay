# Audio/video results: preregistered predictions scored (2026-09-28)

Data: 125 participant groups from 58 studies (audio 58 groups / 27 studies; video and audiovisual 67 / 32). Model: three-level REML meta-regression, groups within papers. Code: `analysis/av_preliminary.py`, `analysis/av_sensitivity.py`.

| Prediction | Audio | Video | Verdict |
|---|---|---|---|
| H1, generator decay | −1.3 [−3.7, +1.2] pts/yr; −0.23 [−0.43, −0.04] d′/yr | −0.1 [−1.2, +1.0] pts/yr | Not refuted: audio negative, significant in d′ only; Holm-adjusted p = .71 |
| H2, sawtooth reset | −7.1 [−27.3, +13.1] (7 groups) | +2.9 [−5.0, +10.8] (12 groups) | Not supported; too few reset groups |
| H3, no observer clock (upper bound < +2 pts/yr) | −0.3 [−9.5, +8.8] | +1.8 [−0.8, +4.4] | Inconclusive |
| H4, expertise | +20.4 [−7.3, +48.0] (3 groups) | −8.8 [−23.4, +5.7] (2 groups) | Not testable |
| H5, deployment effort | +3.2 [−4.6, +11.0] (12 groups) | −2.5 [−7.5, +2.5] (36 groups) | Not supported; video in predicted direction (one-sided p = .16) |
| H6, video slower than audio | — | video − audio +1.1 [−1.3, +3.5] pts/yr | Predicted direction, not significant |
| Point: audio above chance at newest generator | +11.7 [+3.9, +19.4] at 2024.7 | — | Supported |
| Point: video < half the GAN-face rate (2.7 pts/yr) | — | −0.1 [−1.2, +1.0] | Supported |

Secondary: half-life of the above-chance margin within text-to-video 1.3 years (33 points at first release, 18 groups); zero-shot voice cloning 5.0 years (26 points, 30 groups).

Sensitivity: `output/av_sensitivity.md`. Pooled H1: −1.2 [−3.2, +0.8] pts/yr (one-sided p = .11).
