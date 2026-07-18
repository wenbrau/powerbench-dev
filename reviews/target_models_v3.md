# Target models for the v3 pilot (#10)

Decision context: reuse the hackathon models where they still make sense, swap the outdated ones,
keep it cheap/fast for a pilot (Nico: "baratos, rápidos, en lo posible los de la hackatón"). Full
run panel is a later call.

## What was used before

- **Hackathon lit run (probe, 3 models):** `anthropic/claude-3-haiku`, `meta-llama/llama-4-maverick`,
  `mistralai/ministral-14b-2512`, plus `openai/gpt-5.4-nano` as judge.
- **Main 5-model experiment:** `minimax/minimax-m3`, `google/gemini-2.5-flash-lite`,
  `deepseek/deepseek-v4-pro`, `qwen/qwen3.7-plus`, `anthropic/claude-3-haiku`.

Reviewers flagged **`claude-3-haiku` as outdated** — the one clear swap.

## Two hard constraints

1. **Judge ≠ target family.** Judge is `openai/gpt-5.4-nano`, so **no target may be an OpenAI
   model** (self-grading). None of the candidates below are.
2. **Prompt-writer family = same-family bias.** Claude writes the prompts, so any Anthropic target
   answers prompts from its own family. Keep one current Anthropic model (we want it represented),
   but **state this as a limitation in the paper**.

## Recommended pilot panel (3 models, cheap/fast, family-diverse)

| Model | Family | Why |
|---|---|---|
| `anthropic/claude-haiku-4-5` | Anthropic (US) | replaces the outdated claude-3-haiku; current cheap Anthropic tier |
| `minimax/minimax-m3` | MiniMax (CH) | kept from the main experiment; cheap, already characterised, gave the clearest mode signal in the pilot |
| `moonshotai/kimi-k2` (or current Kimi) | Moonshot (CH) | the newer/cheaper option raised in the meeting; non-overlapping with judge and writer |

Rationale: 3 is enough for a pilot; spreads US/CH families; all cheap; two carry over from prior
runs for continuity, one is the requested new/cheap model. `gemini-2.5-flash-lite`,
`deepseek-v4-pro`, `qwen3.7-plus` stay as candidates for the **full** panel — no need to run five
for a pilot.

## Open for the full run (not now)

- Whether to expand back to 5+ and which exact families (the no-overlap-with-judge rule holds).
- Confirm the exact current model IDs resolve on OpenRouter at smoke time (Kimi and Haiku 4.5
  version strings especially).
- If we later want a target-model *panel* (not single), Kimi-family is the non-overlapping anchor.
