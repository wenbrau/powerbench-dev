#!/usr/bin/env python3
"""One multilevel logistic model across every PowerBench run, hackathon and current.

WHY THIS MODEL EXISTS. Eighteen runs have each been analysed alone, so we have eighteen separate
estimates of "how much does the power structure matter", each with its own standard error, and the
gaps between them get read as findings when they may be sampling noise. A multilevel model
estimates the shared effect once and estimates each run's departure from it rather than assuming
the departure is zero (complete pooling) or that every run is its own universe (no pooling). That
is McElreath's argument for multilevel models as the default (Statistical Rethinking, ch. 13), and
it is the whole reason to pool.

WHAT LICENSES POOLING. Every coordinate here is ASSIGNED BY US in a factorial design: mode, means,
domain, context, scale, standing, language, nationality, and (in three banks) the writer. Nothing
selected itself into treatment. So the pooled table is a set of randomised experiments sharing a
design skeleton — the runs differ in coverage, not in confounding.

THE ESTIMAND. P(refuse | do(mode)) and P(refuse | do(means)), marginal over the population of
scenarios our banks sample from. Because mode and means are randomised, these are identified with
NO adjustment at all: there is no back-door path into a variable nothing points into. Every
covariate in the model below is therefore in it for PRECISION or for DESCRIPTION, never for
identification. That distinction is what keeps the model honest.

WHAT IS DELIBERATELY NOT IN THE MODEL — each omission is a claim, so each is stated:

  * ask-form, prompt length, harm vocabulary, rated severity. These are POST-TREATMENT: the writer
    chose them after seeing the cell, so they are consequences of mode, not causes of it
    (Rethinking ch. 6.2, post-treatment bias). Conditioning on them answers a different question —
    the direct effect of mode with style held fixed — and biases the total effect. We report that
    direct effect separately in `analyze_d4_means.py` and in the ask-form work, labelled as such.
    The v6 balance rule and the D4 v2 matched pair are the better fix: they delete the
    mode -> style edge in the design instead of trying to subtract it afterwards.
  * writer. In 15 of 18 banks exactly one model wrote the whole bank, so writer is ALIASED with
    dataset — no data can separate them, and a term for both would be unidentified. Writer is
    estimated only where it is genuinely crossed with cells (`writer_contrast` below, on the
    pilot144/gen2/randomwriter banks that share cells).
  * nationality. Present in 5 banks. Putting it in the pooled model would silently drop every row
    without it. It gets its own stratified fit.
  * harmful, premise_reject, resp_len. These are outcomes, not predictors.
  * judge as a varying effect. Two levels only; a variance cannot be learned from two clusters
    (ch. 13). It is index-coded as a fixed offset instead, which is the honest version of "we know
    the eras were graded differently and refuse to difference them without saying so".
  * an interaction of everything with everything. The design supports it, the data do not: with
    one prompt per cell in most banks, high-order interactions are estimated from single
    observations and the posterior would be prior.

PRIORS follow Rethinking ch. 11-13 for logistic models:
  ᾱ ~ Normal(0, 1.5)   — on the logit scale, sd 1.5 puts most mass on refusal rates between about
                          5% and 95%, rather than piling it at 0 and 1 the way a flat prior does.
  β  ~ ZeroSumNormal(0.5) — regularising, and zero-sum so each factor's levels are deviations from
                          the grand mean and the model is identified alongside ᾱ.
  σ  ~ Exponential(1)  — weakly informative on cluster sd; avoids the near-zero funnel that
                          HalfCauchy creates.
All varying effects are non-centered (ch. 13's funnel fix) via ZeroSumNormal's sigma argument.

    python3 4_analysis/bayes_cross_dataset.py --fit         # sample (writes .nc)
    python3 4_analysis/bayes_cross_dataset.py --report      # summarise an existing fit
"""
import argparse
import json
from pathlib import Path

import arviz as az
import numpy as np
import pandas as pd
import pymc as pm

ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "4_analysis/bayes_cross"
OUTDIR.mkdir(exist_ok=True)
RANDOM_SEED = sum(map(ord, "powerbench-cross-dataset"))

MODES = ["harmless_empowerment", "disempowerment", "power_grabbing"]


def load():
    d = pd.read_csv(ROOT / "4_analysis/pooled_runs.csv", low_memory=False)
    d = d[d["mode"].isin(MODES)].copy()
    d["standing"] = d["standing"].fillna("unknown")
    d["means"] = d["means"].fillna("legal")
    d["lang"] = d["lang"].fillna("en")
    d["cell"] = d["domain"].astype(str) + "|" + d["context"].astype(str)
    return d


