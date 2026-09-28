# Screening rules

Written before each rule is applied. Every decision is logged in `screening.csv` with the rule or stage that made it.

## Stage 1: modality rule (automatic)

Eligibility requires audio or video stimuli (`preregistration.md`, Include). A record is **excluded** at this stage only if all of the following hold:

1. It has an abstract (records without one go to Stage 2 on the title).
2. Neither its title nor its abstract contains any audio, video or deepfake term. Terms are matched case-insensitively on word stems:
   - **Audio:** audio, speech, voice, vocal, speaker, spoken, sound, acoustic, listen, TTS, text-to-speech, vocoder, song, singing, phone, call, podcast, utterance, prosody, spoof
   - **Video:** video, face swap, face-swap, faceswap, talking head, talking-head, lip, movie, film, footage, clip, reenact, animation, avatar, livestream, stream
   - **Either:** deepfake, deep fake, deep-fake, synthetic media, multimodal, multi-modal, audiovisual, audio-visual
3. Reason logged: `S1: no audio, video or deepfake term in title or abstract`.

The list is deliberately broad. A record mentioning any term goes to Stage 2 even when the term is incidental, so this rule removes only records that cannot be about audio or video.

## Stage 1b: human-study rule (automatic)

Eligibility requires human participants making a real-versus-fake judgment. A Stage 1 survivor is **excluded** here only if all of the following hold:

1. It has an abstract.
2. Its title and abstract contain none of the human-study terms in `stage2_view.py` (`HUM`): participant, listener, listening, viewer, subject, respondent, rater, annotator, crowd, survey, experiment, user study, subjective, ABX, Turing test, MOS / opinion score, judg-, behavio-, psycholog-, cognit-, perceptual, perceiv-, people, naive, expert, MTurk, Prolific, forced choice, 2AFC, "human" followed by perform/detect/evaluat/judg/percept/listen/ability/accura/observer/subject/particip/study, or "humans" near identify/distinguish/discriminate/tell/recognize/spot/fool/deceive.
3. It did **not** come from citation searching (records citing or cited by Diel et al., 2024 or Stockner et al., 2026 always go to Stage 2).
4. Reason logged: `S1b: no human-study term in title or abstract`.

A random sample of 45 records meeting these conditions was read before the rule was adopted; all 45 were detector, generator or policy papers with no human participants.

## Stage 2: title and abstract (assistant)

Each remaining record is judged against the Include and Exclude criteria. Decisions: `include`, `exclude` (with the criterion that fails), or `full_text` (cannot be decided from title and abstract).

## Stage 3: full text (assistant)

Every `include` and `full_text` record from Stage 2 is checked against the full text where it can be obtained. Records whose full text cannot be obtained are listed as `not retrieved` in the PRISMA flow, not silently excluded.
