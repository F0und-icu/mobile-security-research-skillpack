# Android Evidence And Reporting

Include package, version, signer/source, device, OS build, root state, component or endpoint, attacker app identity, permissions, exact input, timestamped output, and controls.

Use these terms precisely:

- reachable: the caller enters the interface;
- path reached: business logic executes;
- exposed data: real protected data is returned;
- unauthorized operation: a protected self-owned state changes;
- diagnostic: a hook, mock, or synthetic fixture demonstrates code behavior only.

Keep proof self-contained and minimally reproducible. Place screenshots beside the step they prove. Preserve raw evidence privately and publish only redacted material. Never show full tokens, cookies, account identifiers, payment data, private content, or stable hardware identifiers unless essential, authorized, and safely redacted.

For destructive or state-changing tests, record original state, changed state, restoration, hashes where useful, and removal of test applications or files.
