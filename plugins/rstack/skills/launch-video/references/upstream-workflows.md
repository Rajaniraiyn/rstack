# Comparable video workflows

Consult this index when refreshing guidance or choosing an external workflow.

| Source and revision | Useful comparison | Integration boundary |
| --- | --- | --- |
| [onetake](https://github.com/feitangyuan/onetake/tree/cf09bde3e392c9aa32c4157f80cdbe1fa556685e), including its root skill and probe/render contracts | Continuity between beats, deterministic composition, motion inspection, localized UI demos | [PolyForm Noncommercial license](https://github.com/feitangyuan/onetake/blob/cf09bde3e392c9aa32c4157f80cdbe1fa556685e/LICENSE). Evaluate permitted use before using its tools/assets. |
| [Stickman Video Director](https://github.com/kaomei/stickman-video-director/tree/bdfcbdb8fa97a09bd4a9f1c20b857a48eb4f68fe), especially `skills/directing-stickman-videos/` | Character consistency, independently usable clip briefs, endpoint matching, recomposition | [MIT license](https://github.com/kaomei/stickman-video-director/blob/bdfcbdb8fa97a09bd4a9f1c20b857a48eb4f68fe/LICENSE). Preserve its notice if substantial material is reused. Verify provider names and generation specifications before use. |

[Shunit Haviv Hakimi's /brag workflow](https://github.com/latent-spaces/brag/tree/c893c5ed52aed84e3e2ee56787de869fccdae6b0) informed product-launch planning, engine handoff, and audio cues.

Use [motion-direction.md](motion-direction.md) for motion planning and review, [generated-sequences.md](generated-sequences.md) for character clips and localization, and [engines.md](engines.md) for rendering. Review creative quality and comprehension directly. Verify numerical thresholds and engagement claims before adopting them, and keep external approval and license requirements scoped to the tools or material used.

To inspect currently discoverable skills without installing them:

```sh
bunx --bun skills add feitangyuan/onetake --list
bunx --bun skills add kaomei/stickman-video-director --list
```

Repository listing can clone large media trees. If discovery stalls, inspect the GitHub tree and fetch only the skill, relevant references, and license. Record the revision and distinguish reading source from a real runtime integration check. Keep upstream contracts separate: onetake’s seek/probe metadata is not the bundled renderer’s `render(t)` API.
