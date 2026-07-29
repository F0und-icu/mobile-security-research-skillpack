# Android Components And IPC

## Inventory

Record each component's exported state, intent filters, authority or action, required permission, URI grants, caller checks, and final data or operation. For Binder, record how an ordinary application discovers or binds the service, its descriptor, read-only transactions, and every UID, package, signature, or capability check.

## Validation order

1. Confirm the component exists on the tested version.
2. Test discovery or binding from an ordinary application with a minimal manifest.
3. Query the interface or descriptor before invoking business methods.
4. Start with read-only, empty, or self-owned inputs.
5. Trace caller identity through wrappers and privileged processes to the final sink.
6. Compare direct access failure with delegated access when testing a confused deputy.

Do not infer ordinary-app reachability from a shell-visible service. Framework policy, SELinux, signature permissions, URI grants, and downstream checks may independently block access.

## Provider and file checks

For providers, distinguish metadata from actual data or file handles. Test canonical paths, encoded separators, traversal, symlink handling, URI ownership, MIME decisions, and grant lifetime only with controlled files. A permissive query with empty data is inventory, not exposure.

## Safety

Keep mutating transactions disabled by default. Require an explicit self-owned fixture and recovery plan for delete, format, install, policy, account, or framework-state operations. A temporary framework restart is denial of service, not privilege escalation or code execution.
