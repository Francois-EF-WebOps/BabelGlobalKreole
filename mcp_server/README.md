# Read-only MCP server

This optional MCP server exposes three tools over local repository files:

- `search_babel_records(query, limit)`
- `get_babel_record(record_id)`
- `get_babel_catalog()`

It has no write tools, does not fetch external source text, and does not make provider calls. Draft records are returned as metadata, not evidence. Evidence eligibility requires an accepted record whose source IDs resolve to source records with canonical URLs, access dates, and precise locations. Textual content is withheld unless the record explicitly marks `ai_use.retrieval` as `allowed`.

## Run

From the repository root, install the optional dependency and run:

```sh
python -m pip install -r requirements-mcp.txt
python -m mcp_server.server
```

The process uses MCP stdio transport. Configure your MCP client to launch this command with the repository root as its working directory. Do not expose it as a network service without an independent authentication and deployment review.

## Current limitations

The server is a read-only discovery adapter, not a natural-language answering agent or a replacement for the offline retrieval demo. Most language/variety records are drafts and there are no lexical or grammar records, so many searches correctly abstain. Linked resource URLs and source IDs do not grant content reuse, training, or speech-generation permission.
