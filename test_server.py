"""Test MCP servers"""

import pytest
from fastmcp import Client
from fastmcp.client.transports import PythonStdioTransport
from server_stdio import mcp_stdio
from server_sse import mcp_sse


# In-memory tests: Client connects directly to MCP instance, no real server process
@pytest.mark.asyncio
async def test_stdio_in_memory():
    """Test stdio server (in-memory)"""
    async with Client(mcp_stdio) as client:
        result = await client.call_tool("add", {"a": 2, "b": 3})
        assert result.data == 5


@pytest.mark.asyncio
async def test_sse_in_memory():
    """Test SSE server (in-memory)"""
    async with Client(mcp_sse) as client:
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
