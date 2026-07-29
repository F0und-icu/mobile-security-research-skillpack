# Traffic Research Workflow

Use this workflow for native apps, mini-apps, embedded H5, cross-platform containers, and mobile APIs.

## 1. Decide whether proxy traffic is enough

A proxy is usually enough when bodies are readable, authentication is a normal cookie or bearer field, requests replay cleanly, and parameter changes produce interpretable errors.

Instrument the app when:

- request or response bodies use business-layer encryption;
- signatures, nonces, timestamps, request identifiers, or device fields are dynamic;
- WebView or browser login traffic bypasses the assumed native stack;
- replay fails because serialization or hidden headers differ;
- a custom or native transport obscures the application-layer request.

The proxy proves what left the device. Instrumentation explains how it was generated. Use both when reconstructing a protocol.

## 2. Capture the normal state machine

Record these flows before testing:

```text
registration or onboarding
login and multi-factor steps
token or session refresh
profile or account bootstrap
device binding and trust
one harmless object read
one reversible self-owned state change
logout and revocation
```

For each request identify host, path, method, content type, authentication fields, signature fields, object fields, role context, response identity, and state transition.

## 3. Classify fields

Do not change all identity-looking fields together. Classify each as:

- session credential;
- user or account selector;
- tenant, organization, family, or merchant selector;
- business object identifier;
- device or installation identifier;
- anti-replay value;
- request-integrity signature;
- telemetry or risk input;
- presentation-only client field.

Change one field at a time and compare with the normal control.

## 4. Reconstruct signatures safely

Determine:

1. which fields participate;
2. their exact order or canonical serialization;
3. normalization of null, booleans, numbers, arrays, and Unicode;
4. timestamp, nonce, and replay window;
5. key derivation or decoding;
6. digest or MAC encoding;
7. whether a user credential is independently required.

Use self-owned requests and print hashes or lengths rather than secrets. A reproduced signature shows client-integrity behavior; prove a server-side capability before calling it an authentication bypass.

## 5. Build an authorization matrix

Use only legitimate test identities and self-owned objects:

| Session | Role | Object | Expected |
| --- | --- | --- | --- |
| Account A | normal | A1 | allow |
| Account A | normal | A2 | allow if same owner |
| Account A | normal | B1 from Account B | deny |
| Account B | normal | B1 | allow |
| lower test role | lower | permitted object | limited allow |
| missing or invalid | none | public or private fixture | public only or deny |

If a second account or role is not legitimately available, preserve the model and stop. Do not substitute guessed identifiers.

## 6. Test session and OAuth-style boundaries

Review:

- state and redirect binding;
- authorization-code single use and client binding;
- token audience, scope, expiry, refresh, logout, and revocation;
- account switching and stale session reuse;
- device trust and recovery transitions;
- browser-to-app callback ownership;
- server-side binding between the session and client-supplied identity fields.

Distinguish anonymous access, authenticated cross-object access, and role bypass in the final wording.

## 7. Test environment isolation

Map only environments exposed by the authorized client or documentation. Compare authentication audience, object namespace, storage, callbacks, and state consumers. An alternate environment accepting a token is not enough; prove protected data or an authorized reversible state effect.

## 8. Test upload consumers

Use a benign marker first. Separate:

```text
who can upload
who owns the returned object
who can preview/download/replace/delete
which renderer or parser consumes it
which role or origin receives the result
whether active content or paths are normalized
```

Upload success alone is not stored script execution, file overwrite, or code execution.

## 9. Preserve reproducible evidence

Keep:

- a redacted raw request and response;
- a field classification table;
- signature or encryption call-site evidence;
- the authorization control matrix;
- before, after, and restored object states;
- app and device versions;
- exact tool and hook versions;
- a statement separating observation hooks from the final attack path.

Label incomplete states precisely:

```text
proxy sample only; protocol generation not reconstructed
protocol generation reconstructed; vulnerability impact not validated
authorization boundary validated with self-owned controls
diagnostic bypass only; no realistic attacker path
```

## 10. Stop conditions

Stop when login or the business object cannot be obtained normally, requests are uniformly gated, only public configuration remains, the next step requires third-party records, or the path has no protected consumer. Record the missing prerequisite and first action for a future reopen.
