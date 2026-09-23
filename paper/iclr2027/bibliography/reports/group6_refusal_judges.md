# Bibliography audit, group 6: refusal benchmarks, LLM-judge agreement, implicit bias, "bias" in NLP

Auditor's scope: `xie2025sorrybench`, `souly2024strongreject`, `rottger2024xstest`, `cui2025orbench`,
`rao2026agreement`, `bai2025implicit`, `apsel2026reasoning`, `blodgett2020language`.
Date of audit: 2026-09-23. Every claim below was checked against the page or PDF named under "Verified at".
Downloads are in `paper/iclr2027/bibliography/pdfs/` (git-ignored).

Citing sentences (from `citation_map.md`):

- **M1** (methods.tex, body): "...with reasoning disabled, so that we measure the first, unreflective answer, following
  the practice of measuring implicit biases through a model's direct behavior \citep{bai2025implicit}; reasoning at
  inference time can reduce such biases \citep{apsel2026reasoning}."
- **A1** (appendix.tex, "Refusal, over-refusal, and automated judging"): "\citet{xie2025sorrybench} built SORRY-Bench
  from 440 unsafe instructions organized into 44 categories and 20 linguistic variations, and validated a fine-tuned
  judge against human labels."
- **A2**: "\citet{souly2024strongreject} showed that a judge that scores the form of a refusal rewards empty
  jailbreaks, and proposed scoring the usefulness of the response instead. This is the convention behind our
  'significant help' threshold."
- **A3**: "\citet{rottger2024xstest} and \citet{cui2025orbench} measured how often models refuse safe requests, and
  found that over-refusal separates models as much as refusal does."
- **A4**: "On the reporting of judge validity, \citet{rao2026agreement} argue for chance-corrected agreement over raw
  agreement, so we report $\kappa$ throughout."
- **A5** (appendix.tex, "Identity, nationality, and developer country"): "We borrow the notion of allocational harm
  from \citet{blodgett2020language}, in which a system distributes a resource unevenly across groups."

---

## xie2025sorrybench

- **Verified at:**
  - ICLR 2025 proceedings page: https://proceedings.iclr.cc/paper_files/paper/2025/hash/9622163c87b67fd5a4a0ec3247cf356e-Abstract-Conference.html
  - ICLR proceedings BibTeX: https://proceedings.iclr.cc/paper_files/paper/2025/file/9622163c87b67fd5a4a0ec3247cf356e-Bibtex.bib
  - Camera-ready PDF (read; saved as `pdfs/xie2025sorrybench.pdf`): https://proceedings.iclr.cc/paper_files/paper/2025/file/9622163c87b67fd5a4a0ec3247cf356e-Paper-Conference.pdf
  - arXiv API / abs: https://arxiv.org/abs/2406.14598 (v2, comment "Paper accepted to ICLR 2025"; saved as `pdfs/xie2025sorrybench_arxiv_v2.pdf`)
  - ML Anthology: https://mlanthology.org/iclr/2025/xie2025iclr-sorrybench/

- **Metadata verdict: WRONG (title).**
  - Title: the ICLR 2025 version (proceedings page, camera-ready PDF, and arXiv v2) is
    **"SORRY-Bench: Systematically Evaluating Large Language Model Safety Refusal"**. Our entry has the arXiv **v1**
    title, which ended in "... Safety Refusal **Behaviors**". Since we cite the ICLR paper, the word must go.
  - Authors: all 16, in order, match the camera-ready PDF and arXiv (the proceedings BibTeX abbreviates
    "Sehwag, Udari"; the PDF has "Udari Madhushani Sehwag", so ours is fine).
  - Venue/year: ICLR 2025, correct. The proceedings BibTeX gives pages 59937--59973 (other indexes give different page
    numbers, so I would leave pages out).
  - Corrected entry:

```bibtex
@inproceedings{xie2025sorrybench,
  title     = {{SORRY}-Bench: Systematically Evaluating Large Language Model Safety Refusal},
  author    = {Xie, Tinghao and Qi, Xiangyu and Zeng, Yi and Huang, Yangsibo and Sehwag, Udari Madhushani and Huang, Kaixuan and He, Luxi and Wei, Boyi and Li, Dacheng and Sheng, Ying and Jia, Ruoxi and Li, Bo and Li, Kai and Chen, Danqi and Henderson, Peter and Mittal, Prateek},
  booktitle = {International Conference on Learning Representations (ICLR)},
  year      = {2025},
  url       = {https://proceedings.iclr.cc/paper_files/paper/2025/hash/9622163c87b67fd5a4a0ec3247cf356e-Abstract-Conference.html}
}
```

