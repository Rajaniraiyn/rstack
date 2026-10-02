# Flutter across platforms

Inspect `pubspec.yaml`, Flutter version, flavors, plugins, supported targets, and existing tests. Use unit tests for logic, widget tests for Flutter tree behavior, and `integration_test` for the running app. Select a specific device from `flutter devices` rather than an incidental default.

For a configured desktop target, the official integration guide uses `flutter test integration_test/app_test.dart -d <device-id>`. Reuse the project's test path and supported device ID. Web and device-farm execution may use different runners; read the current guide for that target. [Flutter integration testing](https://docs.flutter.dev/testing/integration-tests).

Use stable keys/semantics and assertions on state. Control fake time in widget tests. `pumpAndSettle` waits until no frames are scheduled and eventually times out on an infinite animation. Prefer the required pumps or a bounded wait for the asserted condition. [API behavior](https://api.flutter.dev/flutter/flutter_test/WidgetTester/pumpAndSettle.html). Don't normalize away layout overflow, text scaling, missing semantics, or input failures to obtain a golden pass.

`integration_test` cannot by itself interact with all native platform UI, including permission dialogs and some embedded platform views. Use a compatible native driver or [Patrol](https://patrol.leancode.co/documentation) where its current supported platforms fit. Check desktop support explicitly; mobile support does not imply desktop support. [Flutter integration-test limitations](https://docs.flutter.dev/testing/integration-tests#introduction).

Test plugins and platform channels on the real target, including serialization, errors, disposal, and native side effects. A mocked channel confirms only Dart behavior. Flutter web tests don't establish Windows/macOS/Linux plugin correctness. Read [desktop.md](desktop.md), [android.md](android.md), or [apple.md](apple.md) for host checks.

Desktop builds require the target platform's supported toolchain and display/session. Exercise resize, minimum window size, DPI/text scaling, keyboard focus, shortcuts, file dialogs, clipboard, menus, and multiple windows if present. Check the packaged build for assets, native libraries, writable paths, and persistence. Goldens need a controlled font/platform environment, and actual visual failures still need inspection.
