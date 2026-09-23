# Bibliography audit, group 4: nationality, developer country, user identity, geopolitical bias, election disinformation

Auditor scope: `khorramrouz2026selective`, `pan2026censorship`, `haslett2025madeinchina`, `bladon2026geopolitical`,
`chang2025homecountries`, `pooledayan2026underperformance`, `liu2025agentic`, `williams2025election`.
Date of checks: 2026-09-23. Every work below was opened and read at the URLs given (abstract, introduction, the
results that bear on our sentences, and discussion/conclusion). Local copies are in `bibliography/pdfs/`.

## A problem common to seven of the eight entries

Seven entries give **surnames only** (e.g. `author = {Khorramrouz and Levy}`), so the compiled bibliography prints
"Khorramrouz and Levy.", "Pan and Xu.", "Liu, Wang, Cheng, and Sadao Kurohashi." (checked in `submission/main.bbl`).
The author identities are right in all seven (no missing or wrong author), but the lists are incomplete and look sloppy
to a reviewer. Every corrected entry below has the full names from the primary source. `pooledayan2026underperformance`
is the only entry that already has them.

---

## khorramrouz2026selective

- **Verified at:** https://aclanthology.org/2026.findings-acl.550/ (page and `.bib`), PDF https://aclanthology.org/2026.findings-acl.550.pdf (saved as `pdfs/khorramrouz2026selective.pdf`).
- **Metadata verdict: MINOR.** Title, venue (Findings of ACL 2026) and year are right. The authors are Adel Khorramrouz
  and Sharon Levy (Rutgers University); first names are missing. Pages and DOI can be added.

```bibtex
@inproceedings{khorramrouz2026selective,
  title     = {Characterizing Selective Refusal Bias in Large Language Models},
  author    = {Khorramrouz, Adel and Levy, Sharon},
  booktitle = {Findings of the Association for Computational Linguistics: ACL 2026},
  pages     = {11305--11326},
  year      = {2026},
  publisher = {Association for Computational Linguistics},
  doi       = {10.18653/v1/2026.findings-acl.550},
  url       = {https://aclanthology.org/2026.findings-acl.550/}
}
```

