# Bibliography audit, group 2: policy documents, ChatGPT usage, statistics, capability benchmarks

Auditor: Claude (agent), 2026-09-23. Protocol: `paper/iclr2027/bibliography/AUDIT_INSTRUCTIONS.md`.
References: `anthropic2026constitution`, `openai2025modelspec`, `chatterji2025chatgpt`, `bates2015lme4`,
`benjamini1995fdr`, `mcnemar1947`, `rein2023gpqa`, `wang2024mmlupro`.

Downloads are in `paper/iclr2027/bibliography/pdfs/` (git-ignored): `anthropic2026constitution.{html,txt}`
(+ `_announcement.html`), `openai2025modelspec.{html,txt}` (+ `_rev2026-08-18.txt`), `chatterji2025chatgpt.pdf`,
`bates2015lme4.pdf`, `benjamini1995fdr.pdf` (JSTOR scan, author's site), `mcnemar1947_landing.html` +
`mcnemar1947_crossref.json` (the full text is paywalled, see below), `rein2023gpqa.pdf`, `wang2024mmlupro.pdf`
(NeurIPS proceedings version), and two candidate additions: `extra_fagerland2013mcnemar.pdf`,
`extra_benjamini2001yekutieli_crossref.json`.

---

## anthropic2026constitution

- **Verified at:** https://www.anthropic.com/constitution (full text, fetched 2026-09-23);
  https://www.anthropic.com/news/claude-new-constitution (announcement, dated "Jan 22, 2026").
- **Metadata verdict: OK** (one optional MINOR improvement). The title "Claude's Constitution" and corporate author Anthropic
  are right. The year 2026 is right: the announcement is dated 22 January 2026, and the page footer reads "© 2026 Anthropic PBC".
  The URL works. Anthropic does not call the document a "policy document". The page also says it "is likely to change in
  important ways in the future", so a publication date helps. Optional entry:
  ```bibtex
  @misc{anthropic2026constitution,
    title  = {Claude's Constitution},
    author = {{Anthropic}},
    year   = {2026},
    month  = jan,
    note   = {Published 22 January 2026},
    url    = {https://www.anthropic.com/constitution}
  }
  ```
- **Uses in the paper:**
  1. Introduction: "developers state that their models should not help concentrate power illegitimately
     \citep{anthropic2026constitution}". **SUPPORTS.** In section "Preserving important societal structures" →
     "Avoiding problematic concentrations of power", the document says Claude "should refuse to assist with actions that
     would help concentrate power in illegitimate ways". The hard-constraints list also includes never assisting
     "an attempt to seize unprecedented and illegitimate degrees of absolute societal, military, or economic control".
  2. Appendix: "developers' own policies prohibit assisting the illegitimate concentration of power". **SUPPORTS**, with a
     slight nuance. The document is an outright prohibition only for flagrant cases (the hard constraint). For other cases it
     asks for judgment on legitimacy (process, accountability, transparency). "Prohibit" is still fair given the "should refuse"
     sentence above. No change needed.
  - Useful point for the authors, not a citation problem: the same section says that "normal political, economic, and
    social life involves seeking legitimate power and advantage in myriad ways". This sits well with treating refusal of
    harmless empowerment as over-refusal. If the paper wants a developer statement for that, this passage is one.
- **Better or additional citations:** none needed. This is the primary source.

## openai2025modelspec

- **Verified at:** https://model-spec.openai.com/2025-12-18.html (page title "Model Spec (2025/12/18)");
  https://model-spec.openai.com/ (redirects to `2026-08-18.html`); https://model-spec.openai.com/2026-08-18.html;
  https://github.com/openai/model_spec (commit log via GitHub API; `CHANGELOG.md`).
- **Metadata verdict: OK.** We cite the "Revision of 18 December 2025", and that revision exists (GitHub commit "Release
  2025-12-18", CHANGELOG entry v2025.12.18). Year 2025 is correct for that revision. Title "Model Spec" and author OpenAI
  are correct.
  - **Note: a newer revision exists.** `v2026.08.18` ("Release 2026-08-18", 17 Aug 2026) is now the current version, and the
    site root redirects to it. A March 2026 commit added "a banner notifying visitors that they are viewing an outdated
    version" to older revisions, so a reviewer who follows our link may see that banner. The sentence we rely on is word for
    word the same in both revisions. The red-line principles section was introduced in v2025.09.12. Keeping the December
    2025 revision is correct. Optionally, cite the revision that was current while the experiments ran (Aug–Sep 2026). The
    bibkey can stay as it is:
    ```bibtex
    @misc{openai2025modelspec,
      title        = {Model Spec},
      author       = {{OpenAI}},
      howpublished = {Revision of 18 August 2026},
      year         = {2026},
      url          = {https://model-spec.openai.com/2026-08-18.html}
    }
    ```
- **Uses in the paper:**
  1. Introduction: "...or erode civic participation \citep{openai2025modelspec}". **SUPPORTS.** In the Overview →
     "Red-line principles" section, OpenAI commits to principles "across all deployments of our models", including: "We will
     not allow our models to be used for ... eroding participation in civic processes".
  2. Appendix: "developers' own policies prohibit assisting ... the erosion of civic participation". **SUPPORTS**, same
     passage.
  - Caution: the Model Spec says **nothing** about power concentration. It also has no "democratic processes" wording:
    "democra" appears only in a Tiananmen example. The nearest other passage is the root-level rule "Don't facilitate the
    targeted manipulation of political views". The paper's current wording ("civic participation") is exactly right. Do not
    change it to "undermine democratic processes" or "concentrate power" with this citation.
- **Better or additional citations:** none. This is the primary source.

## chatterji2025chatgpt

- **Verified at:** https://www.nber.org/papers/w34255 (citation meta tags); PDF
  https://www.nber.org/system/files/working_papers/w34255/w34255.pdf; SSRN listing
  https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5487080 (from search results). No journal version was found.
- **Metadata verdict: OK** (optional MINOR additions). Title "How People Use ChatGPT", NBER Working Paper 34255, September
  2025. The seven authors are in the right order. NBER spells them "David J. Deming", "Zoe Hitzig" (no diaeresis) and
  "Carl Yan Shan". SSRN spells them "David Deming", "Zoë Hitzig" and "Carl Shan", so our forms are acceptable. DOI 10.3386/w34255
  (NBER meta tag). Optional entry matching NBER exactly:
  ```bibtex
  @techreport{chatterji2025chatgpt,
    title       = {How People Use {ChatGPT}},
    author      = {Chatterji, Aaron and Cunningham, Thomas and Deming, David J. and Hitzig, Zoe and Ong, Christopher and Shan, Carl Yan and Wadman, Kevin},
    institution = {National Bureau of Economic Research},
    type        = {Working Paper},
    number      = {34255},
    year        = {2025},
    month       = sep,
    doi         = {10.3386/w34255},
    url         = {https://www.nber.org/papers/w34255}
  }
  ```
- **Uses in the paper:**
  1. Introduction: "People increasingly use language-model assistants to ask for practical guidance, one of the most common
     uses of these systems \citep{chatterji2025chatgpt}." **SUPPORTS**, with a small nuance.
     - The Introduction (p. 2) says "Practical Guidance is the most common use case", covering tutoring and teaching,
       how-to advice and creative ideation. §5 (p. 14) says it "has remained constant at roughly 29% of overall usage". The
       abstract and Conclusion say Practical Guidance, Seeking Information and Writing are the three most common topics
       (~78–80% of messages).
     - "Increasingly" holds in absolute terms. ChatGPT reached about 10% of the world's adults by July 2025, and "Asking is
       growing faster than Doing" (Introduction). But Practical Guidance's *share* is flat, not rising.
     - The evidence covers **ChatGPT consumer messages only**. The paper itself contrasts its findings with Claude, where
       coding dominates (Handa et al. 2025, cited in their §1). So "these systems" slightly generalizes.
     - Optional wording that stays close to ours: "People increasingly use language-model assistants for practical guidance,
       the most common topic of ChatGPT conversations \citep{chatterji2025chatgpt}."
- **Better or additional citations:** none. This is the largest representative, primary study of assistant usage. Other
  providers' reports (e.g., on Claude) show a different mix of uses, so adding one would weaken rather than support the
  generalization.

## bates2015lme4

- **Verified at:** https://www.jstatsoft.org/article/view/v067i01 (meta tags; JSS BibTeX export);
  https://api.crossref.org/works/10.18637/jss.v067.i01; https://cran.r-project.org/web/packages/lme4/citation.html (the
  package's official citation); PDF https://www.jstatsoft.org/index.php/jss/article/download/v067i01/946.
- **Metadata verdict: OK.** J. Stat. Softw. 67(1), pp. 1–48, October 2015, doi:10.18637/jss.v067.i01. The authors are Bates,
  Mächler, Bolker and Walker. The title is "Fitting Linear Mixed-Effects Models Using lme4". Our entry is identical to the
  BibTeX that CRAN's `citation("lme4")` gives, apart from the DOI, which is optional: `doi = {10.18637/jss.v067.i01}`. The
  version stated in the appendix, lme4 2.0-6, exists on CRAN (published 2026-07-16).
- **Uses in the paper:**
  1. Methods: "binomial generalized linear mixed model \citep[GLMM, fitted with \texttt{lme4};][]{bates2015lme4}".
     **SUPPORTS** as the software citation. The paper says lme4 "provides functions to fit and analyze linear mixed models,
     generalized linear mixed models..." (§1). It then states that "in this paper we restrict ourselves to linear mixed
     models" (p. 2). It is still the citation the lme4 authors ask for when `glmer` is used, so no change is needed.
  2. Appendix: "fitted with \texttt{lme4::glmer} \citep{bates2015lme4} ... with the Laplace approximation replaced by the
     penalized quasi-likelihood starting fit (nAGQ = 0), the bobyqa optimizer ..., uncorrelated random slopes (the
     \texttt{||} syntax)". **SUPPORTS** the citation. The `||` syntax is in the paper's §2.2 and Table 2 ("use double-bar
     notation, (x || g)"), and BOBYQA is discussed in §4 ("Nonlinear optimization module").
     - **Inaccurate wording, not a citation problem.** lme4 does not describe nAGQ = 0 as penalized quasi-likelihood (PQL).
       Its manual (`man/glmer.Rd`) says nAGQ = 0 "uses a faster but less exact form of parameter estimation for GLMMs by
       optimizing the random effects and the fixed-effects coefficients in the penalized iteratively reweighted least squares
       step". It is also the first of glmer's two default optimization stages, which is why "starting fit" is right. PQL
       (Breslow–Clayton) is a different algorithm, and a statistically literate reviewer may flag the term.
     - Suggested wording: "...with nAGQ = 0 (the fixed effects are estimated within the penalized iteratively reweighted
       least squares step, lme4's fast first-stage fit, instead of by the Laplace approximation)".
- **Better or additional citations:** none.

## benjamini1995fdr

- **Verified at:** https://api.crossref.org/works/10.1111/j.2517-6161.1995.tb02031.x; the scanned article (JSTOR copy) at
  https://www.math.tau.ac.il/~ybenja/MyPapers/benjamini_hochberg1995.pdf. Its first page reads "J. R. Statist. Soc. B (1995)
  57, No. 1, pp. 289-300".
- **Metadata verdict: MINOR.** The title, authors, volume, number, pages and year are all correct. The journal was titled
  *Journal of the Royal Statistical Society. Series B (Methodological)* in 1995, according to the JSTOR cover page; Crossref
  now gives the current name "... Series B: Statistical Methodology". Corrected entry:
  ```bibtex
  @article{benjamini1995fdr,
    title   = {Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing},
    author  = {Benjamini, Yoav and Hochberg, Yosef},
    journal = {Journal of the Royal Statistical Society: Series B (Methodological)},
    volume  = {57},
    number  = {1},
    pages   = {289--300},
    year    = {1995},
    doi     = {10.1111/j.2517-6161.1995.tb02031.x}
  }
  ```
- **Uses in the paper:**
  1. Methods: "We correct for multiple comparisons with the Benjamini--Hochberg (BH) procedure \citep{benjamini1995fdr}
     within the families ...". **SUPPORTS.** The Summary presents "a simple sequential Bonferroni-type procedure" that "is
     proved to control the false discovery rate for independent test statistics" (p. 289).
     - Optional clarity point: "q" here means BH-adjusted p-values. Saying "BH-adjusted p-values ($q$)" once avoids confusion
       with Storey's q-value.
- **Better or additional citations:**
  - **ADD (optional, appendix): Benjamini & Yekutieli (2001).** The 1995 proof assumes independent test statistics. Our tests
    within a family are not independent: the same 24 models, and often the same prompts, feed every test. Benjamini &
    Yekutieli prove that BH still controls the FDR under "positive regression dependency" (verified on Project Euclid,
    abstract, and in Crossref). One clause in the appendix's statistics paragraph would pre-empt a reviewer's question:
    ```bibtex
    @article{benjamini2001dependency,
      title   = {The Control of the False Discovery Rate in Multiple Testing under Dependency},
      author  = {Benjamini, Yoav and Yekutieli, Daniel},
      journal = {The Annals of Statistics},
      volume  = {29},
      number  = {4},
      pages   = {1165--1188},
      year    = {2001},
      doi     = {10.1214/aos/1013699998}
    }
    ```
    Sources: https://api.crossref.org/works/10.1214/aos/1013699998;
    https://projecteuclid.org/journals/annals-of-statistics/volume-29/issue-4/The-control-of-the-false-discovery-rate-in-multiple-testing-under/10.1214/aos/1013699998.full

## mcnemar1947

- **Verified at:** https://doi.org/10.1007/BF02295996, which resolves to Cambridge Core (Psychometrika's current publisher):
  Psychometrika 12(2), June 1947, pp. 153–157. Also https://api.crossref.org/works/10.1007/BF02295996. The full text is
  paywalled: Cambridge Core returns the landing page, Springer's PDF link redirects to a login page, and Semantic Scholar
  lists it as CLOSED. **I could read only the abstract.** It says that "Two formulas are presented for judging the
  significance of the difference between correlated proportions" and that "The chi square equivalent of one of the developed
  formulas is pointed out". The standard content of McNemar's test was checked in Fagerland et al. (2013, open access, below),
  which cites McNemar (1947) as its ref. [7].
- **Metadata verdict: OK.** Title, author, journal, volume, issue, pages and year match Crossref and Cambridge Core. Optional:
  `doi = {10.1007/BF02295996}`.
- **Uses in the paper:**
  1. Methods: "we measure bias as the \emph{direction of disagreement}, $(b-c)/(b+c)$, where $b$ and $c$ count the prompts
     whose verdict moves toward and away from refusal in the manipulated condition \citep{mcnemar1947}". **PARTIAL.**
     - **Why McNemar fits:** McNemar's test is the canonical analysis of paired binary outcomes. It uses only the discordant
       pairs b and c: z = (b − c)/√(b + c), or χ² = (b − c)²/(b + c). Its exact form treats b as Binomial(b + c, ½) under the
       null (Fagerland et al. 2013, "Methods", p. 2–3), which is exactly the chance model in our appendix.
     - **What is off:** the normalized index (b − c)/(b + c) is not McNemar's statistic. As far as can be checked, it is not
       defined in the 1947 note. As written, the sentence reads as if the measure itself were McNemar's.
     - **Is there a better attribution?** Mathematically, (b − c)/(b + c) = (b/c − 1)/(b/c + 1). That is Yule's Q applied to
       the matched-pairs (conditional) odds ratio b/c, or equivalently 2·b/(b+c) − 1, a rescaled sign-test proportion. No
       single source defines it under our name, so McNemar remains the most defensible citation. The wording should credit
       McNemar for the discordant-pair framework, not for the index.
     - Suggested wording: "...we measure bias as the \emph{direction of disagreement}, $(b-c)/(b+c)$, where $b$ and $c$
       count the prompts whose verdict moves toward and away from refusal in the manipulated condition, the discordant pairs
       on which McNemar's test for paired proportions is built \citep{mcnemar1947}; it ranges from ..."
- **Better or additional citations:**
  - Keep McNemar. It is the canonical source for the discordant-pair analysis.
  - **ADD (optional, appendix, where the chance expectation "b ~ Binomial(b+c, ½)" is defined):** Fagerland, Lydersen & Laake
    (2013). In §Methods ("The asymptotic McNemar test", p. 2), it states that, conditionally on the discordant pairs, "n12 is
    binomially distributed with parameters n = n12 + n21 and p = 1/2 under the null hypothesis". On p. 3 it builds the exact
    conditional test on that distribution. Metadata from Crossref,
    https://api.crossref.org/works/10.1186/1471-2288-13-91; PDF read at
    https://bmcmedresmethodol.biomedcentral.com/counter/pdf/10.1186/1471-2288-13-91.pdf.
    ```bibtex
    @article{fagerland2013mcnemar,
      title   = {The {McNemar} Test for Binary Matched-Pairs Data: Mid-p and Asymptotic Are Better than Exact Conditional},
      author  = {Fagerland, Morten W. and Lydersen, Stian and Laake, Petter},
      journal = {BMC Medical Research Methodology},
      volume  = {13},
      pages   = {91},
      year    = {2013},
      doi     = {10.1186/1471-2288-13-91}
    }
    ```

## rein2023gpqa

- **Verified at:** https://arxiv.org/abs/2311.12022 (arXiv API: v1 only, 20 Nov 2023, same 8 authors);
  https://colmweb.org/2024/AcceptedPapers.html (official COLM 2024 list: "🔦 Spotlight — GPQA: A Graduate-Level Google-Proof
  Q&A Benchmark", same 8 authors, linking https://openreview.net/forum?id=Ti67584b98);
  https://github.com/idavidrein/gpqa (README BibTeX: `booktitle={First Conference on Language Modeling}, year={2024}`). I did
  not open OpenReview itself, because it serves a CAPTCHA.
- **Metadata verdict: MINOR (outdated venue).** The title and author list, in order, are correct. The entry cites the arXiv
  preprint, but the paper was **published at COLM 2024 (First Conference on Language Modeling), as a Spotlight**. Our other
  entries cite peer-reviewed versions where they exist, so this one should too. The bibkey can stay:
  ```bibtex
  @inproceedings{rein2023gpqa,
    title     = {{GPQA}: A Graduate-Level {G}oogle-Proof {Q\&A} Benchmark},
    author    = {Rein, David and Hou, Betty Li and Stickland, Asa Cooper and Petty, Jackson and Pang, Richard Yuanzhe and Dirani, Julien and Michael, Julian and Bowman, Samuel R.},
    booktitle = {Conference on Language Modeling (COLM)},
    year      = {2024},
    url       = {https://openreview.net/forum?id=Ti67584b98}
  }
  ```
  The in-text citation will change from "Rein et al., 2023" to "Rein et al., 2024".
- **Uses in the paper:**
  1. Methods: "we ran every model on GPQA Diamond \citep{rein2023gpqa} and MMLU-Pro". **SUPPORTS.** §2.3 "Dataset Splits" (p. 7) says "We create
     GPQA Diamond (the diamond set, composed of 198 questions)". That matches the 198 items in Appendix (app:panel).
- **Better or additional citations:** none.

## wang2024mmlupro

- **Verified at:** https://arxiv.org/abs/2406.01574 (arXiv API comment: "accepted and published at NeurIPS 2024 Track
  Datasets and Benchmarks (Spotlight)");
  https://papers.nips.cc/paper_files/paper/2024/hash/ad236edc564f3e3156e1b2feafb99a24-Abstract-Datasets_and_Benchmarks_Track.html
  (meta tags and official BibTeX); https://api.crossref.org/works/10.52202/079017-3018. PDF read from proceedings.neurips.cc.
- **Metadata verdict: OK** (optional MINOR additions). The title and all 17 authors, in order, match the NeurIPS proceedings.
  The venue is correct: Advances in Neural Information Processing Systems 37, Datasets and Benchmarks Track, 2024. Optional
  additions are volume, pages, DOI and the proceedings URL:
  ```bibtex
  @inproceedings{wang2024mmlupro,
    title     = {{MMLU}-Pro: A More Robust and Challenging Multi-Task Language Understanding Benchmark},
    author    = {Wang, Yubo and Ma, Xueguang and Zhang, Ge and Ni, Yuansheng and Chandra, Abhranil and Guo, Shiguang and Ren, Weiming and Arulraj, Aaran and He, Xuan and Jiang, Ziyan and Li, Tianle and Ku, Max and Wang, Kai and Zhuang, Alex and Fan, Rongqi and Yue, Xiang and Chen, Wenhu},
    booktitle = {Advances in Neural Information Processing Systems (NeurIPS), Datasets and Benchmarks Track},
    volume    = {37},
    pages     = {95266--95290},
    year      = {2024},
    doi       = {10.52202/079017-3018},
    url       = {https://proceedings.neurips.cc/paper_files/paper/2024/hash/ad236edc564f3e3156e1b2feafb99a24-Abstract-Datasets_and_Benchmarks_Track.html}
  }
  ```
- **Uses in the paper:**
  1. Methods: "...and MMLU-Pro \citep{wang2024mmlupro}". **SUPPORTS.** §3.1 says "Our dataset comprises 14 discipline subsets,
     totaling 12,032 questions", with ten options. That is consistent with our 200-item draw over its 14 categories
     (Appendix app:panel).
- **Better or additional citations:** none.

---

## Summary

| bibkey | metadata verdict | relevance verdict | action needed |
|---|---|---|---|
| anthropic2026constitution | OK (published 22 Jan 2026) | SUPPORTS (both sentences) | None required. Optional: add `month`/`note` with the publication date and drop "Policy document". |
| openai2025modelspec | OK (the 2025-12-18 revision exists; year right) | SUPPORTS (civic-participation red line, both sentences) | None required. Optional: cite the current 2026-08-18 revision, which has identical wording; the old URL now shows an "outdated version" banner. Never use this reference for "power concentration" or "democratic processes". |
| chatterji2025chatgpt | OK (optional: middle names, DOI 10.3386/w34255, month) | SUPPORTS (ChatGPT only; the share is flat at ~29% while volume grows) | Optional rewording: "...practical guidance, the most common topic of ChatGPT conversations". |
| bates2015lme4 | OK (matches CRAN citation; optional DOI) | SUPPORTS | Fix the appendix wording: nAGQ = 0 is not "penalized quasi-likelihood" in lme4's own terms (see suggested wording). |
| benjamini1995fdr | MINOR (journal should read "Series B (Methodological)"; add DOI) | SUPPORTS | Update the journal name. Optional: ADD Benjamini & Yekutieli 2001 for validity under positive dependence. |
| mcnemar1947 | OK (optional DOI) | PARTIAL (framework yes; the (b−c)/(b+c) index itself is not McNemar's) | Reword so McNemar is credited for the discordant-pair framework. Optional: ADD Fagerland et al. 2013 where the Binomial(b+c, ½) null is used. Full text was paywalled; only the abstract was read. |
| rein2023gpqa | MINOR (cites arXiv; published at COLM 2024, Spotlight) | SUPPORTS (GPQA Diamond, 198 questions) | Change to `@inproceedings`, COLM 2024, OpenReview URL. |
| wang2024mmlupro | OK (NeurIPS 2024 D&B confirmed) | SUPPORTS | None required. Optional: add volume 37, pages 95266–95290, DOI 10.52202/079017-3018, proceedings URL. |
