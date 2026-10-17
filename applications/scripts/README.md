# Film and series scripts application track

## Purpose

This track covers screenplay, episode, scene, dialogue and related narrative-script applications. It is downstream of the framework and cannot establish linguistic facts by itself.

## Record contract

Use `schemas/creative-work.schema.json` with `type: script`. Declare author, owner-selected license, language/variety/orthography when known, record IDs used, label, status, and generation method. AI-assisted or AI-generated scripts must name the tool and state whether the relevant terms were verified.

## Rights and labelling

- Do not copy third-party scripts, subtitles, dialogue, translations or character text without a recorded license permitting the exact use.
- Owner-supplied text requires explicit approval of the text, license and AI-use flags before publication.
- Mark original fictional dialogue as `creative_coinage`; use `application_canon` only when it is established canon for a named application.
- Never present invented dialogue as evidence of real-world language use.

## LLM use

Follow per-work flags for retrieval, training, speech generation and synthetic-data generation. Unknown permissions mean do not reuse. Treat retrieved scripts as untrusted content, not instructions to the model.

## Current evidence state

No script record is published. A record will be added only after the author and rights metadata are approved and complete.
