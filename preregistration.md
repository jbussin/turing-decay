# Turing Decay — Preregistration

Sep 26, 2026 · Jonathan Bussing

## Overview

This study tests whether human ability to tell AI-generated content from real content follows a three-factor law, Turing Decay, across four modalities. The model was built from pilot analyses of faces and text; audio and video are the confirmatory test.

The three factors:

- **Generator capability** pushes human accuracy toward chance. The decay runs within an architecture lineage and resets when a new paradigm arrives (a sawtooth, not one curve).
- **Deployment effort** (prompting, personas, curation, post-processing) can push accuracy below chance, independent of the generator.
- **Observer expertise** is the only factor that pushes accuracy back up, and only through heavy hands-on use of generative tools, not background exposure.

The primary outcome is detection accuracy minus chance. Hypotheses H1–H6 about audio and video are confirmatory. Anything else, including new moderators and re-analysis of faces and text, is exploratory and will be labeled as such.

## Pilot disclosure

The author has already seen and analyzed face and text data, so those modalities cannot test the model. Audio and video data have not been coded or analyzed as of the date above.

| Modality | Data source | Experiments | Key pilot result |
| --- | --- | --- | --- |
| Faces | Per-experiment table in Stockner et al. (2026) | 50 | Accuracy fell 5.3 pts per year of generator release within the GAN family (p = .006). No gain over calendar time for a fixed generator (StyleGAN2, +0.2 pts/yr, p = .82). Text-to-image models entered about 33 pts more detectable, then decayed. Training added about 7 pts. |
| Text | 9 studies hand-coded (Clark 2021, Brown 2020, Casal & Kessler 2023, Gao 2023, Fleckenstein 2024, Fiedler & Döpke 2025, Russell 2025, Jones & Bergen 2025) | 17 | Untrained readers reached chance by GPT-3 (2020) and stayed there. At a single release date, accuracy fell 6.5 pts per 10x parameters (p = .005). Frequent LLM users scored about 95% vs about 52% for novices. Persona prompting moved Turing-test detection from 79% to 27%. |

Pilot code and coded data are in this repository (`analysis/`, `data/`). Pilot estimates set the expected direction of effects below but are not reused as confirmatory evidence.

## Hypotheses

Each hypothesis applies to audio and to video separately, and names the result that would count against it.

1. **H1, generator decay.** Within an architecture lineage, newer generators yield lower accuracy (negative slope on generator release date). Refuted if the slope is zero or positive in both modalities.
2. **H2, sawtooth reset.** The first generator of a new architecture family is more detectable than the preceding lineage's trend predicts (positive family-reset term). Refuted if the reset term is zero or negative.
3. **H3, no background observer clock.** Holding the generator fixed, accuracy of untrained participants does not rise with the year the study was run (95% CI for that slope includes zero and excludes +2 pts/yr). Refuted if the slope is reliably above +2 pts/yr.
4. **H4, expertise.** Participants with heavy hands-on use of the relevant generative tools (voice cloning, video generation, audio or video editing work) detect better than untrained participants. Refuted if the difference is zero or negative.
5. **H5, deployment effort.** Curated, prompted or post-processed stimuli (for example phone-codec audio, compressed social-media video) yield lower accuracy than raw outputs from the same generator. Refuted if the difference is zero or positive.
6. **H6, modality ordering.** Video decays more slowly than audio (shallower H1 slope), because it offers more channels for artifacts. Refuted if video's slope is steeper than audio's.

Prediction from the pilot, stated for scoring later: audio is still above chance for the newest generators studied, and video decays at under half the per-year rate of GAN faces.

## Search strategy and eligibility

**Databases:** Scopus, Web of Science, PubMed, PsycInfo, IEEE Xplore, ACL Anthology, and arXiv (cs.CL, cs.SD, cs.CV, cs.HC). Reference lists of Diel et al. (2024) and Stockner et al. (2026) will be screened, and forward citations of both will be checked.

**Search string (adapted per database):** (deepfake OR "synthetic speech" OR "voice clon\*" OR "AI-generated" OR "machine-generated" OR "text-to-speech" OR "generated video") AND (human OR participant\* OR listener\* OR viewer\*) AND (detect\* OR discriminat\* OR distinguish\* OR "real or fake").

**Date range:** 2016 to the date of the final search.

**Include:**

- Adult human participants judging whether audio or video stimuli are real or AI-generated
- Both real and AI-generated stimuli in the task
- Reports accuracy, hit and false-alarm rates, or d′, or data from which one can be computed (authors contacted when missing)
- Names the generator, or describes it well enough to assign a release date

**Exclude:**

- Algorithm-only evaluations
- Tasks rating quality or naturalness without a real-vs-fake judgment
- Manipulations that are not generative (splicing, speed changes, cheap-fakes)
- Non-English reports without an available translation

