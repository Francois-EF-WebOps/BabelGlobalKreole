# Repository audit — initial evidence

**Audit date:** 2026-10-17. This is a selected-file audit, not a complete source-tree, security, licence, build or runtime audit.

| Repository | Evidence observed | Decision |
|---|---|---|
| `mascarene-knowledge-commons` | Existing coordination/discovery documentation and Babel-to-Mooritian handover distinguish real-language evidence from fictional canon. | Keep as coordination layer; link to this framework, do not duplicate canonical data. |
| `Applied-Creole-Linguistics` | Public React/Vite prototype. README is generic AI Studio scaffold; package/app title indicates “SCR - Mauritius | Repository” with pages for foundation, hierarchy, phonetics, contribution, SEO and roadmap. Vite config maps `GEMINI_API_KEY`/`API_KEY` into client-side definitions. | Preserve. Audit pages/components, actual key usage and build output before reuse. This does not prove a live key has leaked. |
| `Refuge` | React/Vite prototype called `mascarene-refuge-hypothesis-s01-explorer`; embeds hypothesis content in root constants. Vite config maps `GEMINI_API_KEY`/`API_KEY` into client-side definitions. | Preserve. Compare embedded content with research source and check rights, provenance, secret usage and runtime. |
| `Mascarene-Refuge-Hypothesis-S01` | README identifies Stage 01 research/preprint materials and contains a CC BY-SA 4.0 notice. Individual assets/licence scope not fully audited. | Link as research source; verify item-level rights before reuse. |

## Remaining audit tasks
1. Retrieve full file trees and commit history for Applied-Creole-Linguistics and Refuge.
2. Inspect manifests, source entry points, assets, environment examples and API-key handling without exposing secrets.
3. Verify project exports and runtime where feasible.
4. Locate exact Babel Creole, Down by the Shore, music and TTS source repositories.
5. Compare embedded/standalone research content before selecting canonical sources or adapters.
6. Record paths, commit SHAs, test evidence and unresolved gaps.


## Follow-up verification — 2026-10-17

- Inspected `vite.config.ts` in both `Applied-Creole-Linguistics` and `Refuge`. Both use Vite's `define` to substitute `env.GEMINI_API_KEY` into browser-bundle identifiers `process.env.API_KEY` and `process.env.GEMINI_API_KEY`. If a real key is supplied at build time, it can be exposed to every user of the built client. This configuration is a confirmed exposure risk; the audit did not establish that a live secret was present in the public bundle.
- Search indexing did not return a complete call-site inventory, so whether each app currently uses the value in client code remains unverified. Before deployment, remove client-side secret substitution and route provider calls through a server-side component, or remove the key-dependent feature. Rotate any real key that may already have been built into or published with a client bundle. Do not commit the replacement secret.
- BabelGlobalKreole now has a full JSON Schema validator in CI, a consumer-agent answer contract, explicit AI-operation rights fields, and external identifier mapping schemas. A passing workflow run must be checked against the latest commit before describing these changes as CI-verified.
- Language-data record counts remain zero. Do not manufacture sample lexical data; the first dataset requires source inspection, exact scope, source locations, and per-operation rights review.
