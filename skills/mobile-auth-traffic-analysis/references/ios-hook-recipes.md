# iOS Hook Recipes

Use these examples only on an authorized test device and application. Prefer observation-only instrumentation and do not equate jailbreak access with a normal attacker capability.

## Contents

1. Preparation
2. URL loading
3. WebKit navigation and bridges
4. Keychain operations
5. Native cryptography and parsing
6. Swift and symbol discovery
7. Failure diagnosis

## Preparation

Record the bundle identifier, app build, team/signing identity, device model, iOS version, jailbreak state, and Frida version. Attach to a running app when preserving login state; spawn when early initialization is required:

```bash
frida-ps -Uai | rg -i 'example|target'
frida -U -n ExampleTarget -l observe-ios.js
frida -U -f com.example.target -l observe-ios.js
```

Verify Objective-C availability before using class hooks:

```javascript
if (!ObjC.available) {
  throw new Error('Objective-C runtime is not available in this process');
}
```

## URL loading

Observe mutable request construction and redact authentication values:

```javascript
if (ObjC.available) {
  const klass = ObjC.classes.NSMutableURLRequest;
  const selector = '- setValue:forHTTPHeaderField:';
  const method = klass[selector];

  Interceptor.attach(method.implementation, {
    onEnter(args) {
      const value = new ObjC.Object(args[2]).toString();
      const field = new ObjC.Object(args[3]).toString();
      const lower = field.toLowerCase();
      const shown = lower.indexOf('token') >= 0 ||
        lower.indexOf('cookie') >= 0 ||
        lower.indexOf('authorization') >= 0
        ? '<redacted len=' + value.length + '>'
        : value;
      console.log('[header] ' + field + ': ' + shown);
    }
  });
}
```

Correlate runtime headers with the request builder, serializer, session delegate, and business model that generated them. If native URL loading is absent, inspect WebKit, a cross-platform framework, or a custom native transport.

## WebKit navigation and bridges

Observe top-level navigation:

```javascript
if (ObjC.available) {
  const WebView = ObjC.classes.WKWebView;
  const load = WebView['- loadRequest:'];
  Interceptor.attach(load.implementation, {
    onEnter(args) {
      const request = new ObjC.Object(args[2]);
      console.log('[WKWebView loadRequest] ' + request.URL().absoluteString());
    }
  });

  const evaluate = WebView['- evaluateJavaScript:completionHandler:'];
  Interceptor.attach(evaluate.implementation, {
    onEnter(args) {
      const script = new ObjC.Object(args[2]).toString();
      console.log('[WKWebView evaluateJavaScript] len=' + script.length);
    }
  });
}
```

Statically map `WKScriptMessageHandler`, registered message names, content worlds, navigation delegates, universal links, custom schemes, and any origin allowlist. A registered handler is only a primitive until attacker-controlled content can invoke a protected capability.

## Keychain operations

Observe operation timing and result codes without dumping secrets:

```javascript
const copyMatching = Module.findExportByName(null, 'SecItemCopyMatching');
if (copyMatching) {
  Interceptor.attach(copyMatching, {
    onEnter(args) {
      console.log('[Keychain] SecItemCopyMatching called');
    },
    onLeave(retval) {
      console.log('[Keychain] status=' + retval.toInt32());
    }
  });
}
```

Review access groups, accessibility classes, synchronizable items, backup behavior, and extension sharing. Jailbreak-readable keychain data does not by itself prove another sandboxed app can read it.

## Native cryptography and parsing

Observe lengths and algorithms before extracting any data. For CommonCrypto-style functions, hook the exported function used by the exact binary and log operation, algorithm, and buffer lengths. For parsing functions, capture format, caller module, and controlled fixture identity rather than raw private content.

Use `Interceptor.attach` on exported functions when possible. For private or stripped symbols, record the app binary UUID, module hash, architecture, load address, and module-relative offset. Recalculate offsets for every build.

## Swift and symbol discovery

Swift methods may not appear as Objective-C selectors. Use a combination of:

- `ObjC.enumerateLoadedClassesSync()` for bridged classes;
- `Process.enumerateModules()` for loaded frameworks;
- `Module.enumerateExports()` and `Module.enumerateSymbols()` where supported;
- static demangling and cross-references from the exact application binary;
- runtime backtraces from stable Objective-C or C boundary hooks.

Prefer a stable platform boundary hook first, then use its backtrace to locate application logic.

## Failure diagnosis

Check the correct process or extension, spawn timing, Objective-C availability, selector existence, Swift-only implementations, app architecture, symbol stripping, and framework load timing. Preserve failed assumptions as evidence so later work does not repeat the same hook path.
