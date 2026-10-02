# Device and network protocols

Separate message semantics, framing/transport, peer compatibility, and physical link behavior. Identify protocol/version, endpoint identity, negotiated options, payload units/endianness, and the intended real or simulated peer. An echo server can verify transport while accepting behavior the real device rejects.

Test parsing and state transitions with deterministic fixtures. Include truncated, concatenated, oversized, malformed, duplicate, reordered, and delayed messages as the transport allows. Stream reads need framing logic; a single read need not return one complete message. Check backpressure, timeout, cancellation, retransmission, reconnect, and session resumption against the specification. Inject faults at the relevant layer: application-level retries do not reproduce packet fragmentation, radio loss, or driver hotplug. Retain minimized wire examples for failures.

## Transport-specific decisions

| Transport | Things generic API tests miss |
| --- | --- |
| UART/serial | Baud/parity/flow control, partial reads, line endings, reset when opening the port, reconnect identity |
| USB | Enumeration/descriptors, interface claiming, hotplug, driver/OS permissions, disconnect during transfer |
| BLE | Advertising/discovery, pairing/bonding, permissions, MTU fragmentation, notifications, reconnect |
| CAN/industrial bus | IDs, frame size, arbitration/load, bus errors, timeouts, matching physical configuration |
| MQTT/IoT messaging | Session state, retained messages, QoS/redelivery, duplicate processing, offline/reconnect behavior |
| TCP/UDP/custom RPC | Framing, half-close, packet loss/reordering where applicable, negotiation, resource limits |

[pySerial](https://pyserial.readthedocs.io/en/latest/shortintro.html) provides serial access with configurable deadlines; [Wireshark](https://www.wireshark.org/docs/wsug_html_chunked/ChapterIntroduction.html) can provide supported packet/dissector evidence. Use the stack's existing driver or protocol fixture first. Check actual platform capabilities and privileges; packet capture may expose unrelated traffic or credentials.

Use a loopback, virtual bus, emulator, or isolated test broker for logic and controlled faults. Add the actual peer/device when the claim depends on OS drivers, negotiation, timing, radio, or electrical behavior. A virtual CAN pass doesn't establish bus termination or arbitration under physical load. Browser Bluetooth/USB restrictions need the actual browser/OS path as well as device checks.

Keep unique client/session/topic IDs and reserve exclusive device links. Confirm the destination before sending commands, and avoid discovery broadcasts or device-control traffic outside the intended fixture. Report wire-level observations separately from the command's durable effect. See [embedded.md](embedded.md) for board evidence and [api-backend.md](api-backend.md) for service contracts.