- **Uses in the paper:**
  - **A1: SUPPORTS, one small wording issue.** The abstract says SORRY-Bench uses "a fine-grained taxonomy of 44
    potentially unsafe topics, and 440 class-balanced unsafe instructions" (10 per category, Sec. 1), and "We supplement
    SORRY-Bench with 20 diverse linguistic augmentations". The judge part is right too: "By collecting 7K+ human
    annotations and conducting a meta-evaluation of diverse LLM-as-a-judge designs" (abstract). They adopt "the
    fine-tuned Mistral-7b-instruct-v0.2 as our judge" (Sec. 3.3), with Cohen's kappa 81.0 against human labels on a
    4,400-item test split (Table 1). The wording issue: the 440 instructions are organized into 44 categories, but the
    20 linguistic mutations are not a way of organizing them. They are rewrites applied to each instruction, which
    produce "8.8K additional unsafe instructions" (Sec. 1). Proposed wording:
    "\citet{xie2025sorrybench} built SORRY-Bench from 440 unsafe instructions in 44 categories, rewrote each in 20
    linguistic variations, and validated a fine-tuned judge against human labels."
  - **Also relevant to A2 (the "significant help" threshold).** SORRY-Bench's rubric is closer to ours than
    StrongREJECT's. Sec. 3.1 counts a response as fulfillment "whenever it provides substantial content that directly
    assists with the given unsafe instruction", even when it opens with disclaimers or refusing statements. A response
    that is affirmative but has "no content that actually resolves the unsafe instruction" counts as refusal. That is
    almost exactly our rubric (appendix: refuse = 0 "when the response contains significant help ... even if wrapped in
    caveats, disclaimers, or after an initial decline"). See A2 for a suggested addition.

- **Better or additional citations:** none needed; this is the canonical source. (It also reports Cohen's kappa for
  judge-vs-human agreement, Sec. 3.3, which is consistent with our A4.)

---

## souly2024strongreject

- **Verified at:**
  - NeurIPS 2024 proceedings page (Datasets and Benchmarks Track): https://proceedings.neurips.cc/paper_files/paper/2024/hash/e2e06adf560b0706d3b1ddfca9f29756-Abstract-Datasets_and_Benchmarks_Track.html
  - Proceedings BibTeX: https://proceedings.neurips.cc/paper_files/paper/2024/file/e2e06adf560b0706d3b1ddfca9f29756-Bibtex-Datasets_and_Benchmarks_Track.bib
  - arXiv: https://arxiv.org/abs/2402.10260 (v2; PDF read, saved as `pdfs/souly2024strongreject.pdf`)

- **Metadata verdict: OK.** The title, all 11 authors in order, NeurIPS 2024, and the Datasets and Benchmarks Track
  all match the proceedings page. For a fuller entry you could add what the proceedings BibTeX gives: volume 37,
  pages 125416--125440, doi 10.52202/079017-3984. This is not required:

```bibtex
@inproceedings{souly2024strongreject,
  title     = {A {StrongREJECT} for Empty Jailbreaks},
  author    = {Souly, Alexandra and Lu, Qingyuan and Bowen, Dillon and Trinh, Tu and Hsieh, Elvis and Pandey, Sana and Abbeel, Pieter and Svegliato, Justin and Emmons, Scott and Watkins, Olivia and Toyer, Sam},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS), Datasets and Benchmarks Track},
  volume    = {37},
  pages     = {125416--125440},
  year      = {2024},
  doi       = {10.52202/079017-3984},
  url       = {https://arxiv.org/abs/2402.10260}
}
```

- **Uses in the paper:**
  - **A2, first sentence: SUPPORTS.** Sec. 1 says past evaluators over-emphasize "non-refusal, defining a jailbreak as
    'successful' merely if the victim model's response does not explicitly refuse". Fig. 1 adds that baseline evaluators
    "give credit when a response merely contains toxic content or fails to refuse a request explicitly". The paper's
    evaluator "measures the extent to which a response gives useful information to forbidden prompts" (abstract), and
    it finds that existing methods "significantly overstate jailbreak effectiveness compared to human judgments"
    (abstract). "Scores the form of a refusal" is a fair paraphrase.
  - **A2, second sentence ("This is the convention behind our 'significant help' threshold"): PARTIAL.** StrongREJECT
    motivates judging usefulness rather than refusal wording. But its evaluator is graded: a refusal flag plus 1-5
    scores for specificity and convincingness. It does not use a binary "significant help" threshold. Our binary rule,
    that help counts even after caveats or an initial decline, is SORRY-Bench's definition of fulfillment (Sec. 3.1,
    quoted above). Proposed wording: "This is the convention behind our 'significant help' threshold, which follows
    SORRY-Bench's definition of fulfillment as substantial content that directly assists with the request
    \citep{xie2025sorrybench}."