- **What the paper does:** 800 generic harmful templates adapted from WildGuardMix ("generic prompts that can target
  any group", §3.2), with the target group swapped across 41 groups by gender, sexual orientation, religion and
  nationality (21 nationalities), sent to GPT-4o, Llama-3.1-70B and Gemini 1.5 Pro. Result for nationality (§4.1):
  "American, Canadian, and French groups consistently rank among the lowest refusal rates", and Mexicans are among the
  three most-refused nationalities in every model.
- **Uses in the paper:**
  1. Intro: "Biases by nationality, developer country, language, and type of requester have been documented
     [khorramrouz, pan, liu, elyagoubi] ... but only on requests that do not shift power." **SUPPORTS** (nationality).
     A caution on the "do not shift power" clause: some templates ask for content that denies a group jobs, education or
     healthcare (Table 1: "an interviewer explicitly denies job offers to demographic group"; Table 3: "Pakistanis are
     unworthy of access to quality education"). They are requests for discriminatory text, not advice to shift power
     between the user and another party, so the claim holds under our definition, but a reviewer could raise it.
  2. Related: "...the identity of the user matters as well: ... and refuse depending on the nationality that a harmful
     request targets [khorramrouz]." **PARTIAL.** The clause itself is accurate, but it sits under "the identity of the
     user matters", and the paper says explicitly that it studies "user queries about demographic groups instead of
     queries from the persona of a group" (§2). The target is not the user. Suggested wording: "...and the identities
     involved matter as well: models ... serve some users worse than others, and refuse depending on the nationality
     that a harmful request targets." (or "who asks and whom a request targets matter as well").
  3. Appendix: "Closer to our setting, Khorramrouz & Levy found that refusal depends on the nationality of the group
     that a generic harmful request targets". **SUPPORTS**, accurate ("generic" matches the paper's own term).
- **Better or additional citations:** Khorramrouz & Levy is the right and most direct work for refusal by the targeted
  nationality. For the user-identity half of the related-work sentence, see Li, Chen & Saphra (2024) under
  `pooledayan2026underperformance` (ADD).

---

## pan2026censorship

- **Verified at:** Crossref https://api.crossref.org/works/10.1093/pnasnexus/pgag013 ; DOI https://doi.org/10.1093/pnasnexus/pgag013 ;
  full text via Europe PMC (PMC12910507) https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12910507/fullTextXML
  (OUP and PMC block scripted PDF downloads, so the full text is saved as `pdfs/pan2026censorship.txt`).
- **Metadata verdict: MINOR.** Title, journal, volume 5, issue 2 and year 2026 are right (published online 17 Feb 2026).
  The authors are Jennifer Pan (Stanford) and Xu Xu (Princeton); first names are missing. Add the article number and
  DOI. The URL in refs.bib is OUP's own article URL and is valid, but the DOI URL is more stable. (Mohammad Atari, who
  appears in the XML, is the handling editor, not an author.)

```bibtex
@article{pan2026censorship,
  title   = {Political Censorship in Large Language Models Originating from {C}hina},
  author  = {Pan, Jennifer and Xu, Xu},
  journal = {PNAS Nexus},
  volume  = {5},
  number  = {2},
  pages   = {pgag013},
  year    = {2026},
  doi     = {10.1093/pnasnexus/pgag013},
  url     = {https://doi.org/10.1093/pnasnexus/pgag013}
}
```

- **What the paper finds:** on 145 questions about Chinese politics, 4 China-originating models (BaiChuan, ChatGLM,
  Ernie Bot, DeepSeek) show "substantially higher rates of refusal to respond, shorter responses, and inaccurate
  responses" than 5 non-China models (abstract). The gap shrinks on the 30 less-sensitive questions. All models refuse
  more in Chinese than in English, but "language differences are less pronounced than disparities between
  China-originating and non-China-originating models". The authors say the study is observational.
- **Uses in the paper:**
  1. Intro, list of documented biases (developer country). **SUPPORTS.**
  2. Related: "Geopolitical biases also depend on the developer's country, though not simply as favoritism toward it."
     **SUPPORTS** the first clause (political bias that tracks developer country). Strictly, the paper is about
     censorship of Chinese domestic political topics, not geopolitics between countries; "political and geopolitical
     biases" would describe the four citations more exactly.
  3. Appendix: "Pan & Xu found that models originating from China refuse politically sensitive questions in a way that
     tracks their DC". **SUPPORTS**, but it is tautological as written (models from China ... tracks their DC).
     Suggested wording: "found that models developed in China refuse questions that are politically sensitive in China
     far more often than models developed elsewhere, a gap that shrinks for less sensitive questions".
- **Better or additional citations:** none needed; this is the peer-reviewed reference on the point.

---

## haslett2025madeinchina

- **Verified at:** https://arxiv.org/abs/2512.13723 (arXiv API record and PDF v1, 13 Dec 2025; saved as `pdfs/haslett2025madeinchina.pdf`).
  No later venue found (arXiv lists only v1; not in the ACL 2026, EACL 2026 or NAACL 2026 Anthology volumes).
- **Metadata verdict: MINOR.** The exact title is "Made-in China, Thinking in America:U.S. Values Persist in Chinese
  LLMs" (arXiv record and PDF: "Made-in China" with a space, not "Made-in-China"; a space after the colon is a harmless
  normalisation). Authors: David Haslett, Linus Ta-Lun Huang, Leila Khalatbari, Janet Hui-wen Hsiao, Antoni B. Chan;
  first names are missing.

```bibtex
@misc{haslett2025madeinchina,
  title  = {Made-in {C}hina, Thinking in {A}merica: {U.S.} Values Persist in {C}hinese {LLMs}},
  author = {Haslett, David and Huang, Linus Ta-Lun and Khalatbari, Leila and Hsiao, Janet Hui-wen and Chan, Antoni B.},
  year   = {2025},
  note   = {arXiv:2512.13723},
  url    = {https://arxiv.org/abs/2512.13723}
}
```

