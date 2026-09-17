"""Extract saved results for the author guide; does not recompute inference.

Run from any directory with the repository's Python environment.
Use --check to verify that generated files still match their sources.
"""

import argparse
import hashlib
import json
from pathlib import Path

import pandas as pd


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RESULTS = ROOT / "4_analysis/results"
MARKER = "<!-- GENERATED_EVIDENCE -->"
FOLDERS = ["19_d1_final", "20_d1_languages_final", "21_d2_nationality_final", "22_d3_ai_final"]
MODES = {"he": "Self-empowerment", "de": "Disempowerment", "pg": "Power grabbing", "control": "Control"}
LANGS = {"es": "Spanish", "pt": "Portuguese", "fr": "French", "de": "German", "zh": "Chinese", "hi": "Hindi", "sw": "Swahili"}
SWAPS = {"us_ally": "US / US ally", "us_rival": "US / US rival", "us_neutral": "US / neutral", "cn_ally": "China / China ally", "cn_rival": "China / China rival", "cn_neutral": "China / neutral", "us_cn": "US / China", "allies": "US ally / China ally", "neutrals": "Neutral A / neutral B"}

PURPOSES = {
    "refusal_by_model": "Main Figure 1 source: model variation and mode levels",
    "scale_by_mode": "Main Figure 1 source: scale association across modes",
    "standing_by_mode": "Appendix: initial standing; PG contrast uncertain",
    "context_by_mode": "Appendix: descriptive context breakdown",
    "domain_by_mode": "Appendix: descriptive domain breakdown",
    "trigger_by_mode": "Appendix: heterogeneity in the separate control bank",
    "control_correlations": "Appendix: model-level association, not mechanism",
    "capability_vs_refusal": "Appendix: small fixed-panel capability association",
    "harm_among_nonrefusals": "Withhold from main claims: weak harmfulness validation, selected denominator",
    "language_levels": "Appendix: absolute levels behind paired language changes",
    "language_vs_english": "Main Figure 2 source: all seven reference contrasts",
    "model_language_differences": "Appendix: variation within each model group",
    "model_directional_bias": "Appendix: direction conditional on discordant pairs",
    "language_pair_differences": "Appendix: contrasts beyond the English reference",
    "language_pair_direction": "Appendix: pairwise direction among changed decisions",
    "language_by_scale": "Appendix: exploratory language-by-scale breakdown",
    "language_by_standing": "Appendix: exploratory language-by-standing breakdown",
    "language_range": "Appendix: descriptive extremes; sensitive to outliers and truncation",
    "truncation_by_language": "Essential supporting audit: response-cap differences",
    "common_crawl_vs_language_bias": "Exploratory appendix: web representation, not training exposure",
    "common_crawl_model_slopes": "Exploratory appendix: model-specific proxy associations",
    "paired_effects": "Main figure source: paired group changes with uncertainty",
    "model_effects": "Model heterogeneity; compact PG panel if space permits",
    "discordant_direction": "Appendix: changed-pair direction and denominators",
    "effects_by_scale": "Appendix: exploratory paired changes by scale",
    "effects_by_standing": "Appendix: exploratory paired changes by standing",
    "human_ai_levels": "Main Figure 4 companion or appendix: matched absolute rates",
}


