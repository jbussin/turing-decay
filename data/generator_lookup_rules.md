# Generator lookup: coding rules

Frozen with `generator_lookup.csv` in release v0.2.0, before any audio or video accuracy value was extracted. These rules implement the "Generator release date", "Architecture family" and "Family reset" variables in `preregistration.md`.

## Release date

1. **Date = first public appearance** of the generator: arXiv v1, a conference paper, a public code release, or a product announcement, whichever came first.
2. **Precision.** Day-level dates convert to decimal years directly. Month-level dates use the 15th of the month. Year-level dates use July 1. The `confidence` column records how exact the date is: high = day confirmed from a primary source, medium = month-level or secondary source, low = year-level or unverified month.
3. **Named versions are separate rows** (ElevenLabs beta, Multilingual v2, v3; Sora preview, Sora public). A study using an unversioned commercial product is coded to the version live on the study's data-collection date, or, if that date is not reported, the version live six months before publication.
4. **Fine-tuned or re-trained copies** of a named architecture inherit its row (for example, a lab's own VITS voice is coded as VITS).

## Studies that use more than one generator

5. If a study reports accuracy **per generator**, each generator is a separate row in the analysis with its own date.
6. If a study reports only **pooled accuracy** across several generators, the release date is the mean of the constituent dates, weighted by stimulus share when reported, otherwise unweighted. The family is the most common family among the stimuli; ties go to the newest.
7. **Datasets** (ASVspoof, WaveFake, In-the-Wild, FaceForensics++, Celeb-DF, DFDC, DeeperForensics) are coded by their constituent systems when the study reports which ones were used. Only when it does not is the dataset's own row used, with family `mixed (dataset)`. These rows are excluded from the family-reset term and included in the release-date slope.

## Unnamed generators

8. A study that names no generator and gives no description sufficient to identify one is excluded, as the preregistration's eligibility rules require. A study that describes the method class but not the tool (for example "a commercial neural TTS system", "a standard deepfake face swap") is coded to the earliest row of that class that was publicly available at the time of data collection, and flagged `generic` in the extraction sheet.

## Family reset

9. The reset flag is computed from the final dataset, not from this table: within each modality, the included generator with the earliest release date in a family gets reset = 1, and all other generators get 0. Family order follows the table's `family` column.

## Generators found during the search

10. Generators not in this table are added during screening using rules 1–4, **before** the study's accuracy values are read. Each addition is logged in `generator_lookup_additions.csv` with the date it was added and the source used. Existing rows are not changed after the freeze. A date found to be wrong is corrected only in a dated deviations note, with the analysis reported both ways.

## Open-source repositories

11. For tools released as code, the date is the first commit of the **original** repository, or the first tagged release when the commit history has been rewritten. Re-uploads and forks do not reset the date. Two cases in this table:
    - **so-vits-svc**: the original repository (innnky/so-vits-svc) was first committed on 2022-09-22. The widely used svc-develop-team/so-vits-svc repository starts on 2023-03-10 because it is a re-upload.
    - **RVC**: the WebUI repository's commit history was re-imported on 2026-07-19, so its first commit is not the release date. Its release tags keep their original dates, and the first is 1.0.230410, dated 2023-04-09.