- **What the paper finds:** 10 Chinese and 10 US models answered the Moral Foundations Questionnaire 2.0 and 19 WVS
  ethics items. "all 20 LLMs responded more like American participants than like Chinese participants", a skew "only
  slightly mitigated when LLMs were made in China", or when prompted in Chinese or given a Chinese persona (§5). On the
  MFQ-2 the LLM-origin × nationality interaction is "far from significant (p > .7)" (§4.1).
- **Uses in the paper:**
  1. Related: "Geopolitical biases also depend on the developer's country, though not simply as favoritism toward it."
     **PARTIAL.** Haslett supports "not simply as favoritism" well, but it measures moral and cultural values, not
     geopolitical bias, and it finds that developer country barely matters. Changing "Geopolitical biases" to
     "Geopolitical and value biases" (or "Political and cultural biases") would make the sentence fit all four
     citations.
  2. Appendix: "whereas Haslett et al. found that Chinese-developed models carry many US-typical values." **SUPPORTS**
     in substance. More precise: "found that Chinese-developed models answer moral-values surveys more like Americans
     than like Chinese people".
- **Better or additional citations:** see Buyl et al. (2026) under `bladon2026geopolitical`, a peer-reviewed study of
  ideology by developer region that fits the "Geopolitical biases also depend on the developer's country" sentence.

---

## bladon2026geopolitical

- **Verified at:** https://arxiv.org/abs/2605.23825 (arXiv API record and PDF v1, 22 May 2026; saved as `pdfs/bladon2026geopolitical.pdf`). Unreviewed preprint, only v1, no venue found.
- **Metadata verdict: MINOR.** The title is right (arXiv uses sentence case; our title case is fine). Authors: Stuart
  Bladon, Brinnae Bent (Duke University); first names are missing.

```bibtex
@misc{bladon2026geopolitical,
  title  = {It's the Humans, Not the Data: Geopolitical Bias in {LLMs} Originates in Post-Training, Amplified by the Language of the Prompt},
  author = {Bladon, Stuart and Bent, Brinnae},
  year   = {2026},
  note   = {arXiv:2605.23825},
  url    = {https://arxiv.org/abs/2605.23825}
}
```

- **What the paper finds:** 7 base/chat pairs of 7–9B open-weight models (Mistral, Llama 3, Gemma 4, Qwen 2.5,
  Baichuan 2, Yi 1.5, GLM 4) on a forced-choice logit probe over 28 country pairs in English, French and Chinese.
  Bases are near-neutral and post-training shifts preferences: "Direction tracks the maker for 6 of 7 families"
  (binomial p = 0.125; signed t-test p = 0.032). Yi is a counter-example, and the authors conclude that this "rules out
  the simple reading that 'Chinese-lab origin' mechanically produces pro-China shifts". On language, the authors' own
  test fails: "The population-level Chinese-prompt amplification claim does not survive formal testing" (paired
  p = 0.66, Limitations). The clean case is Mistral prompted in French, which they call "an existence proof".
- **Uses in the paper:**
  1. Intro: "model behavior varies with ... the country of the developer [deng, pooledayan, bladon]." **SUPPORTS**,
     with caveats: an unreviewed preprint on small open-weight models, where the maker effect is significant only on
     the t-test. Adding a peer-reviewed citation (Buyl et al., below) would strengthen the sentence.
  2. Related: "Geopolitical biases also depend on the developer's country, though not simply as favoritism toward it."
     **SUPPORTS** both clauses (6/7 maker-aligned; Yi and the "four Chinese labs doing four different things").
  3. Appendix: "Bladon & Bent traced geopolitical bias to post-training and found it amplified by the language of the
     prompt". **PARTIAL.** The first half matches the paper, which itself hedges that it cannot tell "post-training
     installs bias" from "post-training makes the MCQ probe sensitive". The second half repeats the title, but the
     paper's own results do not support amplification as a general finding. Suggested wording: "traced geopolitical
     bias to post-training and found that the language of the prompt can amplify it".
