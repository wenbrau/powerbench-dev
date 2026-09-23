# Bibliography audit, group 3: multilingual safety, global opinions, geopolitical bias

Auditor: Claude (agent), 2026-09-23. Protocol: `paper/iclr2027/bibliography/AUDIT_INSTRUCTIONS.md`.

References audited: `yong2023lowresource`, `deng2024multilingual`, `wang2024alllanguages`, `yong2025state`,
`oppong2026illusion`, `marx2026multilingual`, `li2024thisland`, `durmus2023globalopinion`.

The citing sentences were taken from `citation_map.md` and checked against the current sources
(`sections/introduction.tex` l.4, `sections/related.tex` l.4, `sections/appendix.tex` l.349 and l.351). The phrase
"later work confirmed systematic safety gaps across languages" that appears in the task description is **not in the
current source**. The current equivalent is "\citet{wang2024alllanguages} found systematic gaps across languages in a
multilingual safety benchmark" (appendix l.349), and that is the sentence audited below.

All PDFs read are in `paper/iclr2027/bibliography/pdfs/<bibkey>.pdf`. Two candidate additions are saved as
`candidate_alkhamissi2024cultural.pdf` and `candidate_shen2024languagebarrier.pdf`.

The compiled bibliography (`main.pdf`) was also checked. The .bst lowercases titles, so unbraced acronyms print in
lowercase, and entries that give authors as bare surnames print as, e.g., "Marx and Dunaiski." and "Oppong, Sahil,
Belay, ...".

---

## yong2023lowresource

- **Verified at:** https://export.arxiv.org/api/query?id_list=2310.02446 ; https://arxiv.org/abs/2310.02446 ; PDF v2
  (`pdfs/yong2023lowresource.pdf`).
- **Metadata verdict: OK.** Title "Low-Resource Languages Jailbreak GPT-4" and authors Zheng-Xin Yong, Cristina
  Menghini, Stephen H. Bach match arXiv. Year 2023 (v1 2023-10-03). The arXiv comment reads "NeurIPS Workshop on
  Socially Responsible Language Modelling Research (SoLaR) 2023. Best Paper Award". That is a workshop, and no archival
  proceedings version was found, so `@misc` + arXiv is appropriate. Optionally, the workshop can be recorded:
  ```bibtex
  @misc{yong2023lowresource,
    title  = {Low-Resource Languages Jailbreak {GPT}-4},
    author = {Yong, Zheng-Xin and Menghini, Cristina and Bach, Stephen H.},
    year   = {2023},
    note   = {NeurIPS 2023 Workshop on Socially Responsible Language Modelling Research (SoLaR). arXiv:2310.02446},
    url    = {https://arxiv.org/abs/2310.02446}
  }
  ```
- **Uses in the paper:**
  1. related.tex: "Translating an unsafe request into a low-resource language can bypass refusal \citep{yong2023lowresource, ...}".
     **SUPPORTS.** "simply translating unsafe inputs to low-resource natural languages using Google Translate is
     sufficient to bypass safeguards" (Sec. 1). The bypass rate rises "from <1% to 79%" (Sec. 1, Table 1). This is the
     original and canonical source for the claim.
  2. appendix.tex: "\citet{yong2023lowresource} showed that low-resource languages can jailbreak models that refuse the
     same request in English." **PARTIAL (slight overgeneralisation).** Only one model was tested, GPT-4
     (gpt-4-0613, Sec. 3.1). The limitations section says so explicitly: "particularly the most recent stable version
     of GPT-4". In English it rejected 99.04% of the prompts (Table 1). "models" should be "GPT-4".
     Proposed wording: "\citet{yong2023lowresource} showed that translating unsafe requests into low-resource languages
     can jailbreak GPT-4, which refuses the same requests in English."
- **Better or additional citations:** none needed. This is the original source.

## deng2024multilingual