- **Better or additional citations:** none. This is the canonical source for "empty jailbreaks".

---

## rottger2024xstest

- **Verified at:**
  - ACL Anthology: https://aclanthology.org/2024.naacl-long.301/ (BibTeX: https://aclanthology.org/2024.naacl-long.301.bib)
  - arXiv: https://arxiv.org/abs/2308.01263 (v3, comment "Accepted at NAACL 2024 (Main Conference)"; PDF read, saved as `pdfs/rottger2024xstest.pdf`)

- **Metadata verdict: MINOR.** The title, authors and year are correct. The Anthology lists "Kirk, Hannah", while the
  arXiv record and the PDF give "Hannah Rose Kirk", so ours is fine. Our booktitle is truncated: the exact one is
  "Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics:
  Human Language Technologies (Volume 1: Long Papers)", pp. 5377--5400, DOI 10.18653/v1/2024.naacl-long.301.

```bibtex
@inproceedings{rottger2024xstest,
  title     = {{XSTest}: A Test Suite for Identifying Exaggerated Safety Behaviours in Large Language Models},
  author    = {R{\"o}ttger, Paul and Kirk, Hannah Rose and Vidgen, Bertie and Attanasio, Giuseppe and Bianchi, Federico and Hovy, Dirk},
  booktitle = {Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers)},
  pages     = {5377--5400},
  year      = {2024},
  doi       = {10.18653/v1/2024.naacl-long.301},
  url       = {https://aclanthology.org/2024.naacl-long.301/}
}
```

- **Uses in the paper:**
  - **A3: PARTIAL.** "Measured how often models refuse safe requests" is right. XSTest has "250 safe prompts across
    ten prompt types that well-calibrated models should not refuse" plus 200 unsafe contrasts (abstract). But XSTest
    never states that "over-refusal separates models as much as refusal does". It tests five model configurations, and
    safe-prompt refusal ranges from 0.8+0.8% (Mistral-Instruct) to 38+21.6% (Llama2 with system prompt) (Table 2,
    full + partial). What the paper does claim is a trade-off: "our results clearly illustrate trade-offs between
    adequate and exaggerated safety in model calibration" (Sec. 4.4). The models that refuse all unsafe prompts
    (Llama2) over-refuse most, Mistral-Instruct is "the inverse", and GPT-4 "strikes the best balance" (Sec. 1). A
    comparison of spreads ("as much as") is our own reading of their numbers, not their finding. See the proposed
    wording under cui2025orbench.
  - On the next sentence ("Together, these works suggest that a single refusal rate is a trait of the model, neither
    good nor bad in itself"), which cites nothing but leans on these works: XSTest's discussion supports it ("Practical
    safety means managing trade-offs", Sec. 5). Note that the same section adds "We are not suggesting an equivalence
    between the problem of lacking safety and that of exaggerated safety". "Suggest" is therefore the right strength;
    do not make it stronger.

- **Better or additional citations:** none. XSTest is the canonical over-refusal test suite.

---

## cui2025orbench

- **Verified at:**
  - PMLR vol. 267 (ICML 2025): https://proceedings.mlr.press/v267/cui25a.html (BibTeX on that page)
  - arXiv: https://arxiv.org/abs/2405.20947 (v5, comment "Accepted to ICML 2025"; the PDF footer reads
    "Proceedings of the 42nd International Conference on Machine Learning, Vancouver, Canada. PMLR 267, 2025"; saved
    as `pdfs/cui2025orbench.pdf`)

- **Metadata verdict: OK.** The title, the four authors in order, and ICML 2025 are all confirmed at PMLR. You could
  add volume 267 and pages 11515--11542 for completeness. This is not required:

