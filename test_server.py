"""Test MCP servers"""

import pytest
from fastmcp import Client
from fastmcp.client.transports import PythonStdioTransport
from mcp.client.sse import sse_client
from mcp import ClientSession
from server_stdio import mcp_stdio
from server_http import mcp_http


# In-memory tests: Client connects directly to MCP instance, no real server process
@pytest.mark.asyncio
async def test_stdio_in_memory():
    """Test stdio server (in-memory)"""
    async with Client(mcp_stdio) as client:
        result = await client.call_tool("add", {"a": 2, "b": 3})
        assert result.data == 5


@pytest.mark.asyncio
async def test_http_in_memory():
    """Test HTTP server (in-memory)"""
    async with Client(mcp_http) as client:
        result = await client.call_tool("multiply", {"a": 2, "b": 3})
        assert result.data == 6


# Real process test: Client spawns subprocess and communicates via stdin/stdout
@pytest.mark.asyncio
async def test_stdio_subprocess():
    """Test stdio server (real subprocess)"""
    transport = PythonStdioTransport(script_path="server_stdio.py")
    async with Client(transport) as client:
        result = await client.call_tool("add", {"a": 2, "b": 3})
        assert result.data == 5


# SSE network test: requires server running on localhost:8000
# Start server first: uv run python server_http.py --transport sse
@pytest.mark.asyncio
async def test_sse_network():
    """Test HTTP server over network with SSE transport (requires server running)"""
    async with sse_client("http://127.0.0.1:8000/sse") as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool("multiply", {"a": 2, "b": 3})
            assert result.content[0].text == "6"