- **Verified at:** https://export.arxiv.org/api/query?id_list=2310.06474 (comment "ICLR 2024") ;
  https://proceedings.iclr.cc/paper_files/paper/2024/hash/6b396f766a50e0853a5164e68048540c-Abstract-Conference.html
  (lists "Yue Deng, Wenxuan Zhang, Sinno Jialin Pan, Lidong Bing", "International Conference on Learning
  Representations 2024 (ICLR 2024)") ; PDF arXiv v3 with the header "Published as a conference paper at ICLR 2024".
- **Metadata verdict: OK.** Title, authors, venue and year all match. Optionally, the url could point to the
  proceedings page above instead of arXiv.
- **Uses in the paper:**
  1. introduction.tex: "We already know that model behavior varies with the language of the request, ...
     \citep{deng2024multilingual, ...}". **SUPPORTS.** "the rate of unsafe content increases as the availability of
     languages decreases" (Abstract). Table 1 gives unsafe rates by language for ChatGPT and GPT-4.
  2. related.tex: "Translating an unsafe request into a low-resource language can bypass refusal". **SUPPORTS.** In
     the unintentional scenario, "low-resource languages exhibit about three times the likelihood of encountering
     harmful content" (Abstract). Sec. 3.3 shows that machine translation is enough: "machine translation can suffice
     as a means for jailbreaking".
  3. appendix.tex: "\citet{deng2024multilingual} found that multilingual jailbreaks arise both from translated unsafe
     requests and from multilingual prompting". **PARTIAL (the second scenario is misnamed).** Deng et al. define two
     scenarios, and both use translated unsafe requests:
     - *unintentional*: the translated harmful prompt is sent alone;
     - *intentional*: an English jailbreak instruction (AIM) is concatenated with the translated harmful prompt
       (Sec. 3.1, "We take the English version of AIM and concatenate it with the translated harmful prompts").

     "Multilingual prompting" does not describe the intentional scenario, and the sentence implies two different kinds
     of input when both are translated requests. Proposed wording: "\citet{deng2024multilingual} found that non-English
     prompts bypass safety mechanisms both unintentionally, when a user simply asks in a lower-resource language, and
     intentionally, when a translated harmful request is combined with a malicious jailbreak instruction".
- **Better or additional citations:** none needed.

## wang2024alllanguages

- **Verified at:** https://aclanthology.org/2024.findings-acl.349/ (and its `.bib`) ; published PDF
  https://aclanthology.org/2024.findings-acl.349.pdf ; https://export.arxiv.org/api/query?id_list=2310.00905
  (comment "Accepted by ACL 2024 Findings").
- **Metadata verdict: WRONG (title).** The venue is correct: Findings of ACL 2024, pp. 5865–5877. The title in
  refs.bib, "... On the Multilingual Safety of Large Language Models", is the **arXiv** title. The published Findings
  paper, which is the one the entry cites, is titled "**All Languages Matter: On the Multilingual Safety of LLMs**" in
  the Anthology record and in the PDF header. The authors match; the PDF gives "Michael R. Lyu". Corrected entry:
  ```bibtex
  @inproceedings{wang2024alllanguages,
    title     = {All Languages Matter: On the Multilingual Safety of {LLMs}},
    author    = {Wang, Wenxuan and Tu, Zhaopeng and Chen, Chang and Yuan, Youliang and Huang, Jen-tse and Jiao, Wenxiang and Lyu, Michael R.},
    booktitle = {Findings of the Association for Computational Linguistics: ACL 2024},
    pages     = {5865--5877},
    year      = {2024},
    address   = {Bangkok, Thailand},
    publisher = {Association for Computational Linguistics},
    doi       = {10.18653/v1/2024.findings-acl.349},
    url       = {https://aclanthology.org/2024.findings-acl.349/}
  }
  ```
- **Uses in the paper:**
  1. related.tex: "Translating an unsafe request into a low-resource language can bypass refusal". **SUPPORTS (with a
     nuance).** "all LLMs produce significantly more unsafe responses for non-English queries than English ones"
     (Abstract). The ten XSafety languages are widely spoken, though. The authors write that they "are not low-resource
     languages in the real world" but are "relatively low-resource in the pretraining data" (Sec. 3). They also report
     that "the most unsafe languages ... are generally the lowest-resource languages in the pretraining data"
     (Sec. 4.2). Within the multi-citation sentence this is acceptable.
  2. appendix.tex: "\citet{wang2024alllanguages} found systematic gaps across languages in a multilingual safety
     benchmark". **SUPPORTS.** "The unsafety ratios of non-English languages are higher than English in all cases"
     (Sec. 4.2, Table 3, four LLMs).
- **Better or additional citations:** none needed.

## yong2025state

- **Verified at:** https://aclanthology.org/2025.emnlp-main.800/ (and its `.bib`) ; published PDF
  https://aclanthology.org/2025.emnlp-main.800.pdf (header "Proceedings of the 2025 Conference on Empirical Methods in
  Natural Language Processing, pages 15845–15860") ; https://export.arxiv.org/api/query?id_list=2505.24119.
- **Metadata verdict: OK.** The venue is the EMNLP 2025 main conference, as stated. The authors in the published PDF
  are Zheng-Xin Yong, Beyza Ermis, Marzieh Fadaee, Stephen H. Bach and Julia Kreutzer, matching refs.bib. The
  Anthology metadata writes "Zheng Xin" and "Stephen", but the PDF and arXiv use the forms in refs.bib. The PDF title
  capitalises "The Language Gap To Mitigating It"; that is capitalisation only, and the .bst lowercases it anyway.
  Optionally add `pages = {15845--15860}` and `doi = {10.18653/v1/2025.emnlp-main.800}`.
- **Uses in the paper:**
  1. related.tex: "Translating an unsafe request into a low-resource language can bypass refusal". **SUPPORTS**, as a
     survey. "Several commercial LLMs have demonstrated significantly weaker safety performance when prompted in
     non-English languages, producing harmful content ... that would be filtered in English contexts" (Sec. 1). Sec. 3.1
     adds: "models can bypass safety guardrails when prompted in languages underrepresented in pretraining".
  2. appendix.tex: "\citet{yong2025state} survey the field." **SUPPORTS.** It is a "systematic review of nearly 300
     publications from 2020–2024" (Abstract).
- **Better or additional citations:** none needed. A minor point: the next appendix sentence, "All of these studies
  translate requests that are unsafe by construction", also covers this survey, which translates nothing. "All of these
  empirical studies" would be exact. This is optional.

## oppong2026illusion

- **Verified at:** https://export.arxiv.org/api/query?id_list=2608.11146 ; https://arxiv.org/abs/2608.11146 ; PDF v1
  (`pdfs/oppong2026illusion.pdf`, 22 pp., submitted 2026-08-11).
- **Metadata verdict: MINOR (author first names missing).** The work exists. The title "The Illusion of Cross-Lingual
  Safety in Low-Resource Languages" matches exactly, and the 15 authors are listed in the correct order. refs.bib gives
  only surnames, however, so the bibliography prints "Oppong, Sahil, Belay, ...". Full names from arXiv and the PDF:
  Abigail Oppong, P Sam Sahil, Tadesse Destaw Belay, Maryam Ibrahim Mukhtar, Esmael Ahmed Abdu, Tassallah Abdullahi,
  Jessica Oparebea, Saminu Mohammad Aliyu, Idris Abdulmumin, Abubakar Juma Chilala, Nicholaus Dismas Ladislaus, Alfred
  Malengo Kondoro, Lemofouet Valdini Douglace, Shamsuddeen Hassan Muhammad, Seid Muhie Yimam.

  One name is uncertain. The PDF prints "LEMOFOUET VALDINI DOUGLACE" in capitals, so the family name could be
  Lemofouet. The entry below follows the arXiv order, which makes Douglace the surname; that is how refs.bib already
  has it. Corrected entry:
  ```bibtex
  @misc{oppong2026illusion,
    title  = {The Illusion of Cross-Lingual Safety in Low-Resource Languages},
    author = {Oppong, Abigail and Sahil, P Sam and Belay, Tadesse Destaw and Mukhtar, Maryam Ibrahim and Abdu, Esmael Ahmed and Abdullahi, Tassallah and Oparebea, Jessica and Aliyu, Saminu Mohammad and Abdulmumin, Idris and Chilala, Abubakar Juma and Ladislaus, Nicholaus Dismas and Kondoro, Alfred Malengo and Douglace, Lemofouet Valdini and Muhammad, Shamsuddeen Hassan and Yimam, Seid Muhie},
    year   = {2026},
    note   = {arXiv:2608.11146},
    url    = {https://arxiv.org/abs/2608.11146}
  }
  ```
- **Uses in the paper:**
  1. appendix.tex: "\citet{oppong2026illusion} located the low-resource failure in the model's decision and not in its
     comprehension of the request". **PARTIAL.**

     What supports it:
     - The Abstract: literal and localised prompts are "semantically aligned ... suggesting models encode the concepts
       without routing them to safety mechanisms".
     - Sec. 5.1: "The model clearly understands the language and intent; the failure is specifically the routing of
       that understood intent to the refusal mechanism". This is said of one Mistral–Swahili example.
     - Sec. 5.2: "models overwhelmingly failed to route comprehension to safety mechanisms".

     What is off:
     - (a) **Setting.** This is a hidden-state (latent geometry) study of four **7–8B open-weight models** (Mistral,
       Llama, Qwen2.5, AfriqueQwen) in **four African languages** (Twi, Hausa, Amharic, Swahili). The sentence reads
       as a general finding about "the low-resource failure".
     - (b) **Strength.** The authors call the evidence correlational: "Rather than asserting causal claims" (Sec. 6),
       and the framework is "observational in nature" (Sec. 7).
     - (c) **Comprehension is not ruled out.** Their own qualitative analysis reports "weak semantic grounding" and
       "limited cultural and contextual understanding" (Sec. 5.1). It also reports Amharic tokenisation failures that
       "likely distort geometric analysis". Their answer to RQ3 is that failures "arise from both structural
       cross-lingual mapping limitations and prompt form sensitivity" (Sec. 5).
     - (d) **Term.** "Decision" is not their word. They speak of *routing* to the refusal or safety mechanism.

     Proposed wording, close to ours: "\citet{oppong2026illusion} found, in the hidden states of four 7--8B open
     models, that harmful prompts in four African languages are encoded according to their meaning but are not routed
     to the refusal mechanism learned in English, placing much of the failure in the model's safety routing rather
     than in its comprehension of the request".
- **Better or additional citations:** none required. Other work in the same literature places part of the low-resource
  failure in comprehension, which argues for the hedged wording above:
  - Yong et al. (2023) report many UNCLEAR responses for Hmong and Guarani (Table 1).
  - Marx & Dunaiski (2026) attribute low jailbreak rates in isiXhosa and isiZulu to "poor translations ... rather than
    stronger safety mechanisms" (Sec. 4.3).
  - Shen et al. (2024, below) find "more irrelevant responses to malicious prompts in lower-resource languages".

## marx2026multilingual

- **Verified at:** https://export.arxiv.org/api/query?id_list=2605.18239 ; https://arxiv.org/abs/2605.18239 ; PDF v1
  (`pdfs/marx2026multilingual.pdf`, 12 pp., submitted 2026-05-18).
- **Metadata verdict: MINOR (author first names missing).** The work exists. arXiv gives the title in sentence case,
  "Multilingual jailbreaking of LLMs using low-resource languages"; refs.bib has it in title case, which is fine. The
  authors are **Dylan Marx** and **Marcel Dunaiski** (Stellenbosch University). refs.bib has only "Marx and Dunaiski",
  and the bibliography prints "Marx and Dunaiski." Corrected entry:
  ```bibtex
  @misc{marx2026multilingual,
    title  = {Multilingual Jailbreaking of {LLMs} Using Low-Resource Languages},
    author = {Marx, Dylan and Dunaiski, Marcel},
    year   = {2026},
    note   = {arXiv:2605.18239},
    url    = {https://arxiv.org/abs/2605.18239}
  }
  ```
- **Uses in the paper:**
  1. appendix.tex: "\citet{marx2026multilingual} found that susceptibility varies by developer." **PARTIAL.**

     What supports it: "We found variation in model robustness where Claude-3.5-Haiku demonstrated the strongest
     resistance to multilingual multi-turn jailbreaks, while DeepSeek-V3 and GPT-4o-mini showed the highest
     vulnerability" (Sec. 6).

     What is off:
     - (a) They frame the result by *model*, not by developer, and there is no developer-level analysis. The models
       are GPT-4o, GPT-4o-mini, Gemini-2.0-flash, Gemini-2.0-flash-lite, Claude-3.5-Haiku, DeepSeek-V3 and
       Grok-3-mini, i.e. seven models from five developers (Sec. 3.3).
     - (b) The variation is in **multi-turn** attacks. For single-turn translation, harmful rates were low for all
       models (only DeepSeek exceeded 10%), and "the language effects for individual models were not significant"
       (Sec. 4.1).

     Proposed wording: "\citet{marx2026multilingual} found that susceptibility to multi-turn jailbreaks in these
     languages varies across commercial models from different developers".

  **Important nuance for the body sentence.** Marx & Dunaiski report that on 2024–25 commercial models "Simply
  translating harmful prompts into low-resource languages no longer effectively bypasses LLM safety guardrails"
  (Sec. 6). The abstract says "Single-turn translation attacks proved ineffective". This does not make
  related.tex's "Translating an unsafe request into a low-resource language can bypass refusal" false, because the
  cited studies did show it on their models. But it is a recent result the paper already cites, and it qualifies the
  claim. Two options:
  - related.tex: "... can bypass refusal \citep{...}, although on recent models single-turn translation alone has
    become less effective \citep{marx2026multilingual}";
  - appendix, as a merged sentence: "\citet{marx2026multilingual} found that single-turn translation no longer
    bypasses recent commercial models, whereas multi-turn jailbreaks in the same languages still do, with
    susceptibility varying across models from different developers."
- **Better or additional citations:** none.

## li2024thisland

- **Verified at:** https://aclanthology.org/2024.naacl-long.213/ (and its `.bib`) ; published PDF
  https://aclanthology.org/2024.naacl-long.213.pdf ; https://export.arxiv.org/api/query?id_list=2305.14610 (comment
  "NAACL 2024 main conference").