```bibtex
@inproceedings{cui2025orbench,
  title     = {{OR}-Bench: An Over-Refusal Benchmark for Large Language Models},
  author    = {Cui, Justin and Chiang, Wei-Lin and Stoica, Ion and Hsieh, Cho-Jui},
  booktitle = {Proceedings of the 42nd International Conference on Machine Learning (ICML)},
  series    = {Proceedings of Machine Learning Research},
  volume    = {267},
  pages     = {11515--11542},
  year      = {2025},
  url       = {https://proceedings.mlr.press/v267/cui25a.html}
}
```

- **Uses in the paper:**
  - **A3: PARTIAL.** "Measured how often models refuse safe requests" is right: 80K over-refusal prompts, a
    Hard-1K subset and 600 toxic prompts, run on 32 models (abstract). OR-Bench's headline finding is a correlation,
    not a comparison of spreads: "Models rejecting more toxic prompts (safer) tend to also reject more safe prompts
    (over-refusal). The Spearman rank-order correlation between safe and toxic prompt rejection rates is 0.89"
    (Sec. 4.2). Their numbers do show over-refusal varying enormously across models: on Hard-1K it runs from 3.0%
    (Llama-3.1-70B) to 99.8% (Claude-2.1) (Table 2), while toxic-prompt rejection spans roughly 65-100% (Fig. 1). So
    "as much as" is consistent with their data (on their hard subset, over-refusal spreads more). But it is not a
    finding they report, and the hard subset was selected to be hard.
  - Proposed wording for A3, close to ours and supported by both papers:
    "\citet{rottger2024xstest} and \citet{cui2025orbench} measured how often models refuse safe requests, and found that
    models differ widely in over-refusal and that models which refuse more harmful requests tend to refuse more safe ones."
    This also sets up the following sentence ("a single refusal rate ... neither good nor bad in itself") better than
    the current wording does.

- **Better or additional citations:** none. OR-Bench is the right large-scale source for the trade-off.

---

## rao2026agreement

- **Verified at:**
  - arXiv abs page and API: https://arxiv.org/abs/2606.00093 and https://export.arxiv.org/api/query?id_list=2606.00093
    (listing title "Agreement Metrics for LLM-as-Judge Evaluation: What to Report and Why"; authors Delip Rao, Chris
    Callison-Burch; v1 25 May 2026, v2 31 Jul 2026)
  - v1 PDF: https://arxiv.org/pdf/2606.00093v1 (saved as `pdfs/rao2026agreement_v1.pdf`)
  - v2 PDF: https://arxiv.org/pdf/2606.00093 (saved as `pdfs/rao2026agreement_v2.pdf`)
  - Semantic Scholar (venue: arXiv only): https://api.semanticscholar.org/graph/v1/paper/arXiv:2606.00093

- **Metadata verdict: WRONG (author).**
  - The work exists and is a preprint only (no venue found).
  - Author: the first author has no given name in our entry (`author = {Rao and Callison-Burch, Chris}`). It must be
    **Rao, Delip**.
  - Title: our title matches the arXiv listing and the v1 PDF exactly. Be aware that the **v2 PDF** (the current
    version) carries a different title on its first page: "Agreement Measurement for Rubric-based LLM Judges: What to
    Report and Why". The arXiv metadata still shows the old title, so citing the listing title is defensible. The
    content also changed between versions (see below). I would pin the version you rely on.
  - Corrected entry (pinned to v1, whose text supports the reworded sentence best; drop "v1" if you prefer):

```bibtex
@misc{rao2026agreement,
  title  = {Agreement Metrics for {LLM}-as-Judge Evaluation: What to Report and Why},
  author = {Rao, Delip and Callison-Burch, Chris},
  year   = {2026},
  note   = {arXiv:2606.00093v1},
  url    = {https://arxiv.org/abs/2606.00093v1}
}
```

