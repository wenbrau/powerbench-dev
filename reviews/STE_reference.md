# ASD-STE100 Simplified Technical English — working reference

A distilled reference to ASD-STE100 (Simplified Technical English, "STE"). Source: the ASD-STE100
Issue 7 standard (2017-01-25), downloaded from ASD. The standard is free (open since Issue 6, 2013).
The current edition is Issue 8 (January 2025); it has 53 writing rules and about 900 approved words.
Issue 7 has the same structure and near-identical rules, so this reference is accurate for both.

STE has two parts: **Part 1 — writing rules** (9 sections) and **Part 2 — a controlled dictionary**
(about 900 approved words, each with one part of speech and one approved meaning). STE was built by
the aerospace industry (AECMA, now ASD) so that non-native readers can understand maintenance
documentation. Its purpose is clear, unambiguous, translatable technical text.

This file states the rules in my own words. It does not copy the standard's example text. For the
authoritative document, use the copy at `scratchpad/ASD-STE100-ISSUE-7.pdf` or download Issue 8 from
asd-ste100.org.

---

## The core idea (two mechanisms)

1. **A controlled dictionary.** You can use a word only if it is one of these:
   - an approved word in the STE dictionary (used only as the approved part of speech and meaning),
   - a "technical name" (a noun from one of 19 category types — parts, tools, materials, systems,
     mathematical/engineering terms, body parts, medical terms, IT terms, and so on),
   - a "technical verb" (a verb from one of 4 category types — manufacturing, computer, description,
     operational).
   When a word is not approved, you find the approved synonym in the dictionary and use that. For
   example, STE uses "start", not "begin", "commence", "initiate", or "originate".

2. **Writing rules.** 53 rules that control grammar, sentence length, sentence structure,
   procedures, descriptions, safety instructions, punctuation, and consistency.

---

## Part 1 — the writing rules, by section

### Section 1 — Words (Rules 1.1–1.14)
- **1.1** Use only words that are approved in the dictionary, technical names, or technical verbs.
- **1.2** Use an approved word only as the part of speech given in the dictionary. ("test" is an
  approved noun, not an approved verb: write "do a test of the system", not "test the system".)
- **1.3** Use an approved word only with its approved meaning. (The approved meaning of "follow" is
  "come after", not "obey": write "obey the safety instructions".)
