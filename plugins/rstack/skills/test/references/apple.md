# iOS, iPadOS, watchOS, and macOS

Use Swift Testing or XCTest for the repository's logic tests and XCTest/XCUITest for UI automation. Don't replace an existing runner merely to modernize its name. Apple UI testing requires the relevant Xcode/macOS toolchain and runtime. Discover schemes and available destinations before choosing a simulator/device. Keep simulator identifiers, test accounts, and app data explicit. Parallel UI workers need separate simulator/device assignments and isolated backend fixtures; simulator cloning alone does not isolate shared services. Capture `.xcresult` and the underlying failure log; a build success is not a test pass. [Apple UI tests](https://developer.apple.com/documentation/xctest/user-interface-tests).

Test through accessibility identifiers and observable state. Avoid brittle element indexes. Cover navigation, keyboard/focus, permission dialogs, deep links, background/resume, relaunch persistence, denied/offline states, and cancellation as relevant. Distinguish app termination from view recreation. iPad multitasking, orientation, pointer input, and external keyboard deserve their own checks when supported.

Simulator execution does not prove signing, entitlement behavior, hardware sensors, push delivery, Bluetooth, HealthKit, background scheduling, or real-device performance. Identify which assertions need a physical device. Native Safari and WKWebView behavior also differ from desktop Chromium. Test the native/web bridge and host policy rather than replacing the host with a permissive browser stub.

Appium's XCUITest driver or Maestro can supplement the native runner where their current support fits. Verify driver/platform requirements first; do not infer watchOS or native macOS support from an iOS tool's name. [Appium XCUITest](https://appium.github.io/appium-xcuitest-driver/), [Maestro platform support](https://docs.maestro.dev/get-started/supported-platform).

## watchOS

Create/use the watch app's own unit/UI test targets and scheme. Select the watch destination and paired phone when the architecture requires one. A passing iPhone companion test does not exercise watch UI. Apple documents watchOS unit and UI testing bundles. [Set up watchOS tests](https://developer.apple.com/documentation/watchos-apps/setting-up-tests-for-your-watchos-app).

Choose checks according to the app's contract: small-screen layout, accessible names, crown/scroll interaction, launch and resume, complication/widget timeline state, notification actions, and watch/phone connectivity. Exercise delayed, duplicate, out-of-order, and offline messages in deterministic logic tests, then verify supported paired-device flows. Check independent-watch behavior if declared. Do not claim real background scheduling, haptics, workouts, or sensor accuracy from simulated UI. Report controls the selected driver cannot operate.

## Native macOS

Test AppKit/SwiftUI menus, keyboard shortcuts, focus/window lifecycle, file dialogs, drag/drop, sandbox/bookmarks, and persistence. Desktop accessibility and capture permissions can require host setup. Use app-specific accessibility automation or a narrow test helper where XCUITest cannot reach the required interaction. Keep UI automation bound to the intended app/window and account for multiple windows.

For a shared host desktop, use [os-automation.md](os-automation.md) to choose supported background actions or a separate test desktop. CUA's desktop driver does not replace iOS/watchOS device runners.
