# Firmware, embedded Linux, and digital hardware

Identify board/SoC and revision, toolchain, firmware hash, bootloader/partition layout, configuration, connected probe/serial identity, and test fixture. A serial path can change after reset; bind to device identity where possible. Flashing a test image can replace working firmware and data, so use the authorized test device and understand the runner's upload behavior before invoking it.

## Choose the execution level

| Boundary | Starting route and evidence limit |
| --- | --- |
| Portable firmware logic | Host-native tests with controlled peripheral interfaces |
| RTOS behavior or board configuration | Existing RTOS runner; Zephyr's Twister can select supported execution targets |
| ESP-IDF components | Its Unity-based target tests and pytest-embedded automation where appropriate |
| PlatformIO project | Existing `pio test` environments, explicitly selecting host or device |
| Supported CPU/peripherals in simulation | QEMU/Renode or the project's simulator with declared machine models |
| Electrical/timing/peripheral behavior | Board/bench or hardware-in-the-loop tests with independent measurements |
| FPGA/HDL | Existing simulator and cocotb/testbench; formal properties when supported |
| Embedded Linux/driver | Userspace integration, kernel tests where relevant, then the intended board/runtime |

Sources: [Zephyr Twister](https://docs.zephyrproject.org/latest/develop/twister/index.html), [ESP-IDF testing](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/unit-tests.html), [PlatformIO testing](https://docs.platformio.org/en/latest/advanced/unit-testing/index.html), [Renode testing](https://renode.readthedocs.io/en/latest/introduction/testing.html), [cocotb](https://docs.cocotb.org/en/stable/), and [SymbiYosys](https://symbiyosys.readthedocs.io/en/latest/).

## Choose checks by the device contract

- Boot and initialization, reset reasons, watchdog recovery, startup errors, and expected safe output state. Check the actual image ran, not only that compilation or flashing succeeded. Drain stale serial output and bind each result to the boot/image and test invocation so a previous run cannot supply a false pass.
- Interrupt/task ordering, queue exhaustion, cancellation, priority inversion where relevant, stack/heap limits, and long-run resource growth. Inject time deterministically for logic tests; measure real deadlines/jitter on the relevant runtime.
- Timer wraparound, signed/unsigned ranges, endianness, alignment, and compiler optimization differences. Host word size or a debug build can conceal target defects.
- Disconnected/stuck peripherals, bus timeouts, corrupted frames, sensor limits/calibration, and reconnection. Assert externally observable output; a mocked register write isn't a physical measurement.
- Persistent configuration, interrupted writes, OTA/boot rollback, invalid or incompatible images, low-power wakeup, and recovery after reset. Use a controlled bench for power cuts; preserve a known recovery path. Don't burn eFuses or change permanent security state as a routine test.

UART/RTT/SWO logs need framed results, boot identification, finite read deadlines, and reset-aware reconnect. Reserve each physical device/probe/fixture for one test sequence. Multiple boards don't imply independent power supplies, serial bridges, radio channels, or instruments. See [protocols.md](protocols.md) and [concurrency.md](concurrency.md).

Emulator models may omit peripherals, timing, interrupts, analog effects, RF, and power behavior. State what the model covers. Simulation success doesn't establish board pin mapping, voltage levels, throughput, battery life, or physical output.

For HDL, check reset sequencing, handshake/backpressure, corner values, unknown values, clock-domain assumptions, and scoreboard independence. Save seed/waveform for failures. Report formal bounds, assumptions, and whether a property was proven or only covered; simulation isn't timing closure. A synthesized design still needs the relevant implementation/board checks.
