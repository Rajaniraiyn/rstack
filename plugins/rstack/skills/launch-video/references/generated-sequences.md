# Character sequences and generated clips

Use this for stick-figure explainers, character-led product metaphors, or a requested video-generation prompt package. It is a production mode, not another rendering engine. Keep source facts and the requested output explicit: a storyboard, prompts, and a finished video are different deliverables.

## Establish a visual contract

Use the existing brief and defaults unless a material choice remains unresolved. Define the character silhouette/proportions, line weight, costume if relevant, palette, environment, camera grammar, ratio, and narration language. Design an original character or use authorized reference assets. Do not silently reuse an upstream mascot. Visual metaphors explain a claim; they do not replace real UI when the viewer needs evidence of product behavior.

Map each narrated idea to a concrete action and result rather than decorating every sentence. Staging, camera path, and caption-safe space must be recomposed for another aspect ratio. Keep effects sparse enough that the idea remains legible; no universal rule requires constant movement or several effects per shot.

## Package independent clips

Before writing provider-specific prompts, verify the selected service’s actual model ID, duration/fps/resolution support, audio, reference-image/video features, and rights/watermark terms. Upstream provider labels are not an API contract. A prompt cannot enable an unsupported capability. Keep the requested total duration; if provider clip limits require segmentation, choose compatible segments and trims rather than silently rounding the brief.

Each independently generated clip needs enough context to stand alone:

| Field | Include |
| --- | --- |
| Identity | Character and style references, proportions, consistent appearance |
| Composition | Actual supported dimensions/ratio and intended staging |
| Opening | Pose, object placement, movement direction, inherited state |
| Action | Timed, intelligible events with the focus and camera behavior |
| Closing | Exact visible state that the next clip should inherit |
| Sound/text | Requested dialogue and pronunciation, audio ownership, intended overlays |
| Constraints | Relevant deformation, drift, unwanted text, or style errors |

Use available reference/continuation controls rather than assuming that “same character” or an identical seed guarantees consistency. Repeated descriptions help communicate intent but cannot lock generated anatomy, voice, music, or continuity. Inspect actual outputs, including first/last frames, intermediate poses, and every seam. Regenerate the defective segment without discarding accepted user edits.

For exact product names, UI copy, logos, diagrams, or captions, prefer deterministic overlays or actual rendered UI. Keep technical palette tokens in the source/style specification; use descriptive colors in a prompt if literal token rendering is a risk. Do not suppress required attribution or provider watermarks with negative prompts. Choose constraints for the actual style rather than banning all text, gradients, or morphs globally.

## Assemble and localize

When narration is requested, use one authorized voice and a continuous music bed across clips where possible. Generated audio needs listening and transcription review; separate narration, SFX, and music ownership to avoid double mixes. Normalize timelines, inspect trims and crossfades, and use [deliver.md](deliver.md) for final checks.

For multilingual versions, share the composition and content structure where practical; translate meaning and pronunciation, then remeasure glyphs, line breaks, reading time, captions, and safe areas. Align scene events to equivalent spoken ideas; keep time mappings monotone and avoid stretching speech unnaturally. Languages may need different durations or shots. Preserve the accepted source-language cut and compare it after shared changes.

For a prompt-only request, deliver the ordered prompt package, references, intended clip connections, and assembly notes; label it unrendered. For a finished-video request, use the selected available tools through assembly and verification. Existing spending authorization governs generation; ask only when required authorization or a consequential specification is missing.

[Stickman Video Director](https://github.com/kaomei/stickman-video-director) informed the comparison of character-directed planning and clip handoff. This reference uses original instructions and does not copy its prompt templates, character, fixed timing, or approval gates. See [upstream-workflows.md](upstream-workflows.md).
