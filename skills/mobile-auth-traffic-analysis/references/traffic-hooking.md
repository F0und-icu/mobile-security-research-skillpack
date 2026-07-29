# Traffic And Hooking

Use a proxy when requests are readable and replayable. Move to instrumentation when payloads are encrypted, signatures are dynamic, cookies are generated in an embedded browser, a custom transport is used, or replay fails without explanation.

Observe the narrowest stable layer:

- request builders and interceptors for final headers and URLs;
- serializers for pre-encryption objects;
- cryptographic wrappers for inputs and outputs;
- WebView navigation, resource interception, and script evaluation for embedded flows;
- native networking only when higher layers provide no useful boundary.

Capture field names, lengths, hashes, and relationships by default. Avoid printing secret values. Record the code location and a before/after pair when reconstructing serialization or signing.

Instrumentation may explain protocol generation, but a hook-forged response or bypassed environment check is not final vulnerability evidence.
