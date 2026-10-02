# Robotics and control systems

Separate algorithm correctness, node/process integration, simulated motion, and physical behavior. Identify middleware distribution, robot model, coordinate frames/units, clock source, controller configuration, sensor calibration, and active device interfaces. A simulator's time and world are part of the fixture.

Use the repository's node and launch tests, recorded sensor fixtures, or simulation stack. ROS 2's [launch_testing](https://github.com/ros2/launch/tree/rolling/launch_testing) supports process integration checks; consult the version matching the project's distribution. Keep a unique middleware domain or namespace where supported, and verify that tests don't discover or command a nearby real robot. A namespace alone does not prevent domain discovery, external bridges, or drivers bound to shared physical interfaces.

Prioritize relevant contracts:

- Coordinate transforms, units, timestamps, stale sensor readings, missing measurements, outliers, and uncertainty. Plausible-looking motion can hide a sign, scale, or frame error.
- Control-loop deadlines, saturation, anti-windup, command limits, timeout behavior, watchdogs, and return to the intended safe state. Measure overshoot/settling against project-defined criteria rather than inventing acceptable limits.
- Startup, lifecycle transitions, node restart, delayed/duplicate messages, QoS mismatch, and lost connectivity. Readiness should mean the required publishers/controllers are ready, not only that processes exist.
- Deterministic replay with fixed recorded inputs, then simulated noise/latency and representative world conditions. Keep training/tuning cases separate from evaluation cases.
- Fleet coordination, cancellation, obstacle handling, and recovery only when implemented. A planner output is weaker evidence than the full command-to-observed-effect loop.

Physical runs need an authorized bench/site with the intended actuator limits, interlocks, and stop mechanism. Begin with disconnected or constrained actuators when that preserves the test's meaning. Never infer permission to move hardware from a request to test its software. Prefer software-in-the-loop and bench sensor tests while a physical test is unavailable.

Record configuration, trajectory/input trace, observed outputs, timing, failure trigger, and seed/world version. Separate simulator fidelity from app defects. Simulation doesn't establish real friction, payload, RF, sensor calibration, human detection, or mechanical response. Report missing physical checks explicitly.