- **1.4** Use only the approved forms of verbs and adjectives.
- **1.5** You can use a word if it fits a technical-name category.
- **1.6** Use an unapproved dictionary word only when it is a technical name or part of one.
- **1.7** Do not use technical names as verbs. ("oil" is a technical name: write "apply oil to the
  surface", not "oil the surface".)
- **1.8** Use technical names that agree with the approved nomenclature.
- **1.9** When you must select a technical name, use one that is short and easy to understand.
- **1.10** Do not use slang or jargon as technical names.
- **1.11** Do not use different technical names for the same item. (Pick "actuator" and always use
  it; do not also write "servo control unit" or "control unit".)
- **1.12** You can use a verb if it fits a technical-verb category.
- **1.13** Do not use technical verbs as nouns.
- **1.14** Use American English spelling. ("fiber" not "fibre"; "color" not "colour".)

### Section 2 — Noun clusters (Rules 2.1–2.3)
- Do not make a noun cluster of more than three nouns. A long string of stacked nouns ("runway
  light connection resistance test") is ambiguous. Break it up with prepositions and articles.
- When a long noun cluster is a real technical name, define it or hyphenate it, then keep it
  consistent.
- Use articles ("a", "an", "the") and demonstrative adjectives ("this", "these"). Do not drop them.

### Section 3 — Verbs (Rules 3.1–3.7)
- Use only the approved verb forms: the infinitive, the imperative, the simple present tense, the
  simple past tense, and the past participle **as an adjective**.
- Do not use complex or compound verb forms. Do not use the future tense or perfect tenses. Write in
  the simple present or simple past. (Write "if snow falls", not "if it will snow".)
- **Do not use the "-ing" form** (gerund or present participle) as a verb. Use the "-ing" form only
  when it is part of a technical name.
- **3.6** Use only the active voice in procedures. Use the active voice as much as possible in
  descriptions. Use the passive voice only when it is really necessary. (The four methods to make a
  passive sentence active: put the agent first as the subject; change an infinitive to an active
  verb; use the imperative; or use "you"/"we" as the subject.)
- **3.7** Use an approved verb to describe an action — not a noun or another part of speech. (Write
  "the ohmmeter shows 450 ohms", not "the ohmmeter gives an indication of 450 ohms".)

### Section 4 — Sentences (Rules 4.1–4.4)
- **4.1** Write short, clear sentences. Give one piece of specific information. Do not be abstract.
- **4.2** Do not omit words or use contractions to make a sentence shorter. Keep every part — the
  noun, the verb, the subject, and the article. Do not write "don't"; write "do not".
- **4.3** Use a vertical list for complex text. Put a colon before the list. Start each item with an
  uppercase letter. Put a period at the end of a full-sentence item and at the end of the last item.
- **4.4** Use connecting words and phrases to join sentences about related topics. The approved
  connectors include "and", "but", "then", "thus", and "as a result".

### Section 5 — Procedural writing (Rules 5.1–5.5)
- **5.1** Write short sentences. **Use a maximum of 20 words in each sentence.** (This also applies
  to warnings and cautions.)
- **5.2** Write only one instruction per sentence — unless two or more actions occur at the same
  time.
- **5.3** Write instructions in the imperative (command) form. (Write "continue the test", not "the
  test can be continued".)
- **5.4** When you start an instruction with a condition (a dependent phrase or clause), divide the
  condition from the command with a comma. ("When the light comes on, set the switch to NORMAL.")
- **5.5** Write notes to give information only, not instructions. A note must not contain an
  imperative. A note is descriptive text with a maximum of 25 words.

### Section 6 — Descriptive writing (Rules 6.1–6.6)
- **6.1** Give information gradually. Each sentence has only one topic.
- **6.2** Use key words and phrases to organize the text logically. Repeat the key nouns instead of
  replacing them with synonyms; the repetition connects the sentences.
- **6.3** Write short sentences. **Use a maximum of 25 words in each sentence.**
- **6.4** Use paragraphs to group related information. Start each paragraph with a topic sentence.
- **6.5** Make sure that each paragraph has only one topic.
- **6.6** Make sure that no paragraph has more than six sentences.

### Section 7 — Safety instructions (Rules 7.x)
- Put a warning or a caution **before** the step it applies to, never after.
- Start a warning or caution with a clear command or a clear condition. Say exactly what to do or
  not to do and why. Do not hide a negative command inside a vertical list — repeat "do not" in the
  list item.

### Section 8 — Punctuation and word counts (Rules 8.1–8.7)
- Do not use complex punctuation. Avoid the semicolon. Use the colon mainly to introduce a vertical
  list.
- Use the hyphen to join words in a defined technical name; keep it consistent.
- Use parentheses for reference numbers and short clarifications only.
- Use uppercase text for warnings, cautions, placards, and quoted control labels.
- The word-count rules (8.4–8.7) define how you count words toward the 20-word and 25-word limits
  (for example, how hyphenated words and numbers count).

### Section 9 — Writing practices (Rules GR1–GR4 and 9.1–9.4)
- **GR1** Use "that" to introduce a clause. Do not drop it. ("Make sure that the valve is closed.")
- **GR2** Do not use "with" in a way that is ambiguous.
- **GR3** Use a pronoun only when its referent is clear. When in doubt, repeat the noun.
- **GR4** Use "this" and "these" with a noun, not alone. ("This method", not "this".)
- **9.1** Word-for-word replacement: when you swap an unapproved word for the approved one, make sure
  the meaning does not change. If it changes, use a different construction.
- **9.2** Use approved words only with their approved meanings.
- **9.4** Keep a consistent style across the whole document.

---

## Does STE stop "AI slop"? An honest assessment

STE removes many of the exact patterns that mark AI-generated text:
- **It bans hedging and vague abstraction** (Rule 4.1: be specific, not abstract). No "it could be
  argued that…", no "this plays a crucial role".
- **It bans synonym cycling** (Rule 6.2: repeat the key noun). This kills "elegant variation", one
  of the clearest AI tells.
- **It caps sentence length** (20/25 words) and paragraph length (six sentences). This kills the
  long, rolling, subordinate-clause sentences that AI produces.
- **It forces the active voice and real verbs** (Rules 3.6, 3.7). This kills "serves as", "is a
  testament to", and noun-heavy abstraction.
- **It bans jargon and forces one name per thing** (Rules 1.10, 1.11). This kills the
  jargon-for-its-own-sake register.
- **It bans the "-ing" pile-up** (Section 3), which is the AI "…, highlighting…, ensuring…,
  reflecting…" pattern almost exactly.

So the claim has real force: STE compliance removes a large set of AI-slop tells mechanically,
because the rules were designed against the same failures (wordiness, ambiguity, abstraction).

**But STE is not a general anti-slop fix, and it is honest to say why:**
- STE produces a **clipped, instrument-panel register**. It reads as an aircraft maintenance manual,
  because that is what it is for. That register is correct for procedures and reference material. It
  is wrong for a research narrative, an argument, a design rationale, or anything that needs a human
  voice. Forcing STE onto those makes them sound robotic — a different kind of "not human", not a
  fix.
- STE bans contractions and requires every article and "that" (Rules 4.2, GR1). That is the opposite
  of casual natural prose. It trades "sounds like a chatbot" for "sounds like a checklist".
- The ~900-word dictionary is domain-specific (aerospace). Outside that domain you lean on "technical
  names", so the vocabulary control is looser than it looks.

**Verdict.** STE is an excellent forcing function for the parts of our documentation that are
procedures, reference, or instructions — the metaprompt rules, the runbook, the validation checklist,
the pilot-run steps. For those, adhering to STE will measurably reduce slop and improve clarity and
translatability (which matters: our dataset is multilingual). For analytical or narrative docs (the
decision memos, the analysis plan), STE is the wrong register; the better tool there is the plain
anti-slop discipline we already use (short sentences, real verbs, no hedging, specific claims), not
full STE. Use STE where the text is a set of steps or definitions; do not force it onto argument.
