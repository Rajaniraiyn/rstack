# Games, graphics, simulation, media, and XR

Distinguish engine logic, rendered output, input/device integration, and the packaged player. Use the project's engine test runner and scene fixtures. [Unity Test Framework](https://docs.unity3d.com/Packages/com.unity.test-framework@latest/) supports engine-specific tests; [Godot command-line modes](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html) support relevant automation. Check the project's engine version and plugins before adopting a runner.

Test movement/state transitions, collision/physics outcomes, save/load, asset loading, scene changes, multiplayer ordering, and reconnect according to the product. Control seeds and fixed timesteps for repeatable simulation; renderer frame timing and physics time are different. Replay recorded input at defined ticks when diagnosing ordering or determinism rather than comparing wall-clock screenshots. Exercise controller/touch/keyboard input and focus changes on the required host. A headless scene pass doesn't establish graphics, sound, real devices, or exported-player behavior.

For canvas/WebGL/WebGPU/native GPU code, prefer a stable semantic test interface for logic and real input-to-effect checks for wiring. Inspect shader/compiler/validation errors and device-loss recovery where supported. Record GPU/driver/backend, resolution, color space, and precision. Compare visual baselines with justified tolerances; inspect differences rather than accepting broad pixel thresholds to hide failures. Use [os-automation.md](os-automation.md) for input in an isolated desktop when background targeting can't operate the control.

## Audio and video

Verify output bytes and actual decoded content, not filename or a successful export. Probe container/codecs, duration, dimensions, frame cadence, channels/sample rate, timestamps, and required tracks. Check start/end, transitions, sync, clipping/silence, and error cases with representative media. [ffprobe](https://ffmpeg.org/ffprobe.html) supplies structured metadata; it doesn't establish perceived sound or visual correctness.

For live capture/playback, test actual device/permission paths, buffering, latency/dropouts, seek/reconnect, and device changes as relevant. Synthetic media enables known expected content; hardware and browser/OS checks establish actual capture/playback. Offline rendering doesn't prove real-time performance.

For XR or specialized controllers, simulated pose/input covers deterministic logic. The headset/device path is needed for tracking, handedness, interaction, display behavior, and comfort-related performance claims. Don't send automation to the user's active headset. Report untested hardware explicitly and keep performance thresholds tied to the project's requirements.
