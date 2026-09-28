# Sound

Write the music and effects as one piece: effects in the same key and the same space as the music, blended in rather than laid on top. Effects sit softly under the music, nothing harsh or spiky, and repeated small sounds stay in the background.

## Song spec

`scripts/synth.py` builds the track from a JSON spec; every field is shown in [../assets/examples/song.json](../assets/examples/song.json).

```sh
python scripts/synth.py work/song.json --out work/audio
```

It writes `stem-music.wav` (drums, bass, chords, arp, reverb, sidechained to the kick), `stem-fx.wav` (effects), and `soundtrack.wav` (a quick premix). Keep the stems: the voiceover mix ducks the music but not the effects.

| Field | Use |
|---|---|
| `bpm` | 120 gives a beat every 0.5 s; match the storyboard grid |
| `chords` | MIDI triads, one per bar from the drop (A minor: `[[57,60,64],[53,57,60],[48,52,55],[55,59,62]]`) |
| `drop` | when the groove starts; put it where the product appears |
| `intro.ticks` / `hits` / `riser` | clock ticks before the drop, sub hits on the hook's words, a riser into the drop |
| `outro`, `outro_chord`, `outro_motif` | the groove stops, a chord blooms, a short rising motif lands with the logo |
| `sfx` | effects on the timeline, pitched from the first chord's root |

Effect types: `typing` (len, rate), `send`, `pop` (note), `click` (note), `whoosh` (len), `chime` (success), `chord` (a card or preview landing), `hit` (a word slam), `buzz` (phone vibration and notification ding), `rewind` (tape rewind).

Match each effect to what is on screen at that frame: typing under typing, a send when a message leaves, a pop when one arrives, a chime when tests pass, whooshes under scene changes, a buzz only when a phone would really buzz.

## Mood and key

- Energetic launch: 120 bpm, minor key (A minor Am–F–C–G), the drop when the product appears.
- Calm or polished: 90–100 bpm, major key, no kick until the reveal, longer chords (`bars_per_chord: 2`).
- Late-night or deadpan: sparse ticks, sub hits, no groove until late.

Keep the mix under control by construction: effects mostly −25 to −35 LUFS, music around −19 LUFS before mastering, the premix around −14 to −15 LUFS.

## Measure, since you cannot listen

Check the integrated loudness and look at the momentary curve for spikes or holes:

```sh
ffmpeg -hide_banner -i work/audio/soundtrack.wav -af ebur128=peak=true -f null - 2>&1 | tail -12
```

A riser should build (momentary loudness climbing toward the drop), the drop should be the loudest moment, the groove steady within about ±2 LU, and the outro should decay. A dip right before the drop means the riser is too quiet; raise its gain in `synth.py` or add a `hit`.
