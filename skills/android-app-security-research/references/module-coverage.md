# Android Module Coverage

Use these states:

- `U`: unreviewed
- `I`: inventoried
- `S`: static path traced
- `D`: dynamically tested
- `C`: closed with controls, evidence, and a reopen condition

Create a table containing module, entry, authentication or permission, object fields, file or dynamic content, privileged consumer, validation, state, and next action.

Cover only features that exist, including account/device binding, core business objects, Web or cross-platform containers, download/update/cache, IPC/system integration, push/jobs/callbacks, and native or hardware-backed features.

Before time-boxing a substantial app:

1. inventory every DEX and feature root;
2. map network clients, routes, databases, jobs, dynamic containers, and native libraries;
3. test at least three cross-module high-impact hypotheses;
4. record untested modules and exact reopen prerequisites.

A single component, bridge, parser, or loader does not establish app-wide coverage.
