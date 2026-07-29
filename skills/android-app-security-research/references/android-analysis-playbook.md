# Android Analysis Playbook

Use this playbook after recording scope, package, version, signer, source, device, OS build, patch level, and test date.

## Contents

1. Acquire and identify
2. Manifest and component map
3. Code and resource search
4. IPC and caller identity
5. WebView and deep links
6. Files, updates, and dynamic content
7. Native boundaries
8. Runtime evidence

## Acquire and identify

Record package metadata and APK paths:

```bash
adb shell pm path com.example.target
adb shell dumpsys package com.example.target | rg \
  'versionName|versionCode|firstInstallTime|lastUpdateTime|installerPackageName|userId'
adb shell dumpsys package com.example.target > package-state.txt
```

Verify every split and signer with the platform build tools available in the environment. Preserve hashes before decompilation or mechanical formatting.

## Manifest and component map

Inventory exported state, permissions, intent filters, URI grants, authorities, task modes, backup settings, network configuration, and package visibility. Search decompiled output narrowly:

```bash
rg -n 'android:exported|android:permission|grantUriPermissions|authorities' .
rg -n 'Activity|Service|BroadcastReceiver|ContentProvider' sources
rg -n 'getCallingUid|getCallingPid|checkCalling|enforceCalling|clearCallingIdentity' sources
```

For each entry write:

```text
entry and invocation
required permission or grant
caller identity checks
controlled extras, URI, ClipData, or callback
downstream data and operations
ordinary-app reachability result
```

## Code and resource search

Search by capability and consumer rather than only vulnerability words:

```bash
rg -n 'openFile|openInputStream|openOutputStream|FileInputStream|FileOutputStream' sources
rg -n 'ZipInputStream|ZipFile|TarArchive|canonicalPath|normalize|resolve' sources
rg -n 'DexClassLoader|PathClassLoader|System\.load|System\.loadLibrary' sources
rg -n 'addJavascriptInterface|evaluateJavascript|loadUrl|shouldOverrideUrlLoading' sources
rg -n 'PendingIntent|getActivity\(|getService\(|getBroadcast\(' sources
rg -n 'SharedPreferences|SQLiteDatabase|RoomDatabase|WebViewDatabase' sources
```

When normal decompilation fails on one high-value class, recover that class from its containing DEX in fallback mode and verify ambiguous security branches against bytecode or runtime behavior:

```bash
jadx -m fallback --single-class 'com.example.target.FeatureClass' \
  --single-class-output /tmp/FeatureClass.java classes2.dex
```

Treat decompiler output as evidence for navigation, not as unquestionable source truth.

## IPC and caller identity

For Binder or bound services, find descriptors, generated stubs, transaction handlers, custom parcelables, callbacks, and identity fields:

```bash
rg -n 'IInterface|Binder|onTransact|INTERFACE_TRANSACTION|DESCRIPTOR|TRANSACTION_' sources
rg -n 'bindService|ServiceConnection|IBinder|Parcel\.obtain' sources
```

Compare every caller-supplied PID, UID, package, process, or token with platform-reported identity at the final check. Trace whether wrappers clear identity or forward calls through a privileged context. A reachable plugin or action name is not impact; follow its controlled fields to the consumer.

## WebView and deep links

Map route definitions, URI parsing, redirects, domain allowlists, bridge registration, file/content schemes, browser handoffs, and dynamic page sources:

```bash
rg -n 'Intent\.getData|getQueryParameter|Uri\.parse|URLUtil|WebViewClient' sources
rg -n 'JavascriptInterface|addJavascriptInterface|postWebMessage|WebMessage' sources
rg -n 'setAllowFileAccess|setAllowUniversalAccessFromFileURLs|setJavaScriptEnabled' sources
```

Build a matrix of content origin, navigation method, bridge availability, sensitive methods, and proven attacker control. Settings alone do not establish exploitability.

## Files, updates, and dynamic content

For every file flow record:

```text
input source -> decoding -> normalization -> resolved path -> write/replace semantics
             -> integrity check -> consuming process -> trigger -> final effect
```

Check both file and parent directory owner, mode, SELinux label, existence, and replacement behavior. Distinguish truncate, unlink, rename, atomic replace, and new-file creation. Prove the current consumer before investing in a write primitive.

## Native boundaries

Inventory native libraries by ABI and hash. Trace Java-to-native declarations, dynamic registration, parsers, image/media/document inputs, shared memory, dimensions, offsets, and lengths:

```bash
rg -n ' native |System\.load|System\.loadLibrary|RegisterNatives' sources
```

Use a benign input and confirm that the supported app build reaches the exact native consumer. A historical library version or unreachable parser is not a current finding.

## Runtime evidence

Keep observation and attack proof separate:

```bash
adb logcat -c
adb shell pidof com.example.target
adb shell dumpsys package com.example.target > before-package.txt
# run one controlled test
adb shell dumpsys package com.example.target > after-package.txt
```

Capture caller and target UIDs, process IDs, permissions, result data, timestamps, and cleanup. Root may prepare a target-owned marker or inspect hashes; it must not perform the action attributed to the attacker.
