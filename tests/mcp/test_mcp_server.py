import sys
import unittest
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parents[2]


class MCPServerSmokeTests(unittest.IsolatedAsyncioTestCase):
    async def test_server_exposes_only_read_tools(self):
        parameters = StdioServerParameters(
            command=sys.executable,
            args=["-m", "mcp_server.server"],
            cwd=str(ROOT),
        )
        async with stdio_client(parameters) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                response = await session.list_tools()
        names = {tool.name for tool in response.tools}
        self.assertEqual(
            names,
            {"search_babel_records", "get_babel_record", "get_babel_catalog"},
        )


if __name__ == "__main__":
    unittest.main()
