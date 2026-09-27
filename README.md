# Turing Decay

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22989632.svg)](https://doi.org/10.5281/zenodo.22989632)

**A three-factor model of human detection of AI-generated content, with preregistered predictions for audio and video.**

Jonathan Bussing · Independent researcher · Pilot study, September 2026

Project page: `https://<your-username>.github.io/turing-decay/` (after enabling GitHub Pages)

---

## Citation

Bussing, J. (2026). *Turing Decay: A Three-Factor Model of Human Detection of AI-Generated Content, with Preregistered Predictions for Audio and Video* (v0.1.0). Zenodo. https://doi.org/10.5281/zenodo.22989632

The preregistration is frozen in release v0.1.0 (September 27, 2026). Later releases change only links and metadata; any change to the analysis plan is recorded as a dated deviation.

## Summary

How fast is the human ability to tell AI-generated content from real content disappearing? This pilot re-analyzes 50 face experiments from a 2026 meta-analysis and 17 text results from 9 studies, separating two clocks: when the **generator** was released and when the **study** was run.

- **Faces:** accuracy fell about 5.3 points per year of generator release within the GAN lineage (p = .006). Against a fixed generator (StyleGAN2), five years of studies show no gain (+0.2 points per year, p = .82). Text-to-image models reset detectability upward, then decayed again: a sawtooth.
- **Text:** untrained readers hit chance by GPT-3 (2020). At a single release date, accuracy fell 6.5 points per tenfold increase in parameters. Frequent LLM users detected AI text about 95% of the time versus about 52% for novices. Humanlike persona prompting moved Turing-test detection from 79% to 27%.

The proposed model: generator capability and deployment effort push human accuracy toward and below chance; hands-on observer expertise is the only factor that pushes back.

Six falsifiable predictions for audio and video are in [`preregistration.md`](preregistration.md). They were written before any audio or video accuracy data were coded.

## Repository

| Path | Contents |
| --- | --- |
| `index.html` | Project page (GitHub Pages) |
| `preregistration.md` | Hypotheses H1–H6, coding scheme, analysis plan |
| `data/faces_pilot.csv` | 50 face experiments coded from Stockner et al. (2026), Appendix A |
| `data/text_pilot.csv` | 17 text results from 9 studies |
| `data/gpt3_size_ladder.csv` | Brown et al. (2020), Table 3.11 |
| `analysis/faces_pilot.py` | Random-effects meta-regressions for faces |
| `analysis/text_pilot.py` | Text models and the GPT-3 size ladder |

## Reproduce

```bash
pip install -r requirements.txt
python analysis/faces_pilot.py   # prints models, writes output/
python analysis/text_pilot.py
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

## Enabling the page

1. Push this folder to a public GitHub repository named `turing-decay`.
2. Settings → Pages → Source: *Deploy from a branch* → `main`, folder `/ (root)`.
3. Update the project page URL above once Pages is live, and add the arXiv ID when it exists.

## Archiving with Zenodo

Connect the repository at zenodo.org (GitHub integration), then create a GitHub release. Zenodo archives that release and mints a DOI. `CITATION.cff` supplies the metadata. Make the first release before any audio or video data are extracted, so the preregistration carries a dated, citable snapshot.

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