- **Better or additional citations: ADD** Buyl et al. (2026), peer-reviewed, 19 LLMs: "the ideological stance of an
  LLM reflects the worldview of its creators" (abstract), with differences between models from Arabic countries,
  China, Russia and the West, and between prompting languages. It also supports "not simply as favoritism": models from
  China "are particularly critical of political persons tagged with China (PRC)" (Results, "Ideologies vary by
  language and by region"), and there is a "division between internationally- and domestically-focused" Chinese
  models. Suggested placement: add it to the intro citation for "the country of the developer" (next to or instead of
  Bladon) and to the related-work sentence on the developer's country. Verified at Crossref
  https://api.crossref.org/works/10.1038/s44387-025-00048-0 and https://doi.org/10.1038/s44387-025-00048-0 (open
  access PDF saved as `pdfs/candidate_buyl2026ideology.pdf`); arXiv 2410.18417.

```bibtex
@article{buyl2026ideology,
  title   = {Large Language Models Reflect the Ideology of Their Creators},
  author  = {Buyl, Maarten and Rogiers, Alexander and Noels, Sander and Bied, Guillaume and Dominguez-Catena, Iris and Heiter, Edith and Johary, Iman and Mara, Alexandru-Cristian and Romero, Rapha{\"e}l and Lijffijt, Jefrey and De Bie, Tijl},
  journal = {npj Artificial Intelligence},
  volume  = {2},
  number  = {1},
  pages   = {7},
  year    = {2026},
  doi     = {10.1038/s44387-025-00048-0},
  url     = {https://doi.org/10.1038/s44387-025-00048-0}
}
```

---

## chang2025homecountries

- **Verified at:** https://misinforeview.hks.harvard.edu/article/do-language-models-favor-their-home-countries-asymmetric-propagation-of-positive-misinformation-and-foreign-influence-audits/
  (page citation meta tags), PDF https://misinforeview.hks.harvard.edu/wp-content/uploads/2025/09/chang_language_models_not_biasd_20250922.pdf
  (saved as `pdfs/chang2025homecountries.pdf` and `.html`), Crossref https://api.crossref.org/works/10.37016/mr-2020-183 .
- **Metadata verdict: MINOR.** Title, journal and year are right. The PDF header reads "August 2025, Volume 6,
  Issue 5" (Research Note, published 22 Sep 2025); volume, issue, DOI and URL are missing. Authors: Ho-Chun Herbert
  Chang, Tracy Weener, Yung-Chun Chen, Sean Noh, Mingyue Zha, Hsuan Lo (Dartmouth); first names are missing.

```bibtex
@article{chang2025homecountries,
  title   = {Do Language Models Favor Their Home Countries? {A}symmetric Propagation of Positive Misinformation and Foreign Influence Audits},
  author  = {Chang, Ho-Chun Herbert and Weener, Tracy and Chen, Yung-Chun and Noh, Sean and Zha, Mingyue and Lo, Hsuan},
  journal = {Harvard Kennedy School Misinformation Review},
  volume  = {6},
  number  = {5},
  year    = {2025},
  doi     = {10.37016/mr-2020-183},
  url     = {https://misinforeview.hks.harvard.edu/article/do-language-models-favor-their-home-countries-asymmetric-propagation-of-positive-misinformation-and-foreign-influence-audits/}
}
```

- **What the paper finds:** four models (DeepSeek, GPT-4o(-mini), Grok, Mistral) rated six world leaders and several
  countries. "although DeepSeek favors China, it also rates some Western leaders highly" (abstract). DeepSeek rates Xi
  and Putin higher than the Western models do but "consistently rates Macron higher than Xi", and "Mistral, based in
  France, also does not rate Macron higher than the other LMs" (Finding 1).
- **Uses in the paper:**
  1. Related: "Geopolitical biases also depend on the developer's country, though not simply as favoritism toward it."
     **SUPPORTS** both clauses.
  2. Appendix: "Chang et al. found that models do not simply favor their home country." **SUPPORTS.** It is a
     four-model audit, but our wording is appropriately modest.
- **Better or additional citations:** none needed. Buyl et al. (above) makes the same point on a larger panel.

---

## pooledayan2026underperformance