def build(d):
    fac = {}
    for k in ["target", "cell", "dataset", "mode", "means", "scale", "standing", "lang",
              "judge_era"]:
        c = pd.Categorical(d[k])
        fac[k] = (c.codes.astype("int32"), list(c.categories))
    coords = {k: v[1] for k, v in fac.items()}
    coords["obs"] = np.arange(len(d))

    with pm.Model(coords=coords) as m:
        y = pm.Data("y", d["refuse"].to_numpy().astype("int8"), dims="obs")
        idx = {k: pm.Data(f"i_{k}", v[0], dims="obs") for k, v in fac.items()}

        # grand mean on the logit scale
        a_bar = pm.Normal("a_bar", 0.0, 1.5)

        # --- varying intercepts: partial pooling over clusters (ch. 13) ---
        s_target = pm.Exponential("sigma_target", 1.0)
        s_cell = pm.Exponential("sigma_cell", 1.0)
        s_ds = pm.Exponential("sigma_dataset", 1.0)
        a_target = pm.ZeroSumNormal("a_target", sigma=s_target, dims="target")
        a_cell = pm.ZeroSumNormal("a_cell", sigma=s_cell, dims="cell")
        a_ds = pm.ZeroSumNormal("a_dataset", sigma=s_ds, dims="dataset")

        # --- index-coded design factors: the estimands, deviations from a_bar ---
        b_mode = pm.ZeroSumNormal("b_mode", sigma=0.5, dims="mode")
        b_means = pm.ZeroSumNormal("b_means", sigma=0.5, dims="means")
        b_scale = pm.ZeroSumNormal("b_scale", sigma=0.5, dims="scale")
        b_stand = pm.ZeroSumNormal("b_standing", sigma=0.5, dims="standing")
        b_lang = pm.ZeroSumNormal("b_lang", sigma=0.5, dims="lang")
        b_judge = pm.ZeroSumNormal("b_judge", sigma=0.5, dims="judge_era")

        # --- varying slopes: does the mode effect differ BY TARGET? (ch. 14) ---
        # zero-sum on both axes so it is a pure interaction, not a second copy of the main effects.
        s_tm = pm.Exponential("sigma_target_mode", 1.0)
        g_tm = pm.ZeroSumNormal("g_target_mode", sigma=s_tm, dims=("target", "mode"),
                                n_zerosum_axes=2)

        eta = (a_bar
               + a_target[idx["target"]] + a_cell[idx["cell"]] + a_ds[idx["dataset"]]
               + b_mode[idx["mode"]] + b_means[idx["means"]] + b_scale[idx["scale"]]
               + b_stand[idx["standing"]] + b_lang[idx["lang"]] + b_judge[idx["judge_era"]]
               + g_tm[idx["target"], idx["mode"]])
        pm.Bernoulli("refuse_obs", logit_p=eta, observed=y, dims="obs")
    return m, coords


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fit", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--draws", type=int, default=1000)
    ap.add_argument("--tune", type=int, default=1000)
    a = ap.parse_args()
    d = load()
    nc = OUTDIR / "inference_data.nc"

    if a.fit or not nc.exists():
        rng = np.random.default_rng(RANDOM_SEED)
        m, coords = build(d)
        with m:
            # prior predictive: do the priors imply believable refusal rates before seeing data?
            pri = pm.sample_prior_predictive(draws=400, random_seed=rng)
            pr = pri.prior_predictive["refuse_obs"].mean(dim="obs").to_numpy().ravel()
            print(f"prior predictive refusal rate: media {pr.mean():.2f}, "
                  f"2.5–97.5% [{np.quantile(pr,0.025):.2f}, {np.quantile(pr,0.975):.2f}] "
                  f"(quiere cubrir 0–1 sin apilarse en los extremos)")
            idata = pm.sample(draws=a.draws, tune=a.tune, nuts_sampler="nutpie",
                              target_accept=0.9, random_seed=rng)
            idata.extend(pri)
            idata.extend(pm.sample_posterior_predictive(idata, random_seed=rng))
            pm.compute_log_likelihood(idata, model=m)
        idata.to_netcdf(str(nc))
        print(f"-> {nc}")
    else:
        idata = az.from_netcdf(str(nc))

    # ---------- diagnostics ----------
    summ = az.summary(idata, var_names=["a_bar", "b_mode", "b_means", "b_scale", "b_standing",
                                        "b_lang", "b_judge", "sigma_target", "sigma_cell",
                                        "sigma_dataset", "sigma_target_mode"])
    print("\n", summ.to_string())
    bad_r = float(summ["r_hat"].max())
    min_ess = float(summ["ess_bulk"].min())
    div = int(idata.sample_stats["diverging"].sum()) if "diverging" in idata.sample_stats else -1
    print(f"\nmax R-hat {bad_r:.4f} | min ESS {min_ess:.0f} | divergencias {div}")

    post = idata.posterior
    R = {"n_rows": int(len(d)), "max_rhat": bad_r, "min_ess": min_ess, "divergences": div}

    # ---------- contrasts on the log-odds scale (differences of index levels) ----------
    def contrast(var, hi, lo, dim):
        v = post[var]
        x = (v.sel({dim: hi}) - v.sel({dim: lo})).to_numpy().ravel()
        return {"or": float(np.exp(x.mean())),
                "hdi": [float(np.exp(q)) for q in az.hdi(x, hdi_prob=0.94)],
                "p_gt_0": float((x > 0).mean())}

    R["grab_vs_harmless"] = contrast("b_mode", "power_grabbing", "harmless_empowerment", "mode")
    R["grab_vs_disemp"] = contrast("b_mode", "power_grabbing", "disempowerment", "mode")
    R["disemp_vs_harmless"] = contrast("b_mode", "disempowerment", "harmless_empowerment", "mode")
    means_levels = list(post.coords["means"].values)
    for hi in [x for x in means_levels if x != "legal"]:
        R[f"means_{hi}_vs_legal"] = contrast("b_means", hi, "legal", "means")
    if "society" in list(post.coords["scale"].values):
        R["scale_society_vs_individual"] = contrast("b_scale", "society", "individual", "scale")
    R["judge_binary_vs_legacy"] = contrast("b_judge", "binary", "legacy3class", "judge_era")

    # ---------- variance decomposition: where does refusal variation LIVE? ----------
    # sd of each factor's level-effects, on the log-odds scale. This is the question no single run
    # can answer: is a refusal decision mostly about the request, or mostly about who is answering?
    comp = {}
    for var, dim in [("b_mode", "mode"), ("b_means", "means"), ("b_scale", "scale"),
                     ("b_standing", "standing"), ("b_lang", "lang"), ("b_judge", "judge_era"),
                     ("a_target", "target"), ("a_cell", "cell"), ("a_dataset", "dataset")]:
        x = post[var].std(dim=dim).to_numpy().ravel()
        comp[var] = {"sd_logodds": float(x.mean()),
                     "hdi": [float(q) for q in az.hdi(x, hdi_prob=0.94)]}
    x = post["g_target_mode"].std(dim=("target", "mode")).to_numpy().ravel()
    comp["g_target_mode"] = {"sd_logodds": float(x.mean()),
                             "hdi": [float(q) for q in az.hdi(x, hdi_prob=0.94)]}
    R["variance_components"] = comp

    # ---------- per-target discrimination (grab - harmless), with shrinkage ----------
    disc = {}
    for t in list(post.coords["target"].values):
        x = ((post["b_mode"].sel(mode="power_grabbing")
              + post["g_target_mode"].sel(target=t, mode="power_grabbing"))
             - (post["b_mode"].sel(mode="harmless_empowerment")
                + post["g_target_mode"].sel(target=t, mode="harmless_empowerment"))
             ).to_numpy().ravel()
        disc[str(t)] = {"or": float(np.exp(x.mean())),
                        "hdi": [float(np.exp(q)) for q in az.hdi(x, hdi_prob=0.94)],
                        "p_gt_0": float((x > 0).mean())}
    R["discrimination_by_target"] = dict(sorted(disc.items(), key=lambda kv: -kv[1]["or"]))

    (OUTDIR / "cross_dataset.json").write_text(json.dumps(R, indent=1))
    print(f"\n-> {(OUTDIR / 'cross_dataset.json').relative_to(ROOT)}")
    print("\ncontrastes (odds ratio, HDI 94%):")
    for k in ["grab_vs_harmless", "grab_vs_disemp", "disemp_vs_harmless",
              "judge_binary_vs_legacy"]:
        v = R[k]
        print(f"  {k:26s} OR {v['or']:6.2f}  [{v['hdi'][0]:.2f}, {v['hdi'][1]:.2f}]  "
              f"P(>0)={v['p_gt_0']:.3f}")
    for k in R:
        if k.startswith("means_"):
            v = R[k]
            print(f"  {k:26s} OR {v['or']:6.2f}  [{v['hdi'][0]:.2f}, {v['hdi'][1]:.2f}]  "
                  f"P(>0)={v['p_gt_0']:.3f}")
    print("\ndónde vive la variación (sd en log-odds; más alto = más importa):")
    for k, v in sorted(comp.items(), key=lambda kv: -kv[1]["sd_logodds"]):
        print(f"  {k:18s} {v['sd_logodds']:5.2f}  [{v['hdi'][0]:.2f}, {v['hdi'][1]:.2f}]")


if __name__ == "__main__":
    main()
