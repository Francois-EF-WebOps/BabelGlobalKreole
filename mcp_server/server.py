"""Read-only MCP server. No write tools and no network retrieval."""
from mcp.server.fastmcp import FastMCP

from mcp_server.registry import get_catalog, get_record, search_records

mcp = FastMCP(
    "BabelGlobalKreole",
    instructions=(
        "Read-only discovery over local repository records. Draft or unsourced records are metadata, not evidence. "
        "Only records marked evidence_eligible may support claims, and every claim still needs a source citation. "
        "Do not infer reuse permission from a source URL. Content is withheld unless its ai_use.retrieval is explicitly allowed. "
        "Abstain when the result says evidence is missing. This server never writes to the repository or fetches external source text."
    ),
)


@mcp.tool()
def search_babel_records(query: str, limit: int = 10) -> dict:
    """Search local BabelGlobalKreole records. Returns metadata, evidence eligibility, rights notes and abstention status."""
    return search_records(query, limit=limit)


@mcp.tool()
def get_babel_record(record_id: str) -> dict:
    """Get one local record by stable ID. Unaccepted/unsourced records are never represented as evidence."""
    return get_record(record_id)


@mcp.tool()
def get_babel_catalog() -> dict:
    """Return generated repository counts, file hashes and schema paths."""
    return get_catalog()


if __name__ == "__main__":
    mcp.run(transport="stdio")