- **Metadata verdict: MINOR.** Authors, year and venue (NAACL 2024) are correct. The title matches the **published**
  version: "This Land is {Your, My} Land: Evaluating Geopolitical Bias in Language Models through Territorial Disputes".
  The printed braces are in the published PDF title, so `\{Your, My\}` is right. Two things to fix:
  - (a) The `url` points to arXiv, where the title is different: "... Evaluating Geopolitical Biases in Language
    Models". It should point to the Anthology.
  - (b) The booktitle is truncated. The official one is "Proceedings of the 2024 Conference of the North American
    Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers)",
    pp. 3855–3871.

  Corrected entry:
  ```bibtex
  @inproceedings{li2024thisland,
    title     = {This Land is \{Your, My\} Land: Evaluating Geopolitical Bias in Language Models through Territorial Disputes},
    author    = {Li, Bryan and Haider, Samar and Callison-Burch, Chris},
    booktitle = {Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers)},
    pages     = {3855--3871},
    year      = {2024},
    address   = {Mexico City, Mexico},
    publisher = {Association for Computational Linguistics},
    doi       = {10.18653/v1/2024.naacl-long.213},
    url       = {https://aclanthology.org/2024.naacl-long.213/}
  }
  ```
- **Uses in the paper:**
  1. related.tex: "the identity of the user matters as well: models ... take sides in territorial disputes depending
     on the prompt's language \citep{durmus2023globalopinion, li2024thisland}". **SUPPORTS.** "LLMs recall certain
     geographical knowledge inconsistently when queried in different languages—a phenomenon we term geopolitical bias"
     (Abstract). They also "tailor their responses depending on cues from the interaction context" (Abstract), which
     fits the "identity of the user" framing. Several models were tested: GPT-4, BLOOM, BLOOMZ.
  2. appendix.tex: "\citet{li2024thisland} [found] that they take sides in territorial disputes depending on the
     language of the prompt." **SUPPORTS.** Same evidence; Sec. 8: "they exhibit substantial geopolitical bias and
     recall information differently across languages".
