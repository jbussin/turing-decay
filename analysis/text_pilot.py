import numpy as np, pandas as pd
from pathlib import Path
DATA = Path(__file__).resolve().parents[1] / "data"
from scipy import stats

df = pd.read_csv(DATA / "text_pilot.csv")
df["y"] = df.acc - 0.5
df["v"] = df.acc * (1 - df.acc) / df.n

def metareg(d, cols, label):
    y, v = d.y.values, d.v.values
    X = np.column_stack([np.ones(len(d))] + [d[c].values for c in cols])
    k, p = X.shape
    W = np.diag(1 / v)
    A = np.linalg.inv(X.T @ W @ X)
    b = A @ X.T @ W @ y
    Q = float((y - X @ b) @ W @ (y - X @ b))
    P = W - W @ X @ A @ X.T @ W
    tau2 = max(0.0, (Q - (k - p)) / np.trace(P))
    Ws = np.diag(1 / (v + tau2))
    cov = np.linalg.inv(X.T @ Ws @ X)
    b = cov @ X.T @ Ws @ y
    r = y - X @ b
    s2 = float(r @ Ws @ r) / (k - p)
    se = np.sqrt(np.diag(cov) * max(s2, 1))
    pv = 2 * stats.t.sf(np.abs(b / se), k - p)
    print(f"\n== {label}  (k={k}, tau={np.sqrt(tau2):.3f})")
    for name, bi, si, pi in zip(["intercept"] + cols, b, se, pv):
        print(f"  {name:12s} {bi:+.4f}  se {si:.4f}  p={pi:.3f}")

passage = df[(df.paradigm == "passage") & (df.llm_expert == 0)]
metareg(passage, ["gen_date", "intervention"], "Passages, non-LLM-experts: generator clock")
metareg(passage[passage.gen_date > 2020.5], ["gen_date"], "Post-GPT-3 only (is it flat at the floor?)")
metareg(passage, ["pub_year", "intervention"], "Passages: publication year instead")

# GPT-3 paper: same release date, different model size -> capability without time
sizes = pd.DataFrame({
    "params": [125e6, 350e6, 760e6, 1.3e9, 2.7e9, 6.7e9, 13e9, 175e9],
    "acc": [0.76, 0.61, 0.68, 0.62, 0.62, 0.60, 0.55, 0.52]})
s = stats.linregress(np.log10(sizes.params), sizes.acc)
print(f"\n== GPT-3 size ladder (single release): {100*s.slope:+.1f} pts per 10x params, r={s.rvalue:.2f}, p={s.pvalue:.3f}")
print(f"   extrapolated chance crossing at ~{10**((0.5 - s.intercept)/s.slope):.2e} params")

print("\n== Pooled by generator (untrained non-experts, passages)")
for g, sub in passage[passage.intervention == 0].groupby("gen_date"):
    w = 1 / sub.v
    print(f"  {g:.2f} {', '.join(sub.generator.unique()):25s} k={len(sub)} acc={(w*sub.acc).sum()/w.sum():.3f}")