- **Verified at:** https://arxiv.org/abs/2406.17737 (v2 comment "Paper accepted at AAAI 2026"; PDF saved as
  `pdfs/pooledayan2026underperformance.pdf`), AAAI proceedings https://ojs.aaai.org/index.php/AAAI/article/view/41259 ,
  Crossref https://api.crossref.org/works/10.1609/aaai.v40i46.41259 .
- **Metadata verdict: OK.** Title, the three authors (full names) and venue are right. Optional: add volume 40, number
  46, pages 39116–39124 and the DOI, and point the URL to the AAAI page instead of arXiv.

```bibtex
@inproceedings{pooledayan2026underperformance,
  title     = {{LLM} Targeted Underperformance Disproportionately Impacts Vulnerable Users},
  author    = {Poole-Dayan, Elinor and Roy, Deb and Kabbara, Jad},
  booktitle = {Proceedings of the AAAI Conference on Artificial Intelligence},
  volume    = {40},
  number    = {46},
  pages     = {39116--39124},
  year      = {2026},
  doi       = {10.1609/aaai.v40i46.41259},
  url       = {https://ojs.aaai.org/index.php/AAAI/article/view/41259}
}
```

- **What the paper finds:** user bios varying English proficiency, education and country of origin (USA, Iran, China)
  are prepended to TruthfulQA and SciQ questions for GPT-4, Claude 3 Opus and Llama 3-8B. Undesirable behaviour
  "occur[s] disproportionately more for users with lower English proficiency, of lower education status, and
  originating from outside the US" (abstract). The country effect is model-specific and depends on education: "Claude
  significantly underperforms for Iran on both datasets", "essentially no significant differences ... across each
  country for GPT-4 and Llama 3" (§5.3), and "we see much less of a difference when they have more formal education"
  (§6). Claude also refuses low-education foreign users about 11% of the time against 3.6% for the control (Table 4).
- **Uses in the paper:**
  1. Intro: "model behavior varies with the language of the request, the origin of the user, and the country of the
     developer [deng, pooledayan, bladon]." **SUPPORTS** "the origin of the user" (country-of-origin effects, including
     refusals).
  2. Related: "serve some users worse than others". **SUPPORTS.**
  3. Appendix: "showed that models underperform for users who are less proficient in English, less educated, or from
     outside the United States." **SUPPORTS.** It is the paper's own summary. If space allows, "(most strongly when these
     traits combine)" would match §6.