- **Better or additional citations:** none needed.

## durmus2023globalopinion

- **Verified at:** https://export.arxiv.org/api/query?id_list=2306.16388 ; PDF arXiv v2 (2024-04-12) ;
  https://colmweb.org/2024/AcceptedPapers.html. That page lists "Towards Measuring the Representation of Subjective
  Global Opinions in Language Models" with the same 18 authors, marked "Spotlight", and links to
  https://openreview.net/forum?id=zl16jLb91v; the OpenReview page itself was not opened.
- **Metadata verdict: MINOR (peer-reviewed version exists).** The title and the 18 authors in order match arXiv. The
  paper was **published at COLM 2024** (the First Conference on Language Modeling), so it should be cited as such
  rather than as a 2023 arXiv preprint. The in-text citation then becomes "Durmus et al., 2024"; the bibkey can stay.
  Corrected entry:
  ```bibtex
  @inproceedings{durmus2023globalopinion,
    title     = {Towards Measuring the Representation of Subjective Global Opinions in Language Models},
    author    = {Durmus, Esin and Nguyen, Karina and Liao, Thomas I. and Schiefer, Nicholas and Askell, Amanda and Bakhtin, Anton and Chen, Carol and Hatfield-Dodds, Zac and Hernandez, Danny and Joseph, Nicholas and Lovitt, Liane and McCandlish, Sam and Sikder, Orowa and Tamkin, Alex and Thamkul, Janel and Kaplan, Jared and Clark, Jack and Ganguli, Deep},
    booktitle = {Conference on Language Modeling (COLM)},
    year      = {2024},
    url       = {https://openreview.net/forum?id=zl16jLb91v}
  }
  ```
