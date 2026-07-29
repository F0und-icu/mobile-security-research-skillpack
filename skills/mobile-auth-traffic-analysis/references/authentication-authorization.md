# Authentication And Authorization

Separate:

- authentication: who the server believes the caller is;
- session management: how that identity is issued, refreshed, scoped, and revoked;
- object selection: which resource the request names;
- authorization: whether that identity may perform the requested action;
- integrity: whether client-supplied fields or signatures prevent unauthorized changes.

Build a matrix using only self-owned accounts and objects. Compare same-owner objects, legitimately available second accounts or roles, missing authentication, invalid authentication, and nonexistent identifiers.

For OAuth-like flows, review redirect binding, state, authorization-code reuse, client binding, token audience, device binding, and account switching. For signed APIs, prove the leaked or reconstructed client secret enables a real server capability; client possession alone is not a finding.

Stop immediately if a response contains third-party data. Do not enumerate nearby identifiers, scrape user records, or perform irreversible financial, identity, or account operations.
