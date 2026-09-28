# Turing Decay

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22989631.svg)](https://doi.org/10.5281/zenodo.22989631)

**A three-factor model of human detection of AI-generated content, with preregistered predictions for audio and video.**

Jonathan Bussing · Independent researcher · Version 0.3.0, September 2026

Project page: https://jbussin.github.io/turing-decay/ · Paper: [`paper/turing_decay.pdf`](paper/turing_decay.pdf) (LaTeX source in [`paper/`](paper/))

---

## Citation

Bussing, J. (2026). *Turing Decay: A Three-Factor Model of Human Detection of AI-Generated Content, with Preregistered Predictions for Audio and Video* (v0.3.0). Zenodo. https://doi.org/10.5281/zenodo.23010813

To cite the project as a whole (all versions), use the concept DOI [10.5281/zenodo.22989631](https://doi.org/10.5281/zenodo.22989631).

| Release | Contents | DOI |
| --- | --- | --- |
| v0.1.0 (27 Sep 2026) | Pilot and preregistration of H1–H6 | [10.5281/zenodo.22989632](https://doi.org/10.5281/zenodo.22989632) |
| v0.1.1 (27 Sep 2026) | Links and metadata only | [10.5281/zenodo.22989850](https://doi.org/10.5281/zenodo.22989850) |
| v0.2.0 (27 Sep 2026) | Frozen generator lookup table, archived before any audio or video accuracy value was extracted | [10.5281/zenodo.23002314](https://doi.org/10.5281/zenodo.23002314) |
| v0.3.0 (28 Sep 2026) | Audio and video meta-analysis, predictions scored, full manuscript | [10.5281/zenodo.23010813](https://doi.org/10.5281/zenodo.23010813) |

Any change to the registered analysis plan is recorded as a dated deviation in [`deviations.md`](deviations.md).

## Summary

How fast is the human ability to tell AI-generated content from real content disappearing? This pilot re-analyzes 50 face experiments from a 2026 meta-analysis and 17 text results from 9 studies, separating two clocks: when the **generator** was released and when the **study** was run.

- **Faces:** accuracy fell about 5.3 points per year of generator release within the GAN lineage (p = .006). Against a fixed generator (StyleGAN2), five years of studies show no gain (+0.2 points per year, p = .82). Text-to-image models reset detectability upward, then decayed again: a sawtooth.
- **Text:** untrained readers hit chance by GPT-3 (2020). At a single release date, accuracy fell 6.5 points per tenfold increase in parameters. Frequent LLM users detected AI text about 95% of the time versus about 52% for novices. Humanlike persona prompting moved Turing-test detection from 79% to 27%.

The proposed model: generator capability and deployment effort push human accuracy toward and below chance; hands-on observer expertise is the only factor that pushes back.

Six falsifiable predictions for audio and video are in [`preregistration.md`](preregistration.md). They were written before any audio or video accuracy data were coded, and are scored below.

## Repository

| Path | Contents |
| --- | --- |
| `index.html` | Project page (GitHub Pages) |
| `preregistration.md` | Hypotheses H1–H6, coding scheme, analysis plan |
| `deviations.md` | Dated changes from the registered plan |
| `search/` | Search protocol, search log and database exports |
| `data/faces_pilot.csv` | 50 face experiments coded from Stockner et al. (2026), Appendix A |
| `data/text_pilot.csv` | 17 text results from 9 studies |
| `data/gpt3_size_ladder.csv` | Brown et al. (2020), Table 3.11 |
| `paper/` | Manuscript: `turing_decay.tex`, figures and compiled PDF |
| `data/generator_lookup.csv` | Frozen audio and video generator table: release dates, architecture families (v0.2.0, doi:10.5281/zenodo.23002314) |
| `data/generator_lookup_rules.md` | Rules for assigning dates and families, including mixed and unnamed generators |
| `data/generator_lookup_additions.csv` | Log of generators added during screening, after the freeze |
| `data/extraction_protocol.md` | Units, columns and rules for audio/video data extraction |
| `data/av_extraction.csv` | Extracted audio/video data: one row per participant group (and generator), each number with a source quote |
| `data/generator_coding.csv` | Each extracted row mapped to lookup-table generators, release date and family |
| `data/verification_log.csv` | Every check of an extracted value against its source, and every row dropped, with reason |
| `search/records.csv`, `search/screening.csv`, `search/stage3.csv` | Deduplicated records and screening decisions at every stage |
| `search/screening_rules.md`, `search/prisma.md` | Screening rules and PRISMA flow counts |
| `analysis/faces_pilot.py` | Random-effects meta-regressions for faces |
| `analysis/text_pilot.py` | Text models and the GPT-3 size ladder |
| `analysis/code_generators.py` | Generator coding (reads generator columns only) |
| `analysis/av_preliminary.py`, `analysis/av_sensitivity.py` | Three-level meta-regressions (H1–H6) and registered sensitivity analyses |
| `output/av_results.md` | Predictions scored (audio/video) |
| `output/av_preliminary_summary.md`, `output/av_sensitivity.md` | Model output and sensitivity analyses |

## Audio/video meta-analysis: results (September 2026)

148 studies are included (see `search/prisma.md`); 58 enter the quantitative synthesis (125 participant groups: 58 audio, 67 video or audiovisual). 54 included studies report no usable numbers and, by decision (D6), authors were not contacted. Deviations from the registered plan are listed in `deviations.md` (D1–D6). Full scorecard: `output/av_results.md`.

- People still detect AI audio and video about 17 points above chance.
- **H1:** audio sensitivity falls 0.23 d′ per year of generator release [−0.43, −0.04]; the accuracy slope (−1.3 points per year [−3.7, +1.2]) is not significant, and nothing survives Holm correction. Video is flat overall.
- Within text-to-video, the above-chance margin starts at about 33 points and halves in about 1.3 years.
- **H6** is in the predicted direction (video declines more slowly than audio) but not significant. **H3** is inconclusive; **H2, H4, H5** could not be tested adequately (few reset, expert or post-processed groups).
- Both point predictions hold: audio is still above chance at the newest generator (+11.7 [+3.9, +19.4] points), and video declines at less than half the GAN-face rate.

## Reproduce

```bash
pip install -r requirements.txt
python analysis/faces_pilot.py   # prints models, writes output/
python analysis/text_pilot.py
python analysis/code_generators.py
python analysis/av_preliminary.py
PYTHONPATH=analysis python analysis/av_sensitivity.py
```

Models are random-effects meta-regressions with DerSimonian-Laird between-study variance and the Knapp-Hartung adjustment, implemented in NumPy and SciPy.

## Coding notes

- **Outcome:** accuracy minus chance (0.5, or 0.25 for one four-choice task).
- **Sampling variance:** SD²/n for faces; p(1−p)/n for text, where SDs are rarely reported (approximate).
- **Generator release dates** (decimal year): StyleGAN 2018.95, StyleGAN2 2019.95, StyleGAN3 2021.47, Stable Diffusion 2022.64, GPT-4o images 2025.23, GPT-2 2019.13, GPT-3 2020.42, ChatGPT 2022.92, GPT-4 2023.20.
- **Year run:** publication year minus 0.5 where data-collection dates were not reported.
- **Turing tests:** accuracy = 1 − rate at which the AI was chosen as human. Sample sizes per witness are approximate.

## Limitations

The face slope rests on about six generators, and StyleGAN3 appears only in trained groups. Text variances are approximated. The expert–novice comparison rests on 9 annotators. All coding was done by one author without a second coder.

## Archiving

The repository is connected to Zenodo through its GitHub integration: each GitHub release is archived and receives a DOI, with metadata from `CITATION.cff`.

## Sources

- Stockner, M., Convertino, G., Cambedda, S., & Mazzoni, G. (2026). Are humans able to discriminate between real and deepfake faces? *Computers in Human Behavior: Artificial Humans*, 9, 100332.
- Clark, E., et al. (2021). All that's 'human' is not gold. *ACL 2021*, 7282–7296.
- Brown, T. B., et al. (2020). Language models are few-shot learners. *NeurIPS*, 33, 1877–1901.
- Casal, J. E., & Kessler, M. (2023). *Research Methods in Applied Linguistics*, 2(3), 100068.
- Gao, C. A., et al. (2023). *npj Digital Medicine*, 6, 75.
- Fleckenstein, J., et al. (2024). *Computers and Education: Artificial Intelligence*, 6, 100209.
- Fiedler, A., & Döpke, J. (2025). *International Review of Economics Education*, 49, 100321.
- Russell, J., Karpinska, M., & Iyyer, M. (2025). *ACL 2025*, 5342–5373.
- Jones, C. R., & Bergen, B. K. (2026). Large language models pass a standard three-party Turing test. *PNAS*, 123(21), e2524472123.

## License

Code: MIT (see `LICENSE`). Text, figures and coded data: CC BY 4.0. Source studies remain under their original licenses.
