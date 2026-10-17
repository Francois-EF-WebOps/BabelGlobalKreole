# Music, lyrics and poetry application track

## Purpose

This track supports original music, lyrics and poetry as consumers of BabelGlobalKreole. Creative work does not establish or redefine attested language facts.

## Record contract

Use `schemas/creative-work.schema.json`. Each work must declare its author, owner-selected license, AI-use flags, language/variety/orthography scope where known, record IDs used, label, status, and generation method. Generation method is `human`, `ai-assisted`, or `ai-generated`; AI-assisted/generated work must name the tool and record whether its terms were verified.

## Rights and evidence

- Do not ingest or quote third-party lyrics, poems, recordings, samples, translations or dictionary material unless the specific license permits the exact intended operation and all necessary permissions/consent are established.
- A source citation does not grant permission to reproduce or train on its contents.
- Owner-contributed works remain unpublished until the owner chooses the license and each AI-use flag.
- Preserve attribution and provenance; do not imply that generated lyrics are attested community usage.
- Separate factual language constraints from rhyme, meter, genre, persona and performance choices.

## Labels

- `creative_coinage`: original or newly composed creative material.
- `application_canon`: material established as canon for a specific application.
- Neither label means the text is an attested lexical or grammatical source.

## LLM use

Only perform retrieval, training, speech generation or synthetic-data use when the work's corresponding AI-use flag and rights permit that operation. `unknown`, `permission-required`, or missing permission blocks reuse. Do not send third-party protected text to a model merely because it is publicly viewable.

## Current evidence state

No owner work is published in this track. A sample record is intentionally withheld until the owner approves a specific work, license, and AI-use flags; this avoids publishing fabricated metadata as if it represented a real work.