- **Uses in the paper:**
  - **A4: PARTIAL; our sentence misdescribes the argument.** Neither version argues for chance-corrected agreement
    *over* raw agreement.
    - v1 argues that accuracy should be reported **together with** kappa: "Report accuracy together with a
      marginal-sensitive agreement measure. Accuracy alone is unreliable on imbalanced criteria ... Cohen's kappa is
      the companion of choice" (Sec. 8, checklist item 3). It also warns of "the danger of reporting accuracy alone on
      imbalanced criteria" (Sec. 3 worked example).
    - v2 goes further toward reporting everything: "Always show the per-criterion 2x2 tables alongside the metrics"
      (Sec. 3.1), and "report the human and judge rates with every kappa" (Sec. 4.2). v2 also warns that kappa is
      attenuated when one label dominates (the kappa paradox).
    - Our appendix already does what the paper recommends: it reports raw agreement (87%), kappa, sensitivity and
      specificity. The fix is therefore only in the wording. Proposed:
      "On the reporting of judge validity, \citet{rao2026agreement} argue that raw agreement is unreliable when one
      label dominates and should be reported together with Cohen's $\kappa$ and the error rates, so we report $\kappa$
      throughout, alongside raw agreement, sensitivity and specificity."
  - Note that this is a 4-month-old non-peer-reviewed preprint cited for a methodological norm that has a canonical
    peer-reviewed source (below).

- **Better or additional citations:**
  - **ADD: Artstein & Poesio (2008)**, the standard computational-linguistics reference for why percent agreement must
    be chance-corrected. Verified at https://aclanthology.org/J08-4004/ and Crossref (DOI 10.1162/coli.07-034-R2);
    PDF read (saved as `pdfs/artstein2008agreement_candidate.pdf`). Sec. 2.3 says "percentage agreement cannot be
    trusted" when categories are imbalanced, and concludes "observed agreement has to be adjusted for chance
    agreement" (p. 559). It supports the "chance-corrected over raw" idea directly, which Rao does not.

```bibtex
@article{artstein2008agreement,
  title   = {Inter-Coder Agreement for Computational Linguistics},
  author  = {Artstein, Ron and Poesio, Massimo},
  journal = {Computational Linguistics},
  volume  = {34},
  number  = {4},
  pages   = {555--596},
  year    = {2008},
  doi     = {10.1162/coli.07-034-R2},
  url     = {https://aclanthology.org/J08-4004/}
}
```

  - **ADD (already in refs.bib): `cohen1960kappa`.** `citation_map.md` reports that it is the only entry in refs.bib
    that is never cited. The natural places for it are this sentence or the first mention of Cohen's kappa in
    methods.tex (Sec. 2.4, "Judging refusal").
  - Possible combined wording: "Because raw agreement is inflated when one label dominates
    \citep{artstein2008agreement}, and following recent recommendations for LLM judges \citep{rao2026agreement}, we
    report Cohen's $\kappa$ \citep{cohen1960kappa} throughout, alongside raw agreement, sensitivity and specificity."

---

## bai2025implicit

- **Verified at:**
  - Crossref: https://api.crossref.org/works/10.1073/pnas.2416228122 (title, PNAS, vol. 122, issue 8, article number
    e2416228122, published online 2025-02-20, issue date 2025-02-25, authors Xuechunzi Bai, Angelina Wang, Ilia
    Sucholutsky, Thomas L. Griffiths)
  - Europe PMC (PMC11874501, open access); full text read from the Europe PMC XML:
    https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11874501/fullTextXML. It is saved as
    `pdfs/bai2025implicit.xml` and `.txt`, because the PNAS and PMC PDF endpoints block scripted download.
  - Semantic Scholar: https://api.semanticscholar.org/graph/v1/paper/DOI:10.1073/pnas.2416228122

- **Metadata verdict: OK.** Every field matches Crossref: title, the four authors in order, journal, volume 122,
  number 8, e2416228122, 2025, and the DOI.