- **Uses in the paper:**
  1. related.tex: "the identity of the user matters as well: models represent some countries' opinions better and take
     sides in territorial disputes depending on the prompt's language \citep{durmus2023globalopinion, li2024thisland}".
     **PARTIAL.**

     What supports it: "By default, LLM responses tend to be more similar to the opinions of certain populations, such
     as those from the USA, and some European and South American countries" (Abstract).

     What is off:
     - (a) One model was evaluated, not several: "we evaluate our framework using a single language model"
       (footnote 6).
     - (b) The study does not vary the user's identity. It measures default opinions, and in the cross-national
       condition it asks the model to adopt a country's perspective. So it does not show that "the identity of the
       user matters".
     - (c) Durmus et al. found the **opposite** for prompt language: "With Linguistic Prompting (LP), model responses
       do not become more similar to the opinions of the populations that predominantly speak the target languages"
       (Sec. 3). With one joint citation at the end of the sentence, a reader can attach "depending on the prompt's
       language" to Durmus.

     Proposed wording: "..., and who is involved matters as well: models represent some countries' opinions better
     than others \citep{durmus2023globalopinion}, take sides in territorial disputes depending on the prompt's
     language \citep{li2024thisland}, serve some users worse than others ...". At minimum, split the two citations.
  2. appendix.tex: "\citet{durmus2023globalopinion} found that models represent the opinions of some countries better
     than others". **PARTIAL (minor).** The substance is right, but they studied a single model. Proposed wording:
     "\citet{durmus2023globalopinion} found that a model's answers to cross-national survey questions resemble the
     opinions of some countries more than others".
