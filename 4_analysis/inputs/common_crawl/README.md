# Frozen Common Crawl language statistics

- Source: [official language-count CSV](https://commoncrawl.github.io/cc-crawl-statistics/plots/languages.csv).
- Methodology: [Common Crawl language statistics](https://commoncrawl.github.io/cc-crawl-statistics/plots/languages).
- Selected snapshot: **CC-MAIN-2026-34**, latest listed at selection, before calculating associations.
- `languages.csv` is the complete source download, including other snapshots. `source.json` records retrieval time, source URLs, selected crawl, and SHA-256 checksum.
- `pbanalysis/language_resource.py` selects one snapshot and checks the checksum. Shares use page counts and the total across all primary-language categories, including unknown; the eight study languages are not renormalized to sum to 100%.
- Common Crawl identifies primary language on HTML pages using CLD2. Page shares are a web-availability proxy. They do not describe any benchmarked model's actual training mixture.

The main Figure 2 script reads this frozen local copy and makes no network requests. Updating the source requires an explicit provenance update and analysis rerun.
