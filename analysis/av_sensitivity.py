"""Registered sensitivity analyses, Holm correction and half-life fits (preliminary data).

Reuses the dataset and three-level model from av_preliminary.py.
Output: output/av_sensitivity.json and output/av_sensitivity.md
"""
import contextlib, io, csv, json, math, re
import numpy as np
from scipy import stats, optimize

with contextlib.redirect_stdout(io.StringIO()):
    import av_preliminary as P  # builds P.data, defines P.fit3

ext = {r['row_id']: r for r in P.rows}
for d in P.data:
    r = ext[d['row']]
    d['raw_modality'] = r['modality']
    d['approx_n'] = int('APPROX_N' in r['notes'])
    pubs = [P.num(P.rec[x]['year']) for x in r['record_ids'].split(';') if x in P.rec]
    d['pubyr'] = min(p for p in pubs if p) - 0.5 if any(pubs) else None
    d['is_dataset'] = int('dataset' in d['family'])
    h, fa, dp = P.num(r['hit_rate_pct']), P.num(r['false_alarm_pct']), P.num(r['dprime'])
    if h is not None and fa is not None:
        clip = lambda x: min(max(x / 100, 0.005), 0.995)
        d['dprime'] = stats.norm.ppf(clip(h)) - stats.norm.ppf(clip(fa))
    else:
        d['dprime'] = dp

def slope(sub, cols=('gendate',), name='gendate'):
    sub = [d for d in sub if d.get('yrun') is not None]
    if len(sub) < 5 or len({d['study'] for d in sub}) < 3: return None
    f = P.fit3(sub, list(cols))
    c = f['coef'].get(name)
    return None if c is None else dict(k=f['k'], papers=f['papers'], b=c['b'] * 100, lo=c['ci'][0] * 100, hi=c['ci'][1] * 100,
                                       p_one=float(stats.t.sf(-c['t'], c['df'])) if name == 'gendate' else None, p_two=c['p_two'])

full = ['gendate', 'reset', 'effort', 'expert', 'yrun', 'train']
out = {}
for m in ['audio', 'video']:
    S = [d for d in P.data if d['modality'] == m]
    o = {}
    o['primary_gendate_only'] = slope(S)
    o['primary_full'] = slope(S, full)
    # 1. influence: leave-one-row-out change in GenDate slope, Cook-style
    base = P.fit3([d for d in S if d['yrun']], ['gendate'])['coef']['gendate']
    infl = []
    for i, d in enumerate(S):
        f = P.fit3([x for j, x in enumerate(S) if j != i and x['yrun']], ['gendate'])['coef']['gendate']
        infl.append(((f['b'] - base['b']) / base['se']) ** 2)
    infl = np.array(infl); thr = np.median(infl) + 6 * (np.percentile(infl, 75) - np.percentile(infl, 25))
    flagged = [S[i]['row'] for i in np.where(infl > thr)[0]]
    o['influential_rows'] = flagged
    o['drop_influential'] = slope([d for d in S if d['row'] not in flagged])
    # 2. leave-one-paper-out range
    loo = []
    for st in sorted({d['study'] for d in S}):
        s = slope([d for d in S if d['study'] != st])
        if s: loo.append((st, s['b']))
    o['leave_one_paper_out'] = dict(min=min(loo, key=lambda x: x[1]), max=max(loo, key=lambda x: x[1]))
    # 3. d' in place of accuracy
    Sd = []
    for d in S:
        if d['dprime'] is None or not math.isfinite(d['dprime']): continue
        x = dict(d); x['y'] = d['dprime']; x['v'] = 2 / d['n'] + d['dprime'] ** 2 / (4 * d['n'])  # approximate
        Sd.append(x)
    s = slope(Sd)
    o['dprime'] = None if not s else dict(s, b=s['b'] / 100, lo=s['lo'] / 100, hi=s['hi'] / 100, units="d' per year")
    # 4. publication year in place of year run
    Sp = [dict(d, yrun=d['pubyr']) for d in S if d['pubyr']]
    o['pubyear_H3'] = slope(Sp, full, 'yrun')
    o['yearrun_H3'] = slope(S, full, 'yrun')
    # 5. exclude approximate variance
    o['exact_variance_only'] = slope([d for d in S if not d['approx']])
    o['exclude_approx_N'] = slope([d for d in S if not d['approx_n']])
    # 6. exclude dataset-coded rows (constituents not split)
    o['exclude_dataset_rows'] = slope([d for d in S if not d['is_dataset']])
    # 6b. base rate: rows with unequal real/fake counts in single-item tasks -> balanced accuracy where hit/FA exist, else drop
    def _unequal(r):
        nr, nf = P.num(r['n_real_stimuli']), P.num(r['n_fake_stimuli'])
        tf = r['task_format'].lower()
        return nr is not None and nf is not None and max(nr, nf) / max(min(nr, nf), 1) > 1.25 and not any(k in tf for k in ('afc', 'paired', 'alternative'))  # >25% imbalance
    Sb = []
    for d in S:
        r = ext[d['row']]
        if not _unequal(r): Sb.append(d); continue
        h, fa = P.num(r['hit_rate_pct']), P.num(r['false_alarm_pct'])
        if h is not None and fa is not None: Sb.append(dict(d, y=(h + 100 - fa) / 200 - 0.5))
    o['balanced_base_rate'] = slope(Sb)
    # 7. audiovisual separately (video only)
    if m == 'video':
        o['video_only_no_av'] = slope([d for d in S if d['raw_modality'] == 'video'])
    # 8. Egger / PET: accuracy regressed on SE within the three-level model
    Se = [dict(d, se=math.sqrt(d['v'])) for d in S]
    f = P.fit3([d for d in Se if d['yrun']], ['se'])
    c = f['coef'].get('se')
    o['egger'] = dict(b=c['b'], p_two=c['p_two'], k=f['k'])
    # 9. Holm across directional hypotheses in the full model (H1 gendate<0, H2 reset>0, H4 expert>0, H5 effort<0, training reported)
    ff = P.fit3([d for d in S if d['yrun']], full)['coef']
    dirs = {'H1_gendate': ('gendate', -1), 'H2_reset': ('reset', +1), 'H4_expert': ('expert', +1), 'H5_effort': ('effort', -1)}
    ps = {}
    for h, (nm, sgn) in dirs.items():
        if nm in ff:
            c = ff[nm]; ps[h] = float(stats.t.sf(sgn * c['t'], c['df']))
        else:
            ps[h] = None
    avail = sorted([(p, h) for h, p in ps.items() if p is not None])
    holm = {}; running = 0
    for i, (p, h) in enumerate(avail):
        adj = min(1, (len(avail) - i) * p); running = max(running, adj); holm[h] = running
    o['one_sided_p'] = ps; o['holm_p'] = holm
    out[m] = o

