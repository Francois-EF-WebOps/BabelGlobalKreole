# Offline retrieval demo

Run from the repository root:

```sh
python demo/retrieval/demo.py "Mauritian Creole"
python demo/retrieval/demo.py "lng-mauritian-creole"
python -m unittest discover -s tests/retrieval -v
```

The demo searches local JSONL metadata only. It never fetches source text, never cites a record that is draft/proposed or has missing, empty, or unresolved `source_ids`, and validates every answer against `agents/consumer-answer.schema.json`. When evidence is missing it abstains. The current candidate records are drafts, so a query for them should abstain rather than make a linguistic claim.

This is a read-only local demonstration, not an API or MCP server. Test fixtures use synthetic metadata only to test the program's control flow; they are not language data and are not part of the published corpus.