- **Better or additional citations:**
  - **ADD (optional), for opinions that depend on the prompt's language:** AlKhamissi et al. (2024). It finds that
    models "demonstrate greater cultural alignment ... when prompted with the dominant language of a specific culture"
    (Abstract; Egypt/US survey replication, several models). The paper does not claim this for opinions now; if it
    wants to, this is the source, since Durmus found the opposite. Verified at https://aclanthology.org/2024.acl-long.671/
    (PDF saved as `pdfs/candidate_alkhamissi2024cultural.pdf`).
    ```bibtex
    @inproceedings{alkhamissi2024cultural,
      title     = {Investigating Cultural Alignment of Large Language Models},
      author    = {AlKhamissi, Badr and ElNokrashy, Muhammad and AlKhamissi, Mai and Diab, Mona},
      booktitle = {Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)},
      pages     = {12404--12422},
      year      = {2024},
      address   = {Bangkok, Thailand},
      publisher = {Association for Computational Linguistics},
      doi       = {10.18653/v1/2024.acl-long.671},
      url       = {https://aclanthology.org/2024.acl-long.671/}
    }
    ```
    The Anthology writes "Alkhamissi, Mai"; the PDF writes "Mai AlKhamissi".
  - Durmus et al. itself is the canonical source for "some countries' opinions are represented better". Keep it.