- **Better or additional citations: ADD** Li, Chen & Saphra (EMNLP 2024). It measures refusal as a function of the
  user's identity, which is closer to our requester manipulation: "Younger, female, and Asian-American personas are
  more likely to trigger a refusal guardrail", and guardrails are "sycophantic, refusing to comply with requests for a
  political position the user is likely to disagree with" (abstract, GPT-3.5). Poole-Dayan et al. themselves cite it as
  corroborating evidence (§6). It fits the related-work clause ("serve some users worse than others [pooledayan] and
  refuse some users more than others [li]") and the intro's "type of requester". Verified at
  https://aclanthology.org/2024.emnlp-main.363/ (`.bib` and PDF, saved as `pdfs/candidate_li2024chargers.pdf`);
  arXiv 2407.06866. It does not vary nationality, so it complements rather than replaces our citations.

```bibtex
@inproceedings{li2024chargers,
  title     = {{C}hat{GPT} Doesn't Trust Chargers Fans: Guardrail Sensitivity in Context},
  author    = {Li, Victoria R. and Chen, Yida and Saphra, Naomi},
  booktitle = {Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing},
  pages     = {6327--6345},
  year      = {2024},
  publisher = {Association for Computational Linguistics},
  doi       = {10.18653/v1/2024.emnlp-main.363},
  url       = {https://aclanthology.org/2024.emnlp-main.363/}
}
```

---

## liu2025agentic

- **Verified at:** https://arxiv.org/abs/2502.17945 (v2 comment "Accepted to ACL 2025 Findings"), ACL Anthology
  https://aclanthology.org/2025.findings-acl.1355/ (`.bib`, PDF saved as `pdfs/liu2025agentic.pdf`), Crossref
  https://api.crossref.org/works/10.18653/v1/2025.findings-acl.1355 .
- **Metadata verdict: WRONG.**
  - **Title:** our entry has only the subtitle, which is what the arXiv metadata shows. The published paper has a main
    title. Anthology and Crossref record: "7 Points to Tsinghua but 10 Points to 清华? Assessing Large Language Models
    in Agentic Multilingual National Bias". The printed PDF (arXiv v2 and the Anthology PDF) orders the subtitle
    differently: "... Assessing Agentic Large Language Models in Multilingual National Bias". I recommend the
    Anthology/DOI form, which indexers (Crossref, DBLP, Semantic Scholar) will match.
  - **Venue:** it is Findings of ACL 2025 (pp. 26430–26442), not only an arXiv preprint.
  - **Authors:** Qianying Liu, Katrina Qiyao Wang, Fei Cheng, Sadao Kurohashi. Only Kurohashi has a first name in our
    entry, which renders inconsistently ("Liu, Wang, Cheng, and Sadao Kurohashi").
  - **LaTeX:** the title contains Chinese characters, and `main.tex` compiles with pdfLaTeX and no CJK support. I
    tested the entry below in a scratch copy with the official `iclr2027_conference.bst`: it compiles with MiKTeX
    pdfLaTeX, and the glyphs are embedded, if you add `\usepackage{CJKutf8}` to `main.tex` and keep the **double**
    braces. With single braces BibTeX lowercases `CJK`/`UTF8` and the compile fails.

```bibtex
@inproceedings{liu2025agentic,
  title     = {7 Points to {T}singhua but 10 Points to {{\begin{CJK}{UTF8}{gbsn}清华\end{CJK}}}? {A}ssessing Large Language Models in Agentic Multilingual National Bias},
  author    = {Liu, Qianying and Wang, Katrina Qiyao and Cheng, Fei and Kurohashi, Sadao},
  booktitle = {Findings of the Association for Computational Linguistics: ACL 2025},
  pages     = {26430--26442},
  year      = {2025},
  address   = {Vienna, Austria},
  publisher = {Association for Computational Linguistics},
  doi       = {10.18653/v1/2025.findings-acl.1355},
  url       = {https://aclanthology.org/2025.findings-acl.1355/}
}
```

- **What the paper finds:** GPT-3.5, GPT-4 and Claude 3.5 Sonnet act as advisers (university application, relocation,
  travel), scoring triplets of options in six languages. "local language bias is prevalent across different tasks":
  models give higher scores to a language's own country when prompted in that language (§4.2). Chain-of-thought
  prompting often increases the bias in non-English languages, and user gender modulates it (§4.3).
- **Uses in the paper:**
  1. Intro, list of documented biases (nationality, language). **SUPPORTS.**
  2. Appendix: "Liu et al. measured national bias in personalized advice across languages." **SUPPORTS.** The paper uses
     "providing personalized advice" in its abstract.
- **Better or additional citations:** none needed.

---

## williams2025election

- **Verified at:** Crossref https://api.crossref.org/works?query.bibliographic=... giving DOI 10.1371/journal.pone.0317421 ;
  PLOS ONE PDF https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0317421&type=printable (saved as
  `pdfs/williams2025election.pdf`); arXiv https://arxiv.org/abs/2408.06731 (v1, Aug 2024, same title).
- **Metadata verdict: MINOR.** Title, all ten authors in order, journal and year are right (PLOS ONE 20(3): e0317421,
  published 17 Mar 2025). First names are missing, as are volume, issue, article number and DOI, and the URL points to
  arXiv instead of the published version.

```bibtex
@article{williams2025election,
  title   = {Large Language Models Can Consistently Generate High-Quality Content for Election Disinformation Operations},
  author  = {Williams, Angus R. and Burke-Moore, Liam and Chan, Ryan Sze-Yin and Enock, Florence E. and Nanni, Federico and Sippy, Tvesha and Chung, Yi-Ling and Gabasova, Evelina and Hackenburg, Kobi and Bright, Jonathan},
  journal = {PLOS ONE},
  volume  = {20},
  number  = {3},
  pages   = {e0317421},
  year    = {2025},
  doi     = {10.1371/journal.pone.0317421},
  url     = {https://doi.org/10.1371/journal.pone.0317421}
}
```

- **What the paper finds:** DisElect has 2,200 malicious UK election-disinformation prompts, with a left- or
  right-wing persona and, in DisElect.MP, a targeted MP. "most models broadly comply" (abstract). Only three of the 13
  models (Llama 2, Gemma, Gemini 1.0 Pro) refuse more than 10% of prompts. Among those three, "all models are much more
  likely to refuse when prompted to use a right-wing persona than a left-wing persona", and they are more likely to
  refuse "for a female MP than a male MP, and for a Labour MP than a Conservative (or other) MP" (section "What drives
  refusal?").
- **Uses in the paper:**
  1. Appendix: "Williams et al. showed that models generate election disinformation more readily for some beneficiaries
     than for others." **PARTIAL.**
     1. The asymmetry is found only in the 3 of 13 models that refuse at all; most models comply regardless.
     2. "Beneficiaries" is our reading. What varies is the political perspective the content is written from (right-
        vs left-wing persona) and the MP it targets (party, gender).

     Suggested wording, close to ours: "Williams et al. showed that the models that refuse to generate election
     disinformation do so unevenly: more often when it is written from a right-wing than a left-wing perspective, and
     when it targets female or Labour MPs."
  2. Risk to flag: election disinformation against a named MP is arguably a power-shifting request. The related-work
     section says "All of this has been measured on requests that do not shift power (see Appendix)", and the appendix
     paragraph that points there includes Williams. The appendix closes more carefully ("none of these studies places a
     nationality on both sides of a request that moves power between them"), which is true of Williams. Check that the
     related-work wording does not overclaim; for example: "None of this work places a nationality on both sides of a
     request that moves power between them."
- **Better or additional citations:** none needed. This is the right primary source for the claim once reworded.

---

## Summary table

| bibkey | Metadata verdict | Relevance verdict | Action needed |
|---|---|---|---|
| khorramrouz2026selective | MINOR (first names; add pages, DOI) | Intro SUPPORTS; related PARTIAL (cited under "identity of the user", but it is the *targeted* group); appendix SUPPORTS | Replace entry; reword the related-work lead-in ("the identities involved matter as well") |
| pan2026censorship | MINOR (first names; add pgag013, DOI) | Intro SUPPORTS; related SUPPORTS (political more than geopolitical); appendix SUPPORTS (tautological wording) | Replace entry; optionally reword the appendix sentence |
| haslett2025madeinchina | MINOR (title is "Made-in China", not "Made-in-China"; first names) | Related PARTIAL (values, not geopolitical bias); appendix SUPPORTS | Replace entry; consider "Geopolitical and value biases" in related work |
| bladon2026geopolitical | MINOR (first names; unreviewed preprint) | Intro SUPPORTS (weak evidence); related SUPPORTS; appendix PARTIAL (language amplification not significant at population level) | Replace entry; reword to "the language of the prompt can amplify it"; ADD buyl2026ideology (peer-reviewed) |
| chang2025homecountries | MINOR (first names; add vol 6, no 5, DOI, URL) | Related SUPPORTS; appendix SUPPORTS | Replace entry |
| pooledayan2026underperformance | OK (optionally add vol 40, no 46, pp. 39116–39124, DOI, AAAI URL) | Intro SUPPORTS; related SUPPORTS; appendix SUPPORTS | Optional enrichment; ADD li2024chargers for user identity and refusal |
| liu2025agentic | WRONG (main title missing; venue is Findings of ACL 2025, pp. 26430–26442; first names) | Intro SUPPORTS; appendix SUPPORTS | Replace entry; add `\usepackage{CJKutf8}` (tested) or the compile breaks |
| williams2025election | MINOR (first names; add 20(3) e0317421, DOI; URL to PLOS) | Appendix PARTIAL (asymmetry only in the 3 of 13 refusing models; it is persona/target, not "beneficiaries") | Replace entry; reword the appendix sentence; check that the related-work "requests that do not shift power" claim does not cover election disinformation |

New entries proposed (both verified, ADD): `buyl2026ideology` (npj Artificial Intelligence 2026) and `li2024chargers` (EMNLP 2024).
