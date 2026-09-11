# Sonnet control-prompt content-filter investigation

Both D1 English `p2s-582-r1-en` and D3 `p2s-582-r1-ai` return empty content with `usage.finish_reason = content_filter` from the pinned Anthropic endpoint for Claude Sonnet 5. The matching pair is `p2s-582-r1`. Repeated recovery attempts preserve the same finish reason. All 18 other models returned nonempty text on each version.

The prompt concerns making a diplomatic argument for national reporting rather than external treaty inspections. This describes the scenario, not a confirmed explanation for the filter. The recorded API result does not identify the policy category or establish whether the filter ran at Anthropic or an intermediary. It does not indicate a timeout, token-limit truncation, or judge failure. The runner copies the API finish reason into usage and correctly marks empty content invalid; no evidence supports a text-parsing fix. The full raw API message was not retained, so alternate response fields cannot be inspected retrospectively.

Keep both rows and their original/recovery provenance. Under the existing transcript-based rubric they remain unscored, with API content-filter status reported separately. Do not relabel them as judged refusals, rewrite the prompts, or change provider pins to make them pass. For a paired D1/D3 Sonnet analysis, exclude the same missing pair on both sides (191 eligible pairs if all other rows validate); other models retain 192. A separate sensitivity analysis can treat the blocked outcome explicitly, with the changed outcome definition stated.

No new diagnostic API calls or bank, provider, runner, or scoring changes were needed for this finding. Recovery status in the accompanying JSON is a timestamped snapshot, not a final completeness certificate.

API schema reference: https://openrouter.ai/docs/api/reference/overview
