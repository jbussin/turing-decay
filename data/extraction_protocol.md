# Data extraction protocol

Written on 2026-09-27, before any accuracy value was extracted. It implements the coding scheme in `preregistration.md`.

## Units

- **Study** (`study_id`, in `search/studies.csv`): one or more reports of the same participants. Preprints, conference abstracts, dataset deposits and journal versions of one study share a `study_id`. The most complete report is the data source, and the others fill gaps.
- **Row** (`row_id`, in `data/av_extraction.csv`): one independent participant group, split by generator when the study reports accuracy per generator (lookup rule 5). Rows from the same participants share `dependence_id`, so the analysis can merge or drop them as the preregistration requires.

## What is extracted

Only the audio and video arms are extracted. Image and text arms are ignored, as are groups of minors when they can be separated. Each number carries a verbatim quote and its location (`outcome_quote`), so every value can be checked against its source.

| Column | Content |
| --- | --- |
| study_id, record_ids, row_id, dependence_id | Identifiers |
| group_label | Condition or group as the authors name it |
| modality | audio, video, audiovisual, music |
| language | Stimulus language |
| n_participants | Participants in this row after exclusions |
| trials_per_participant | Real-vs-fake judgments each participant made in this row |
| n_real_stimuli, n_fake_stimuli | Stimulus counts |
| task_format | single-item yes/no, paired/2AFC, 3AFC, Likert, interactive |
| chance | 0.5, or 1/k for k-choice |
| accuracy_pct, accuracy_sd | Overall percent correct and its SD across participants |
| hit_rate_pct | Fakes correctly called fake |
| false_alarm_pct | Real items called fake |
| dprime, auc | As reported |
| pct_fake_judged_real | For fake-only designs |
| outcome_quote | Verbatim sentence or table cell, with page, section or table number |
| generator_verbatim | Generator, tool, model or dataset exactly as named |
| generator_share | Stimulus share per generator, when reported |
| curation | raw, curated (best-of or light prompting), adversarial (selected to fool humans or detectors, humanlike prompting) |
| post_processing | Codec, compression, noise or reverberation applied to the stimuli |
| channel | lab, phone, social media |
| participant_type | general public, students, domain professionals, generative-tool users, special population |
| training_feedback | 1 if training, examples or trial feedback preceded or accompanied the judgments; description |
| data_collection | Dates as reported |
| familiar | 1 if celebrities or voices known to the participants |
| stimulus_length_s | Seconds per trial |
| fake_only, minors_included | Flags |
| source_read | URL of the text the numbers came from |
| extraction_confidence | high (read in full text), medium (read in a secondary copy or abstract with numbers), low (inferred) |
| notes | Anything that affects coding |

## Generator coding

Generators are mapped to `data/generator_lookup.csv` from `generator_verbatim` alone, in a separate pass that does not read the outcome columns. New generators go to `data/generator_lookup_additions.csv` under lookup rules 1–4 and 10.

## Missing numbers

If a study describes an eligible task but gives no usable numbers, it is kept with empty outcome columns and listed for author contact, as the preregistration specifies. Values are computed from reported statistics (for example accuracy from hit and false-alarm rates with balanced stimuli) only when the computation is exact. Any computed value is marked `computed` in `notes`.
