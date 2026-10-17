# Safety, limitations and pre-deployment checks — agent-fleet

**Scope:** Coordination of multiple automated tasks and workers acting on local systems and external services.  
**Issued:** 2026-10-17  
**Status:** Risk guidance, **not** a safety certification, compliance approval, or verified representation that technical controls have been implemented.

This document is meant to help users and maintainers identify foreseeable risks and the checks **they still need to perform**. It supplements [DISCLAIMER.md](DISCLAIMER.md) and the existing software license; it does not override either or remove non-waivable duties.

## Material risks to assess

- Concurrent workers may overwrite files, perform duplicate operations or exceed external provider rate limits.
- Browser or terminal automation may expose credentials, create unintended purchases or messages, or modify third-party accounts.
- Untrusted task instructions and outputs may cause tool misuse or an incorrect 'completed' status.

## Required assessment before consequential deployment

- [ ] Enforce bounded concurrency, permission scopes, domain allowlists, budgets and human approval for high-impact operations.
- [ ] Test task claiming, cancellation, cleanup, stale locks, retries, idempotency and rollback.
- [ ] Keep credentials out of prompts and logs; do not bypass authentication, CAPTCHAs or third-party protections.
- [ ] Verify task completion using independent evidence and apply an emergency stop before high-impact use.

## Operational conditions

- Start with an isolated, disposable environment and the least privileges possible.
- Do not infer that a feature claim in project documentation proves that the safeguard is effectively enforced in every execution path. Perform threat modeling and independent testing.
- Independently validate material outcomes. Preserve audit evidence, tested version, configuration, dependencies, approver identity and incident response arrangements where appropriate.
- Before exposing a networked service, inspect authentication, authorization, logging, data handling, supply chain and applicable laws.
- Pause deployment when unresolved critical flaws, missing permissions, unexplained automation, or inaccurate claims are discovered. Route security reports privately rather than disclosing exploitable details in public issues.

**Important:** Project maintainers and users remain subject to applicable mandatory safety, privacy, security and product laws. A disclaimer does not substitute for these checks or guarantee immunity from claims.
