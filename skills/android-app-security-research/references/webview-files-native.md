# WebView, Files, Loaders, And Native Inputs

## Web content

Map every content source, navigation callback, origin check, bridge object, bridge method, file-access setting, download callback, and browser handoff. Prove that attacker-controlled content reaches the target WebView under the claimed origin before testing a sensitive bridge.

A bridge method or weak-looking allowlist is only a candidate until an untrusted origin can invoke a protected data or operation path.

## Files and archives

Trace the complete path from share, import, download, restore, or provider input to the exact target file. Check decoding and normalization order, archive entry handling, filename collisions, parent-directory permissions, replacement semantics, and cleanup.

Use harmless marker files. Never overwrite irreplaceable user or system data.

## Dynamic content

Before pursuing code execution, prove the consumer:

1. the current version loads the exact script, archive, module, library, or executable content;
2. the full resolved path and timing are observed;
3. the attacker path can control the required bytes and metadata;
4. signature, hash, mode, ownership, and platform loader checks are understood;
5. the consumer can be triggered from the stated attacker context.

Writable content without a consumer is a file primitive, not code execution.

## Native parsers

Identify untrusted formats that reach JNI or native libraries, then preserve sample provenance and reduce inputs. Treat a crash as a triage signal. A security finding requires a realistic input channel and evidence of memory corruption, data exposure, control-flow impact, or another concrete boundary violation.
