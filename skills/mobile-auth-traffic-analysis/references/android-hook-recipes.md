# Android Hook Recipes

Use these recipes only on an authorized test device and target. Start with observation-only hooks. Do not treat a hook-forged response, bypassed environment check, or modified return value as final vulnerability evidence.

## Contents

1. Preparation
2. WebView and JavaScript bridges
3. Native HTTP stacks
4. Cryptography and request signing
5. Cookies and local session state
6. Native functions
7. Failure diagnosis

## Preparation

Confirm the package, process, ABI, and Frida versions before debugging application behavior:

```bash
adb devices
adb shell pm path com.example.target
adb shell dumpsys package com.example.target | rg 'versionName|versionCode|userId|firstInstallTime|lastUpdateTime'
frida-ps -Uai | rg -i 'example|target'
frida --version
```

Spawn when early initialization matters; attach when login state or app startup must remain untouched:

```bash
frida -U -f com.example.target -l observe.js
frida -U -n ExampleTarget -l observe.js
```

Clear logs and keep one evidence window:

```bash
adb logcat -c
adb logcat --pid "$(adb shell pidof -s com.example.target)" -v threadtime
```

## WebView and JavaScript bridges

Observe navigation and script evaluation without changing results:

```javascript
Java.perform(function () {
  const WebView = Java.use('android.webkit.WebView');

  const loadUrl = WebView.loadUrl.overload('java.lang.String');
  loadUrl.implementation = function (url) {
    console.log('[WebView.loadUrl] ' + url);
    return loadUrl.call(this, url);
  };

  const evaluate = WebView.evaluateJavascript.overload(
    'java.lang.String',
    'android.webkit.ValueCallback'
  );
  evaluate.implementation = function (script, callback) {
    console.log('[WebView.evaluateJavascript] len=' + script.length);
    return evaluate.call(this, script, callback);
  };

  const addBridge = WebView.addJavascriptInterface.overload(
    'java.lang.Object',
    'java.lang.String'
  );
  addBridge.implementation = function (object, name) {
    console.log('[WebView.addJavascriptInterface] name=' + name +
      ' class=' + object.getClass().getName());
    return addBridge.call(this, object, name);
  };
});
```

Pair runtime observations with static review of `WebViewClient`, `WebChromeClient`, navigation callbacks, URL parsing, bridge annotations, content sources, and every origin decision. A bridge name alone does not prove an attacker-controlled origin can invoke it.

## Native HTTP stacks

Start at request construction. This often reveals dynamic headers without reading response secrets:

```javascript
Java.perform(function () {
  const Builder = Java.use('okhttp3.Request$Builder');
  const build = Builder.build.overload();

  build.implementation = function () {
    const request = build.call(this);
    console.log('[HTTP] ' + request.method() + ' ' + request.url().toString());

    const names = request.headers().names().toArray();
    for (let i = 0; i < names.length; i++) {
      const name = String(names[i]);
      const lower = name.toLowerCase();
      if (lower.indexOf('token') >= 0 || lower.indexOf('cookie') >= 0 ||
          lower.indexOf('authorization') >= 0) {
        const value = request.header(name);
        console.log('  ' + name + ': <redacted len=' + (value ? value.length : 0) + '>');
      } else {
        console.log('  ' + name + ': ' + request.header(name));
      }
    }
    return request;
  };
});
```

If this class is absent, identify the actual stack from loaded classes and libraries. Check WebView/Chromium, URL connections, Retrofit wrappers, native libraries, or a vendor-independent custom transport. Do not conclude that no request exists merely because one hook point does not fire.

For bodies, prefer hooking the application serializer or business request object. Writing an arbitrary one-shot body into a buffer can consume or alter it; use that only after verifying the body type is repeatable.

## Cryptography and request signing

Use platform crypto hooks to identify algorithms, key sizes, input lengths, and call timing. Do not print raw keys or full plaintext by default:

```javascript
Java.perform(function () {
  const Cipher = Java.use('javax.crypto.Cipher');
  const init = Cipher.init.overload('int', 'java.security.Key');
  init.implementation = function (mode, key) {
    const encoded = key.getEncoded();
    console.log('[Cipher.init] algorithm=' + this.getAlgorithm() +
      ' mode=' + mode + ' keyBytes=' + (encoded ? encoded.length : 0));
    return init.call(this, mode, key);
  };

  const doFinal = Cipher.doFinal.overload('[B');
  doFinal.implementation = function (input) {
    const output = doFinal.call(this, input);
    console.log('[Cipher.doFinal] algorithm=' + this.getAlgorithm() +
      ' inputBytes=' + input.length + ' outputBytes=' + output.length);
    return output;
  };

  const Mac = Java.use('javax.crypto.Mac');
  const macFinal = Mac.doFinal.overload('[B');
  macFinal.implementation = function (input) {
    const output = macFinal.call(this, input);
    console.log('[Mac.doFinal] algorithm=' + this.getAlgorithm() +
      ' inputBytes=' + input.length + ' outputBytes=' + output.length);
    return output;
  };
});
```

Prefer the application's higher-level `sign`, `encrypt`, `envelope`, or serializer wrapper after the platform hook identifies its call stack. Reconstruct four things together: participating fields, canonical serialization, timestamp/nonce rules, and key decoding. A client key is reportable only after proving a real server-side capability.

## Cookies and local session state

Observe cookie access while redacting values:

```javascript
Java.perform(function () {
  const CookieManager = Java.use('android.webkit.CookieManager');
  const getCookie = CookieManager.getCookie.overload('java.lang.String');
  getCookie.implementation = function (url) {
    const value = getCookie.call(this, url);
    console.log('[CookieManager.getCookie] url=' + url +
      ' value=<redacted len=' + (value ? value.length : 0) + '>');
    return value;
  };
});
```

Static session locations commonly include preferences, database-backed stores, WebView cookies, browser local storage, and framework-specific key/value stores. Use root only for your own test-account diagnostics; the final issue must have an independent attacker path.

## Native functions

Use exported symbols or a known offset from the exact tested binary. Log arguments conservatively and call the original function unchanged:

```javascript
const moduleName = 'libexample.so';
const symbol = Module.findExportByName(moduleName, 'example_function');

if (symbol) {
  Interceptor.attach(symbol, {
    onEnter(args) {
      console.log('[native] example_function called');
      this.first = args[0];
    },
    onLeave(retval) {
      console.log('[native] return=' + retval);
    }
  });
}
```

For stripped libraries, record the binary hash, load base, architecture, module-relative offset, and static-analysis symbol context. Never reuse an offset across versions without revalidating it.

## Failure diagnosis

When a hook does not fire, check in order:

1. correct package and process, including secondary processes;
2. spawn versus attach timing;
3. class loader and delayed module loading;
4. overload signature and obfuscation;
5. WebView or native network stack instead of the assumed Java stack;
6. architecture mismatch or wrong native module version;
7. anti-instrumentation behavior, documented as a test limitation rather than silently bypassed.

Keep a raw diagnostic log and a redacted evidence log. Label any modified return value or bypass as diagnostic.