A single author screens titles, abstracts and full texts and extracts all data. To limit drift, screening decisions and every coding judgment are logged with a one-line reason, and a random 20% of records are re-coded by the same author at least two weeks later, with intra-rater agreement (Cohen's kappa) reported. Single-coder screening and extraction is disclosed as a limitation.

## Coding scheme

One row per independent participant group. Groups that overlap with another row (subsamples, repeated measures) are merged or dropped, and the choice is logged.

| Variable | Factor | Coding |
| --- | --- | --- |
| Accuracy minus chance | Outcome | Overall accuracy minus task chance (0.5, or 1/k for k-choice). d′ computed alongside when hit and false-alarm rates are available. |
| Sampling variance | Outcome | SD²/n when SD is reported; otherwise p(1−p)/(n × trials), flagged as approximate |
| Generator release date | Capability | Decimal year of the generator's first public paper, demo or product release |
| Architecture family | Capability | Audio: concatenative, parametric/early neural TTS, zero-shot cloning, speech-to-speech conversion. Video: face-swap autoencoder, GAN reenactment, diffusion/transformer text-to-video. |
| Family reset | Capability | 1 for the first generator of a family in the dataset, else 0 |
| Deployment effort | Deployment | 0 = raw outputs; 1 = curated best-of or light prompting; 2 = adversarial or humanlike prompting, or post-processing that hides artifacts (codec, compression, noise) |
| Real-world channel | Deployment | Phone line, social-media compression, or clean lab playback |
| Observer expertise | Expertise | 0 = general public; 1 = domain professionals (audio engineers, video editors, forensic analysts) without heavy generative-tool use; 2 = heavy users of the relevant generative tools |
| Training or feedback | Expertise | 1 if the group received training, examples or trial-by-trial feedback |
| Year run | Observer clock | Data-collection year if reported, else publication year minus 0.5 |
| Task format | Moderator | Single-item yes/no, paired comparison, Likert, interactive |
| Familiar speaker or face | Moderator | 1 if stimuli show celebrities or voices known to participants |
| Stimulus length | Moderator | Seconds of audio or video per trial |
| Study quality | Moderator | Adapted RoB-2 score, following Stockner et al. (2026) |

Release dates, family assignments and effort codes will be fixed in a public lookup table before any accuracy value is extracted, so the coding cannot be tuned to the results.

## Analysis plan

The primary model is a random-effects meta-regression, fit separately for audio and video, with REML variance estimation and the Knapp-Hartung adjustment. Groups from the same paper are nested within paper (three-level model).

```
y_ij = β0 + β1·GenDate_ij + β2·Reset_ij + β3·Effort_ij + β4·Expertise_ij
          + β5·YearRun_ij + β6·Training_ij + u_j + e_ij
```

Here y is accuracy minus chance for group i in paper j, u is the paper-level random effect and e the group-level error. H6 is tested with the pooled audio-plus-video model and a GenDate × Modality interaction.

**Inference criteria:**

- H1, H2, H4, H5, H6: one-sided test in the predicted direction, α = .05 per modality, Holm correction across the five directional hypotheses within each modality.
- H3: equivalence-style test. Supported if the 95% CI for the YearRun slope lies below +2 pts/yr.
- If a modality yields fewer than 15 independent groups, its results are reported as underpowered and descriptive.
- The half-life of the above-chance margin is reported per lineage from an exponential fit toward 0.5, as a secondary estimate.

**Sensitivity analyses:**

- Drop influential groups (Cook's distance > median + 6 × IQR), then leave-one-paper-out
- d′ in place of accuracy
- Publication year in place of year run
- Exclude groups flagged for approximate variance
- Egger's test and a step-function selection model for small-study effects

Analyses run in R (metafor) or Python (statsmodels), with code published before the final search is run.

## Timeline, data sharing and deviations

**Order of work:** archive this preregistration (tagged GitHub release with Zenodo DOI, or OSF) → publish the release-date and family lookup table → run the search → screen → extract → run the registered analysis → write up. No audio or video accuracy values are extracted before the lookup table is frozen.

**Data sharing:** the coded dataset, lookup table, screening log (PRISMA flow) and analysis code will be public in this repository under CC BY 4.0 (data) and MIT (code).

**Deviations:** any change after archiving is listed in a deviations table in the paper, with the date, the reason and whether it was made before or after seeing outcome data. Results from changed analyses are labeled exploratory; the registered analysis is always reported too.

**Decisions recorded at archiving:**

- Coding: single author, with a delayed 20% re-code for intra-rater agreement (see Search strategy and eligibility).
- H3 threshold: +2 points per year.
- Faces and text may be re-analyzed under this scheme in the same paper; any such analysis is labeled exploratory.