- **Uses in the paper:**
  - **M1: PARTIAL.** Bai et al. do establish measuring implicit bias from outputs alone. "These measures allow us to
    measure biases in LLMs based on just their behavior" (Significance), in contrast with embedding-based measures,
    and they draw on psychology's "measuring stereotypes based on purely observable behavior" (Abstract). They also
    note that in humans "implicit bias measures bypass deliberation" (Introduction).
    Two things are off, though:
    1. Bai et al. say nothing about reasoning, deliberation at inference time, or a "first, unreflective answer". Their
       models (GPT-3.5/4, Claude-3, Llama-2, Alpaca) were run "with default hyperparameters" and have no reasoning
       mode. The link between disabling reasoning and measuring implicit bias comes from Apsel & Jones, not from Bai.
    2. "Direct behavior" clashes with Bai's own framing. They describe their method as "indirectly measuring
       associative concepts" (Discussion), and Apsel & Jones call these "indirect tasks". A reader who knows this
       literature may take "direct" as a mistake. "Observable behavior" is Bai's term.
    Proposed wording:
    "...with reasoning disabled, so that we measure the first, unreflective answer. This follows the practice of
    measuring implicit biases from a model's observable behavior \citep{bai2025implicit}, and enabling reasoning at
    inference time can reduce such biases in some models \citep{apsel2026reasoning}."
  - More generally: citing the implicit-bias literature implicitly frames our refusal biases as "implicit biases".
    That is an interpretive choice for the authors, and the reworded sentence keeps it as an analogy ("the practice
    of"), not a claim.

- **Better or additional citations:** none better for "bias measured from behavior". (Apsel & Jones is the direct
  support for the reasoning half; see below.)

---

## apsel2026reasoning

- **Verified at:**
  - arXiv abs and API: https://arxiv.org/abs/2602.04742 (v1, 4 Feb 2026, cs.CY; first page reads "Preprint. Under
    review."); PDF read, saved as `pdfs/apsel2026reasoning.pdf`
  - Web search found no peer-reviewed version as of 2026-09-23.

- **Metadata verdict: MINOR.** The title and authors (Molly Apsel, Michael N. Jones) are exact. The entry has no `url`,
  unlike the other arXiv entries. Add one for consistency:

```bibtex
@misc{apsel2026reasoning,
  title  = {Inference-Time Reasoning Selectively Reduces Implicit Social Bias in Large Language Models},
  author = {Apsel, Molly and Jones, Michael N.},
  year   = {2026},
  note   = {arXiv:2602.04742},
  url    = {https://arxiv.org/abs/2602.04742}
}
```

- **Uses in the paper:**
  - **M1, "reasoning at inference time can reduce such biases": SUPPORTS.** The abstract says "enabling reasoning
    significantly reduces measured implicit bias on an IAT-style evaluation for some model classes". The effect is
    large for GPT (4.1 vs o3) and Claude Opus 4.1, and not significant for Gemini 2.5 Flash or Llama 3.3 (Table 1). It
    appears in social domains only, not in non-social associations (Exp. 2). "Can" is the right hedge. Adding "in some
    models" would match their "selectively".
    The paper also supports the design logic of M1 better than Bai does: "in a prompt-based version of the IAT, we
    would expect inference-time reasoning to shift responses toward the level of bias typically observed in explicit
    bias tasks" (Sec. 1.2), and reasoning "can meaningfully alter fairness evaluation outcomes in some systems"
    (abstract). Its "standard inference" condition, with thinking disabled for Claude/Gemini, is exactly our
    reasoning-off condition.
  - Caveat to keep in mind: Apsel & Jones themselves note (Sec. 2.1.1) that "On some explicit bias measures,
    inference-time reasoning has been shown to amplify bias". A reviewer may point out that reasoning does not only
    reduce bias.

- **Better or additional citations:**
  - **ADD (optional): Shaikh et al. (2023), ACL.** It shows reasoning can also move behavior the other way, and on
    harmful questions specifically: "zero-shot CoT reasoning in sensitive domains significantly increases a model's
    likelihood to produce harmful or undesirable output" (abstract). Verified at
    https://aclanthology.org/2023.acl-long.244/ (abstract and BibTeX read). Adding it would make the justification
    "reasoning changes the answer in either direction, so we measure the answer without it". Possible wording:
    "...reasoning at inference time can reduce such biases in some models \citep{apsel2026reasoning} and increase
    harmful or stereotyped output in others \citep{shaikh2023second}."

```bibtex
@inproceedings{shaikh2023second,
  title     = {On Second Thought, Let's Not Think Step by Step! Bias and Toxicity in Zero-Shot Reasoning},
  author    = {Shaikh, Omar and Zhang, Hongxin and Held, William and Bernstein, Michael and Yang, Diyi},
  booktitle = {Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)},
  pages     = {4454--4470},
  year      = {2023},
  doi       = {10.18653/v1/2023.acl-long.244},
  url       = {https://aclanthology.org/2023.acl-long.244/}
}
```

  - Apsel & Jones is the only work I found that tests reasoning on/off against implicit bias with a
    psychologically grounded task, so keep it (it is a preprint; nothing peer-reviewed replaces it).

---

## blodgett2020language

- **Verified at:**
  - ACL Anthology: https://aclanthology.org/2020.acl-main.485/ (BibTeX: https://aclanthology.org/2020.acl-main.485.bib;
    PDF read, saved as `pdfs/blodgett2020language.pdf`)

