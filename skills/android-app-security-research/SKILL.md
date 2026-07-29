---
name: android-app-security-research
description: Authorized Android application security research workflow for APK triage, exported components, Binder and ContentProvider boundaries, WebView and JavaScript bridges, file handling, dynamic code loading, native input paths, device evidence, and conservative finding validation. Use when assessing an Android app or system component without relying on vendor-specific knowledge.
---

# Android App Security Research

Use an evidence-first workflow. Treat static reachability as a hypothesis until a supported app version and a realistic attacker path prove a concrete security impact.

## Start safely

1. Confirm written authorization, asset scope, allowed accounts, rate limits, and prohibited actions.
2. Record package name, version, signer, source, device model, OS build, security patch, root state, and test date.
3. Use self-owned accounts, objects, files, and devices. Stop if a response unexpectedly contains third-party data.
4. Preserve the original app and device state before replacing packages, files, settings, or business objects.

## Build the attack-surface map

Inventory every DEX and relevant native library. Map:

- exported activities, services, receivers, providers, permissions, URI grants, and pending intents;
- Binder descriptors, transaction handlers, caller identity checks, and privileged deputies;
- deep links, custom schemes, app links, WebViews, bridge methods, and origin checks;
- imports, shares, downloads, archives, backups, plugins, updates, scripts, and code-loading consumers;
- local databases, preferences, logs, credentials, and cross-user or work-profile boundaries;
- network clients, authentication fields, object identifiers, upload/download consumers, and native parsers.

Use [references/android-analysis-playbook.md](references/android-analysis-playbook.md) for the detailed acquisition, static search, runtime, and evidence sequence. Read [references/android-ipc.md](references/android-ipc.md) for component and IPC work. Read [references/webview-files-native.md](references/webview-files-native.md) for content, file, loader, and native boundaries.

## Prioritize complete paths

Prefer hypotheses that join an attacker-controlled input to a sensitive consumer:

```text
ordinary app or remote content
  -> exposed or confused trust boundary
  -> target process or backend capability
  -> protected data, privileged state, installation, or code execution
```

An exported component, callable transaction, writable filename, bridge method, parser, or loader is not a vulnerability by itself. Prove the final data or operation and state every precondition.

## Validate dynamically

1. Start with read-only or no-op requests.
2. Establish a positive baseline and at least one negative control.
3. Run the final proof from the stated attacker context. Use root, ADB, instrumentation, and hooks only to observe or prepare controlled fixtures.
4. Record target PID/UID, caller package/UID, permissions, exact input, exact checkpoint, and observed result.
5. For state changes, use reversible self-owned objects and capture before, after, and restored states.
6. Recheck the latest supported version before promoting the finding.

Use [references/module-coverage.md](references/module-coverage.md) before declaring a substantial app reviewed. Use [references/evidence-reporting.md](references/evidence-reporting.md) for proof and report quality.

When traffic, WebView, cryptography, or native behavior needs runtime observation, route to `mobile-auth-traffic-analysis` and load its Android hook recipes. Preserve the distinction between an observation hook and the final attacker path.

## Promotion gate

Promote a finding only when all answers are clear:

- Is the asset and tested version in scope?
- Can a realistic ordinary app, remote origin, or normal user reach it?
- What protected data or operation is observed?
- Does the proof work without diagnostic-only privileges?
- Are positive and negative controls included?
- Are prerequisites, interaction, cleanup, and limitations explicit?
- Is the root cause distinct from already recorded findings?

Otherwise label it as inventory, candidate, diagnostic evidence, or blocked by a named prerequisite.

## Stop conditions

Stop or time-box a direction when it has only static flags, fabricated responses, old-version behavior, root-only reachability, a crash without security impact, an empty result, or a primitive with no sensitive consumer. Record the exact condition that would justify reopening it.
