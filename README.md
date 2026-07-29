# Mobile Security Research Skill Pack

A vendor-neutral Codex skill collection for authorized mobile application security research. The skills turn broad assessment work into a repeatable workflow: establish the product baseline, map trust boundaries, select high-impact hypotheses, validate them with realistic attacker capabilities, and preserve reproducible evidence without overstating incomplete leads.

## Skill capabilities

| Skill | Primary function | Use it for |
| --- | --- | --- |
| [`mobile-vulnerability-research`](skills/mobile-vulnerability-research/SKILL.md) | Platform-neutral assessment entry point and task router | Android and iOS attack-surface planning, mobile APIs, deep links, WebViews, local storage, file/update flows, native parsers, hypothesis scoring, and time-box selection |
| [`android-app-security-research`](skills/android-app-security-research/SKILL.md) | Android application and system-component research | APK acquisition, manifest/JADX search, exported components, Binder, ContentProvider, URI grants, WebView bridges, file handling, dynamic loaders, JNI/native paths, runtime evidence, and finding validation |
| [`mobile-auth-traffic-analysis`](skills/mobile-auth-traffic-analysis/SKILL.md) | Mobile authentication, Hook, and business-API analysis | Android/iOS Frida recipes, WebView/WebKit observation, native HTTP stacks, crypto/signing hooks, cookies, keychain calls, login/session flows, OAuth-style boundaries, object authorization, environment isolation, and safe control matrices |
| [`vulnerability-research-process-control`](skills/vulnerability-research-process-control/SKILL.md) | Long-running research coordination and quality control | Detailed research cycle, target ledgers, root-cause deduplication, module coverage, maturity levels, time boxes, stop/reopen rules, cleanup, experience cards, handoff, and report promotion gates |

## How the skills work together

Start with `mobile-vulnerability-research` when the target is new or spans several platforms. Route Android-specific component and local-boundary work to `android-app-security-research`, route authentication and backend-object questions to `mobile-auth-traffic-analysis`, and use `vulnerability-research-process-control` throughout multi-target or multi-session projects.

```text
scope and baseline
  -> mobile attack-surface map
  -> Android or authentication deep dive
  -> realistic attacker-path validation
  -> controls and evidence
  -> verified finding, precise blocker, or stop/reopen record
```

The pack consistently separates interface reachability, diagnostic behavior, candidate primitives, verified impact, and report-ready findings. Root, jailbreak, ADB, instrumentation, and proxies may help observe a path, but they do not replace the claimed attacker capability.

## Included references

The skill references provide reusable guidance for:

- Android APK acquisition, static searches, IPC, providers, WebViews, file consumers, loaders, native inputs, and runtime evidence;
- Android/iOS mobile attack-surface coverage;
- concrete Android and iOS Frida observation hooks for network, WebView/WebKit, cryptography, cookies, keychain, and native functions;
- authentication, session, signature, OAuth, role, environment, upload, and object-authorization modeling;
- evidence terminology, redaction, reproducibility, and conservative reporting;
- full target workflows, workspace templates, maturity levels, deduplication, time boxes, experience transfer, stop conditions, and handoff.

Each directory under `skills/` is an independent installable skill with its own `SKILL.md`, UI metadata, and focused references.

## Publication safety check

The repository includes a deterministic scanner for common publication risks:

```bash
python3 scripts/scan_publication_risks.py .
```

It checks for vendor or private-program identifiers, ticket patterns, absolute user paths, non-example domains and package names, IP addresses, and credential-like assignments. Manual review is still required.

Use these skills only on assets for which you have explicit authorization. Prefer self-owned accounts, devices, files, and business objects; avoid third-party data and irreversible state changes.
