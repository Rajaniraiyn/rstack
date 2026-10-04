# Comparable video workflows

Checked 2026-10-04 against repository skills, references, and licenses, not only demo claims. Consult this index when refreshing guidance or choosing an external workflow. No upstream implementation was installed, executed, or vendored by this update.

| Source and inspected revision | Useful comparison | Integration boundary |
| --- | --- | --- |
| [onetake](https://github.com/feitangyuan/onetake/tree/cf09bde3e392c9aa32c4157f80cdbe1fa556685e), including its root skill and probe/render contracts | Continuity between beats, deterministic composition, motion inspection, localized UI demos | [PolyForm Noncommercial license](https://github.com/feitangyuan/onetake/blob/cf09bde3e392c9aa32c4157f80cdbe1fa556685e/LICENSE); keep external and evaluate permitted use before using its tools/assets. R Stack remains MIT and contains no copied onetake implementation. |
| [Stickman Video Director](https://github.com/kaomei/stickman-video-director/tree/bdfcbdb8fa97a09bd4a9f1c20b857a48eb4f68fe), especially `skills/directing-stickman-videos/` | Character consistency, independently usable clip briefs, endpoint matching, recomposition | [MIT license](https://github.com/kaomei/stickman-video-director/blob/bdfcbdb8fa97a09bd4a9f1c20b857a48eb4f68fe/LICENSE). No templates/assets copied; preserve its notice if substantial material is later reused. Its provider names and generation specifications require independent verification. |

Use [motion-direction.md](motion-direction.md) for motion planning and review, and [generated-sequences.md](generated-sequences.md) for character clips, generation handoffs, and localization. Keep engine mechanics in [engines.md](engines.md). Automated heuristics help locate defects; they cannot certify creativity, comprehension, or completion rates. Do not inherit arbitrary numerical thresholds, claimed engagement improvements, mandatory approvals, or licensing restrictions as hidden defaults for the whole skill.

To inspect currently discoverable skills without installing them:

```sh
bunx --bun skills add feitangyuan/onetake --list
bunx --bun skills add kaomei/stickman-video-director --list
```

Repository listing can clone large media trees. If discovery stalls, inspect the GitHub tree and fetch only the skill, relevant references, and license. Record the revision and distinguish reading source from a real runtime integration check. Keep upstream contracts separate: onetake’s seek/probe metadata is not the bundled renderer’s `render(t)` API.