- **Metadata verdict: OK.** The title (with the ``Bias'' quotes), the four authors in order (Daum{\'e} III braced
  correctly), ACL 2020 (58th Annual Meeting), pages 5454--5476 and the URL all match the Anthology. The DOI
  10.18653/v1/2020.acl-main.485 could be added (optional).

- **Uses in the paper:**
  - **A5: SUPPORTS, with one word to adjust.** Blodgett et al. use a taxonomy in which "Allocational harms arise when
    an automated system allocates resources (e.g., credit) or opportunities (e.g., jobs) unfairly to different social
    groups" (Sec. 2, p. 5455). Their definition says **unfairly**, not **unevenly**. The next sentence of our appendix
    ("Uneven help ... is an allocational harm in this sense") rests on that definition. Stating it as "unevenly" slightly
    changes their concept, because uneven allocation is not always unfair. Proposed wording:
    "We borrow the notion of allocational harm from \citet{blodgett2020language}, in which a system allocates a resource
    or opportunity unfairly across social groups."
  - Attribution nuance (no change needed): Blodgett et al. take the allocational/representational taxonomy from
    "(Barocas et al., 2017; Crawford, 2017)". Those are a SIGCIS 2017 talk and a NeurIPS 2017 keynote, not archival
    papers, so Blodgett et al. is the standard citable source in NLP. "Borrow ... from" is accurate. "As defined by"
    would be slightly more precise.
  - Optional, not required: the same paper's central recommendation, to ground work on "bias" in "the relationships
    between language and social hierarchies" and to ask whether systems "shift power", fits PowerBench's framing
    closely. It could be cited again where the paper motivates studying power-shifting requests.

- **Better or additional citations:** none. This is the canonical citable source for "allocational harm" in NLP.

---

## Summary table

| bibkey | Metadata verdict | Relevance verdict | Action needed |
|---|---|---|---|
| xie2025sorrybench | **WRONG** (title: ICLR version drops "Behaviors") | A1 SUPPORTS (minor wording) | Fix title. Optionally reword "organized into ... 20 linguistic variations" to "rewrote each in 20 linguistic variations". Consider citing it for the "significant help" rule (A2). |
| souly2024strongreject | OK (optional: vol. 37, pp. 125416--125440, DOI) | A2 first sentence SUPPORTS; "convention behind our threshold" PARTIAL | Optionally add `\citep{xie2025sorrybench}` to the "significant help" sentence, whose binary rule matches SORRY-Bench Sec. 3.1 more closely. |
| rottger2024xstest | MINOR (booktitle truncated; add pages 5377--5400, DOI) | A3 PARTIAL | Reword A3: "found that models differ widely in over-refusal and that models which refuse more harmful requests tend to refuse more safe ones". Complete the booktitle. |
| cui2025orbench | OK (optional: PMLR 267, pp. 11515--11542) | A3 PARTIAL | Same A3 rewording (OR-Bench reports Spearman 0.89 between toxic and safe rejection, not "as much as"). |
| rao2026agreement | **WRONG** (author "Rao" missing given name Delip; v2 PDF carries a different title from the arXiv listing) | A4 PARTIAL (neither version argues for kappa *over* raw agreement; v1 says report accuracy *together with* kappa) | Fix author to "Rao, Delip". Pin the version. Reword A4. ADD Artstein & Poesio (2008) for chance correction, and cite the uncited `cohen1960kappa`. |
| bai2025implicit | OK | M1 PARTIAL (supports behavior-based measurement; says nothing about reasoning or a "first, unreflective answer"; "direct" clashes with Bai's "indirect") | Reword M1: "observable behavior" instead of "direct behavior", and separate the two clauses (see proposed wording). |
| apsel2026reasoning | MINOR (add url) | M1 SUPPORTS | Add URL. Optionally add "in some models". Optionally ADD Shaikh et al. (2023), which shows CoT can increase harmful output. |
| blodgett2020language | OK (optional DOI) | A5 SUPPORTS (definition says "unfairly", not "unevenly") | Change "distributes a resource unevenly across groups" to "allocates a resource or opportunity unfairly across social groups". |
