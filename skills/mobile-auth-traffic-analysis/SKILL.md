---
name: mobile-auth-traffic-analysis
description: Authorized mobile, mini-app, H5, WebView, and API traffic analysis for authentication flows, dynamic headers, request signing, object authorization, role checks, environment isolation, uploads, and reproducible evidence. Use when proxy traffic alone is insufficient or when testing a mobile backend with self-owned accounts and objects.
---

# Mobile Auth Traffic Analysis

Model the normal application protocol before changing authentication or object fields. Keep raw secrets out of reports, terminal output, and reusable skills.

## Establish the baseline

1. Confirm scope and use an authorized test account.
2. Capture login, token refresh, profile, and one harmless business request.
3. Identify the network stack, host, path, method, serialization, authentication fields, signature fields, timestamps, nonces, device fields, and object identifiers.
4. Record which values prove identity and which merely select an object.

Read [references/traffic-hooking.md](references/traffic-hooking.md) when requests are encrypted, signed, generated in a WebView, or not replayable. Read [references/authentication-authorization.md](references/authentication-authorization.md) before changing identity, role, or object fields.

## Choose the observation layer

- Use an intercepting proxy for plaintext requests, responses, replay, and evidence capture.
- Use Java or native instrumentation for pre-encryption payloads, signing inputs, dynamic headers, cookies, and custom transports.
- Inspect WebView and browser layers when native HTTP hooks do not observe login or embedded business flows.
- Treat hook-modified success as diagnostic only. Final proof must come from the real app or backend behavior.

## Test with controls

For each hypothesis compare only the minimum necessary variants:

1. valid session with a self-owned object;
2. missing, expired, or intentionally invalid authentication;
3. valid session with another self-owned object or legitimately available second test role;
4. a malformed or nonexistent identifier when it helps distinguish validation from authorization.

Do not enumerate adjacent identifiers or retrieve third-party records. For mutating endpoints, prepare a reversible self-owned object and capture its state before, after, and after cleanup.

## High-value questions

- Can an unauthenticated client obtain or refresh a usable session?
- Is user identity selected by a client field instead of the authenticated session?
- Are horizontal and vertical object permissions enforced server-side?
- Are redirect, state, code, device binding, and token audience validated?
- Does a leaked client signing key grant a real server capability?
- Can production and non-production identities or objects cross boundaries?
- Can an upload be consumed in a more privileged preview, renderer, parser, or workflow?

## Evidence gate

Record a redacted request/response pair, ownership model, control matrix, exact observed data or state change, time, app version, and cleanup. Do not claim account takeover, financial impact, or sensitive-data exposure from a success code alone.

Stop when no normal account exists, all useful operations are uniformly gated, only public configuration is exposed, or testing would require guessing third-party identifiers.
