# Android

Identify application ID, build variant, API levels, device ABI, and installed instrumentation target. Use the Gradle tasks already present. Select an explicit emulator/device serial for adb and the test runner; never assume the first attached device is the intended one.

| Boundary | Tool route |
| --- | --- |
| App logic | Existing JVM/local tests |
| Native Views inside the app | Espresso and instrumentation |
| Compose UI | Compose testing APIs and semantics |
| OS dialogs or cross-app flow | UI Automator, or a compatible Appium UIAutomator2 driver |
| Agent-driven mobile journey | Maestro when its current platform/device support fits |
| Embedded web content | Supported WebView debugging or Appium webview context, plus native bridge checks |

Sources: [Android testing](https://developer.android.com/training/testing), [UI Automator](https://developer.android.com/training/testing/other-components/ui-automator), [Compose tests](https://developer.android.com/develop/ui/compose/testing), [Appium contexts](https://appium.io/docs/en/latest/guides/context/), and [Maestro platform support](https://docs.maestro.dev/get-started/supported-platform).

Wait on semantics or an app state. Espresso idling resources and Compose synchronization cover their supported work, not every arbitrary background job or remote request. Register relevant idling resources or use bounded condition waits. [Espresso idling resources](https://developer.android.com/training/testing/espresso/idling-resource).

Exercise permission grant/deny/revoke, Back/navigation, keyboard/IME, rotation, background/resume, process recreation, offline recovery, and notification/deep-link entry when relevant. Distinguish activity recreation from real process death. Forced stop, low-memory process death, and a normal background transition have different lifecycle effects; choose the event the regression concerns. Test persistent state after relaunch. Capture logcat, instrumentation results, and crash/ANR evidence with the correct process/device filters. Keep each worker on its own device or emulator; concurrent UI runs on one device can invalidate each other's assertions.

Hybrid apps need context discovery after the webview becomes available, driver/webview compatibility, and explicit native/web context switching. Don't assume every view exposes a DOM or that debug builds match release inspectability.

Use dedicated test data and confirm clearing app state is appropriate before resetting a device/profile. Record animation settings and accessibility/font-scale changes rather than hiding a bug by disabling them. Emulator checks don't establish real camera, Bluetooth, biometrics, battery, OEM, or network-radio behavior. Run required hardware scenarios on a suitable device and mark missing ones not run.
