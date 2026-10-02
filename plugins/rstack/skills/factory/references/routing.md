# Model routing

Verified against official provider documentation on 3 October 2026. Replace this shortlist when the recommended lineup changes; keep one current table rather than appending generations. Confirm the installed harness and account expose a model before dispatching it. API availability does not establish subscription or CLI availability.

## Current shortlist

| Provider | Model | API ID | Starting role |
| --- | --- | --- | --- |
| OpenAI | GPT-6.1 Sol | `gpt-6.1-sol` | Balanced implementation and ordinary coding |
| OpenAI | GPT-6 Astra | `gpt-6-astra` | Demanding reasoning, coding, and long-running work |
| OpenAI | GPT-6 Luna | `gpt-6-luna` | Focused, high-volume, cost-sensitive tasks |
| Anthropic | Claude Opus 5.5 | `claude-opus-5-5` | General starting point and long-running coding |
| Anthropic | Claude Sonnet 5.5 | `claude-sonnet-5-5` | Faster implementation route |
| Anthropic | Claude Fable 5.1 | `claude-fable-5-1` | Demanding reasoning and long-horizon work |
| Anthropic | Claude Haiku 4.5 | `claude-haiku-4-5-20251001` | Fast, inexpensive focused tasks |
| Google | Gemini 3.8 Flash | `gemini-3.8-flash` | Current stable general route through a configured provider |
| Google | Gemini 3.5 Flash-Lite | `gemini-3.5-flash-lite` | Current stable cost-sensitive route through a configured provider |

Roles follow the [OpenAI catalog](https://developers.openai.com/api/docs/models), [Claude lineup](https://platform.claude.com/docs/en/models/overview), and [Gemini catalog](https://ai.google.dev/gemini-api/docs/models). They are starting choices, not a measured ranking on this repository. Haiku 4.5 remains the listed Haiku generation; its smaller version number does not make it a retired model. Restricted-access and preview models are excluded from the default shortlist.

## Defaults and escalation

Preserve the user's explicit model or saved route. Without an existing choice, start ordinary implementation with GPT-6.1 Sol on an available OpenAI route or Opus 5.5 on an available Claude route. Use Luna, Haiku, Sonnet, or Flash-Lite for a representative focused task before dispatching a large inexpensive batch. Use Gemini 3.8 Flash when that configured provider fits the task.

For demanding work, choose Astra or Fable when available. Escalate an ordinary route after a demonstrated capability failure, or choose the stronger route up front when the problem warrants it. A new release alone does not justify overriding the user's choice, switching providers, or claiming lower cost.

Review with an independent available route within budget. Collect elapsed time, retries, accepted outputs, and actual billed cost when available. Subscription runs still have quotas. Update defaults from those results rather than leaderboards.

## Reasoning settings

Use the user's setting or the model and harness default. Translate intent through current installed help; provider effort names are not equivalent.

- [GPT-6.1 Sol](https://developers.openai.com/api/docs/models/gpt-6.1-sol) supports API effort `low`, `medium`, `high`, `xhigh`, and `max`, with `medium` as default. It does not support `none` or `minimal`.
- [GPT-6 Astra](https://developers.openai.com/api/docs/models/gpt-6-astra) supports API effort `low`, `medium`, `high`, `xhigh`, and `max`.
- [GPT-6 Luna](https://developers.openai.com/api/docs/models/gpt-6-luna) also supports `none`; its API default is `medium`.
- Claude's current model table lists default effort `medium` for Opus 5.5 and `high` for Sonnet 5.5 and Fable 5.1. Haiku 4.5 has no effort parameter. Opus and Fable use always-on adaptive thinking. Check [Claude Code model configuration](https://code.claude.com/docs/en/model-config) for CLI aliases and supported controls.

API settings are not CLI arguments. OpenCode provider prefixes and variants depend on its configured provider; Amp and Copilot can expose different selections. Resolve them through [harnesses.md](harnesses.md) rather than manufacturing a command from an API ID.

## Budgets and refresh

Put the retry and spend limits in the worker brief. Enforce a native cost cap only when supported; a timeout limits wall time, not dollars. Inspect logs and artifacts before retrying. Fix setup failures, narrow a vague brief, or escalate a demonstrated reasoning failure. Stop at the configured limit and retain partial work.

During factory setup or a requested model refresh, fetch the official catalogs, check actual harness support, replace superseded rows and examples, and update the verification date. Keep current supported family members; remove retired and obsolete default choices. Record any approved change to saved routes. Preserve credentials and unrelated configuration. Fetch current pricing when a budget decision requires it rather than maintaining another price table here.
