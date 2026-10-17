# Repository audit — initial evidence

**Audit date:** 2026-10-17. This is a scoped repository and configuration review; public bundle history, full runtime behaviour and item-level licensing remain outside what was verified.

| Repository | Evidence observed | Decision |
|---|---|---|
| `mascarene-knowledge-commons` | Existing coordination/discovery documentation and Babel-to-Mooritian handover distinguish real-language evidence from fictional canon. | Keep as coordination layer; link to this framework, do not duplicate canonical data. |
| `Applied-Creole-Linguistics` | Public React/Vite prototype. Repository search found no `GoogleGenAI`, `process.env.API_KEY`, `process.env.GEMINI_API_KEY`, or `GEMINI_API_KEY` call sites beyond the Vite configuration and README instructions. | [Security PR #2](https://github.com/Francois-EF-WebOps/Applied-Creole-Linguistics/pull/2) removes unused client-side key injection and obsolete README instructions. Open, unmerged; `npm run build` still needs to be run. |
| `Refuge` | React/Vite prototype called `mascarene-refuge-hypothesis-s01-explorer`; its `services/gemini.ts` directly calls Gemini from the browser and reads `process.env.API_KEY`. | [Security PR #2](https://github.com/Francois-EF-WebOps/Refuge/pull/2) removes key injection and disables browser-side AI actions until a server proxy exists. Open, unmerged; build and UI tests remain pending. |
| `Mascarene-Refuge-Hypothesis-S01` | README identifies Stage 01 research/preprint materials and contains a CC BY-SA 4.0 notice. Individual assets/licence scope not fully audited. | Link as research source; verify item-level rights before reuse. |

## Remaining audit tasks
1. Review the complete commit history and any previously deployed client bundles for accidental credential exposure; no real key was observed in this review.
2. Run `npm run build` and exercise the AI-related UI after the security PRs are reviewed; neither repository has a GitHub Actions build workflow.
3. Compare project exports and embedded research content with canonical sources before selecting adapters.
4. Locate exact Babel Creole, Down by the Shore, music and TTS source repositories.
5. Compare embedded/standalone research content before selecting canonical sources or adapters.
6. Record paths, commit SHAs, test evidence and unresolved gaps.


## Follow-up verification — 2026-10-17

- Inspected `vite.config.ts` in both `Applied-Creole-Linguistics` and `Refuge`. Both use Vite's `define` to substitute `env.GEMINI_API_KEY` into browser-bundle identifiers `process.env.API_KEY` and `process.env.GEMINI_API_KEY`. If a real key is supplied at build time, it can be exposed to every user of the built client. This configuration is a confirmed exposure risk; the audit did not establish that a live secret was present in the public bundle.
- Follow-up repository search found no Gemini call sites in Applied-Creole-Linguistics. Refuge has two client-side AI call sites; its PR disables those functions while preserving their exports. Both security PRs are open and unmerged. No real key was read or rotated. If a real key was ever embedded in a public bundle, rotate it in the provider console; do not commit the replacement secret.
- BabelGlobalKreole now has a full JSON Schema validator in CI, a consumer-agent answer contract, explicit AI-operation rights fields, and external identifier mapping schemas. A passing workflow run must be checked against the latest commit before describing these changes as CI-verified.
- The current core data contains 19 accepted catalogue-level language records with Glottolog IDs and source records, 1 sourced Martinican variety, 50 source records, 1 APiCS-attributed lexical entry, 3 sourced Mauritian Creole grammar claims, and 1 organizing concept. The 24 unsourced variety placeholders were removed; unsupported candidates are documented in `docs/language-coverage.md`. No dictionary, corpus or third-party examples were mirrored. The first lexical and grammar records use APiCS material licensed CC BY 4.0 with attribution; training, speech-generation and synthetic-data permissions remain unknown.