## Additional candidate for the body sentence on translation (optional)

- **ADD (optional), not needed:** Shen et al. (2024). It compares "the same set of malicious prompts written in
  higher- vs. lower-resource languages" and finds that "LLMs tend to generate unsafe responses much more often" and
  "more irrelevant responses" in lower-resource languages (Abstract). It would be a fifth citation for "Translating an
  unsafe request into a low-resource language can bypass refusal". Its "irrelevant responses" finding is also a
  comprehension-side counterpoint to the Oppong sentence. Verified at https://aclanthology.org/2024.findings-acl.156/
  (PDF saved as `pdfs/candidate_shen2024languagebarrier.pdf`).
  ```bibtex
  @inproceedings{shen2024languagebarrier,
    title     = {The Language Barrier: Dissecting Safety Challenges of {LLMs} in Multilingual Contexts},
    author    = {Shen, Lingfeng and Tan, Weiting and Chen, Sihao and Chen, Yunmo and Zhang, Jingyu and Xu, Haoran and Zheng, Boyuan and Koehn, Philipp and Khashabi, Daniel},
    booktitle = {Findings of the Association for Computational Linguistics: ACL 2024},
    pages     = {2668--2680},
    year      = {2024},
    address   = {Bangkok, Thailand},
    publisher = {Association for Computational Linguistics},
    doi       = {10.18653/v1/2024.findings-acl.156},
    url       = {https://aclanthology.org/2024.findings-acl.156/}
  }
  ```

---

## Summary table

| bibkey | metadata verdict | relevance verdict | action needed |
|---|---|---|---|
| yong2023lowresource | OK (SoLaR 2023 workshop, arXiv) | related: SUPPORTS; appendix: PARTIAL (only GPT-4 tested, not "models") | Appendix: "can jailbreak GPT-4, which refuses the same requests in English". Optionally note the SoLaR workshop in the bib. |
| deng2024multilingual | OK (ICLR 2024 verified) | intro: SUPPORTS; related: SUPPORTS; appendix: PARTIAL | Reword the appendix: the two scenarios are an unintentional non-English prompt and a translated request plus an English jailbreak instruction, not "multilingual prompting". |
| wang2024alllanguages | **WRONG title** | related: SUPPORTS (languages are widely spoken, "relatively low-resource in the pretraining data"); appendix: SUPPORTS | Title must be "All Languages Matter: On the Multilingual Safety of {LLMs}" (Findings version); add pages 5865–5877 and DOI. |
| yong2025state | OK (EMNLP 2025 main, pp. 15845–15860) | related: SUPPORTS (as survey); appendix: SUPPORTS | Optional: add pages/DOI; "All of these empirical studies" in the next sentence. |
| oppong2026illusion | MINOR (exists; title exact; first names missing) | appendix: PARTIAL (hidden-state, correlational, four 7–8B open models, four African languages; "routing", not "decision"; comprehension issues also reported) | Add full author names; hedge and scope the sentence (wording above). |
| marx2026multilingual | MINOR (exists; first names Dylan, Marcel missing) | appendix: PARTIAL (variation by model, for multi-turn attacks; not analysed by developer) | Add first names; reword to "across commercial models from different developers". Consider their finding that single-turn translation "no longer" bypasses recent models when wording related.tex. |
| li2024thisland | MINOR (url is arXiv, whose title differs; booktitle truncated) | related: SUPPORTS; appendix: SUPPORTS | Point url to the Anthology; full NAACL booktitle, pages 3855–3871, DOI. |
| durmus2023globalopinion | MINOR (published at COLM 2024, Spotlight) | related: PARTIAL (single model; does not vary user identity; found prompt language does *not* shift opinions); appendix: PARTIAL (single model) | Cite as COLM 2024. Split the related.tex citation so "depending on the prompt's language" attaches only to Li; say "a model" in the appendix. Optional ADD: AlKhamissi et al. 2024. |