# 10. Half-life of the above-chance margin per family (secondary): y = a * exp(-lam * (t - first release in lineage))
hl = {}
for m in ['audio', 'video']:
    for fam in sorted({d['family'] for d in P.data if d['modality'] == m and 'dataset' not in d['family']}):
        S = [d for d in P.data if d['modality'] == m and d['family'] == fam and d['train'] == 0 and d['expert'] == 0]
        dates = {round(d['gendate'], 2) for d in S}
        if len(S) < 4 or len(dates) < 3: continue
        t0 = min(d['gendate'] for d in S); t = np.array([d['gendate'] - t0 for d in S]); y = np.array([d['y'] for d in S]); w = 1 / np.array([d['v'] + 0.005 for d in S])
        def loss(p): return np.sum(w * (y - p[0] * np.exp(-p[1] * t)) ** 2)
        r = optimize.minimize(loss, [max(y.mean(), 0.05), 0.1], method='Nelder-Mead')
        a, lam = r.x
        hl[f'{m}: {fam}'] = dict(k=len(S), n_dates=len(dates), first_release=round(t0, 2), margin_at_first=round(a * 100, 1), lam=round(lam, 3),
                                 half_life_years=(round(math.log(2) / lam, 1) if lam > 0 else 'no decay (lambda <= 0)'))
out['half_life'] = hl
out['not_run'] = ['step-function selection model (too few groups per modality for stable estimation; planned for the final dataset)']
json.dump(out, open('output/av_sensitivity.json', 'w'), indent=1, default=str)

# markdown summary
L = ['# Sensitivity analyses (preliminary data)', '', 'GenDate slope in accuracy points per year of generator release, 95% CI. Generated by `analysis/av_sensitivity.py`.', '']
def fmt(s): return '—' if not s else f"{s['b']:+.2f} [{s['lo']:+.2f}, {s['hi']:+.2f}] (k={s['k']}, papers={s['papers']})"
rowsmd = [('Primary, GenDate only', 'primary_gendate_only'), ('Primary, full model', 'primary_full'),
          ('Drop influential rows', 'drop_influential'), ('Exact variance only', 'exact_variance_only'),
          ('Exclude approximate N', 'exclude_approx_N'), ('Exclude dataset-coded rows', 'exclude_dataset_rows'),
          ('Unequal real/fake counts: balanced accuracy or dropped', 'balanced_base_rate')]
L += ['| Analysis | Audio | Video |', '|---|---|---|']
for lab, key in rowsmd:
    L.append(f"| {lab} | {fmt(out['audio'][key])} | {fmt(out['video'][key])} |")
L.append(f"| Video only (audiovisual removed) | | {fmt(out['video']['video_only_no_av'])} |")
for m in ['audio', 'video']:
    o = out[m]
    L += ['', f'## {m.capitalize()}', '',
          f"- Influential rows (Cook-style, > median + 6×IQR): {', '.join(o['influential_rows']) or 'none'}",
          f"- Leave-one-paper-out GenDate slope range: {o['leave_one_paper_out']['min'][1]:+.2f} (without {o['leave_one_paper_out']['min'][0]}) to {o['leave_one_paper_out']['max'][1]:+.2f} (without {o['leave_one_paper_out']['max'][0]})",
          f"- d′ outcome: " + ('—' if not o['dprime'] else f"{o['dprime']['b']:+.3f} d′/yr [{o['dprime']['lo']:+.3f}, {o['dprime']['hi']:+.3f}] (k={o['dprime']['k']})"),
          f"- H3 year-run slope (full model): {fmt(o['yearrun_H3'])}; with publication year instead: {fmt(o['pubyear_H3'])}",
          f"- Egger/PET (accuracy on SE): b = {o['egger']['b']:+.3f}, p = {o['egger']['p_two']:.3f} (k={o['egger']['k']})",
          f"- One-sided p (full model): " + ', '.join(f"{h} {('n/a' if p is None else f'{p:.3f}')}" for h, p in o['one_sided_p'].items()),
          f"- Holm-adjusted: " + ', '.join(f"{h} {p:.3f}" for h, p in o['holm_p'].items())]
L += ['', '## Half-life of the above-chance margin (secondary)', '', '| Lineage | k | Dates | First release | Margin at first release (pts) | Half-life (years) |', '|---|---|---|---|---|---|']
for k, v in hl.items():
    L.append(f"| {k} | {v['k']} | {v['n_dates']} | {v['first_release']} | {v['margin_at_first']} | {v['half_life_years']} |")
L += ['', 'Not run: ' + '; '.join(out['not_run'])]
open('output/av_sensitivity.md', 'w').write('\n'.join(L) + '\n')
print('\n'.join(L))