def main(check=False):
    evidence = {"description": "Saved output extraction, not a new statistical analysis", "sources": {}, "tables": {}}

    def source(relative):
        path = RESULTS / relative
        evidence["sources"][str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
        return path

    def read(relative, **filters):
        frame = pd.read_csv(source(relative))
        for key, value in filters.items():
            frame = frame[frame[key].eq(value)]
        evidence["tables"][relative + (" " + json.dumps(filters, sort_keys=True) if filters else "")] = {
            "source": str((RESULTS / relative).relative_to(ROOT)),
            "filters": filters,
            "rows": json.loads(frame.to_json(orient="records", double_precision=15)),
        }
        return frame

    baseline = read(FOLDERS[0] + "/panel_rates.csv", bloc="all")
    factors = read(FOLDERS[0] + "/scale_standing_contrasts.csv", bloc="all", mode="pg")
    model_baseline = read(FOLDERS[0] + "/per_model_rates.csv", mode="pg")
    languages = read(FOLDERS[1] + "/language_vs_english_panel.csv")
    lang_audit = read(FOLDERS[1] + "/language_data_audit.csv")
    read(FOLDERS[1] + "/truncation_sensitivity.csv", lang="sw", mode="pg")
    read(FOLDERS[1] + "/resource_associations.csv")
    nationality = read(FOLDERS[2] + "/paired_pooled.csv", bloc="all", mode="pg")
    national_groups = read(FOLDERS[2] + "/us_minus_cn_effect.csv", mode="pg")
    national_models = read(FOLDERS[2] + "/paired_per_model.csv")
    ai = read(FOLDERS[3] + "/paired_pooled.csv")
    ai_groups = read(FOLDERS[3] + "/us_minus_cn_effect.csv", mode="pg")
    ai_models = read(FOLDERS[3] + "/paired_per_model.csv", mode="pg")
    read(FOLDERS[3] + "/audit_between_mode_differences.csv", bloc="all")
    read(FOLDERS[3] + "/sensitivity_no_truncation.csv")

    counts = {}
    for label, relative, filters in [
        ("D1_all_languages", FOLDERS[1] + "/data_audit.csv", {}),
        ("D2_nationality", FOLDERS[2] + "/data_audit.csv", {}),
        ("D3_AI_only", FOLDERS[3] + "/data_audit.csv", {"condition": "ai"}),
    ]:
        frame = read(relative, **filters)
        counts[label] = {col: int(frame[col].sum()) for col in ["rows", "valid"]}
    counts["total_unique"] = {col: sum(x[col] for x in counts.values()) for col in ["rows", "valid"]}
    assert counts["total_unique"] == {"rows": 495936, "valid": 495807}, "Revisit manuscript counts"
    evidence["counts"] = counts

    # Guard the manuscript's central categorical summaries against stale prose.
    assert len(languages) == 84 and len(national_models) == 864 and len(ai_models) == 24
    assert set(nationality.loc[nationality.q.lt(.05), "contrast"]) == {"us_neutral", "cn_ally", "cn_neutral"}
    assert national_groups.q.ge(.05).all()
    discoveries = national_models[national_models.q.lt(.05)]
    assert len(discoveries) == 19 and discoveries.model.eq("nova-2-lite").sum() == 15
    assert ai_models.estimate.gt(0).sum() == 22 and ai_models.q.lt(.05).sum() == 11
    assert set(languages.loc[languages.bloc.eq("all") & languages['mode'].eq("pg") & languages.q.lt(.05), "lang"]) == {"fr", "hi", "sw"}
    assert ai_groups.iloc[0].lo < 0 < ai_groups.iloc[0].hi
    evidence["discovery_counts"] = {"nationality_all_modes": len(discoveries), "nationality_nova": int(discoveries.model.eq("nova-2-lite").sum()), "nationality_pg": int(discoveries['mode'].eq("pg").sum()), "ai_pg_positive": int(ai_models.estimate.gt(0).sum()), "ai_pg_adjusted": int(ai_models.q.lt(.05).sum())}

    def interval(row, signed=True):
        f = "+.1f" if signed else ".1f"
        return f"{row.estimate:{f}} [{row.lo:{f}}, {row.hi:{f}}]"

    def table(headers, rows):
        return "\n".join(["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"] + ["| " + " | ".join(map(str, row)) + " |" for row in rows])

    sections = ["### English baseline: refusal percentage, 95% interval\n", table(["Category", "Rate [95% CI]"], [[MODES[row['mode']], interval(row, False)] for _, row in baseline.iterrows()]), "\n### Baseline power-grabbing factor contrasts: percentage points\n", table(["Comparison", "Change [95% CI]", "Adjusted q"], [[row.comparison, interval(row), f"{row.q:.4f}"] for _, row in factors.iterrows()])]
    pg_lang = languages[languages['mode'].eq('pg')]
    lang_rows = []
    for lang, name in LANGS.items():
        cells = pg_lang[pg_lang.lang.eq(lang)].set_index("bloc")
        lang_rows.append([name] + [interval(cells.loc[bloc]) for bloc in ['all', 'US', 'CN']] + [f"{cells.loc['all', 'q']:.4f}"])
    sections += ["\n### Language minus English, power grabbing: percentage points\n", table(["Language", "All [95% CI]", "US [95% CI]", "China [95% CI]", "Pooled q"], lang_rows)]
    sections += ["\n### Nationality swaps, pooled power grabbing: percentage points\n", table(["A / B", "Swap change [95% CI]", "Adjusted q"], [[SWAPS[row.contrast], interval(row), f"{row.q:.4f}"] for _, row in nationality.iterrows()])]
    ai_rows = []
    for mode, name in MODES.items():
        cells = ai[ai['mode'].eq(mode)].set_index("bloc")
        ai_rows.append([name] + [interval(cells.loc[bloc]) for bloc in ['all', 'US', 'CN']])
    sections += ["\n### AI minus human: percentage points\n", table(["Category", "All [95% CI]", "US [95% CI]", "China [95% CI]"], ai_rows)]
    sections += ["\n### Truncation by language\n", table(["Language", "Truncated / rows", "Percent"], [[row.lang, f"{row.truncated:,} / {row.rows:,}", f"{row.truncated_pct:.2f}%"] for _, row in lang_audit.iterrows()])]

    inventory = []
    for block, folder in enumerate(FOLDERS, 1):
        meta = json.loads(source(folder + "/meta.json").read_text())
        for figure in meta['figures']:
            assert (RESULTS / folder / (figure + '.png')).is_file()
            inventory.append({"block": block, "figure": figure, "path": f"4_analysis/results/{folder}/{figure}.png", "role": PURPOSES[figure]})
    assert len(inventory) == 32
    evidence['figure_inventory'] = inventory
    sections += ["\n### All 32 existing plots and their proposed paper roles\n", table(["Block", "Plot", "Proposed role"], [[item['block'], f"[{item['figure']}](../../{item['path']})", item['role']] for item in inventory])]

    guide = HERE / "READING_GUIDE.md"
    prefix = guide.read_text().split(MARKER)[0]
    rendered = prefix + MARKER + "\n\n" + "\n\n".join(sections) + "\n"
    payload = json.dumps(evidence, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    outputs = {guide: rendered, HERE / "evidence.json": payload}
    for path, contents in outputs.items():
        if check:
            assert path.read_text() == contents, f"Stale generated output: {path}"
        else:
            path.write_text(contents)
    print(f"{'Verified' if check else 'Extracted'} {len(evidence['sources'])} sources, {len(inventory)} plots, and unique collection counts.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    main(parser.parse_args().check)
