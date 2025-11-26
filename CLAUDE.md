# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A minimal FastMCP demo project demonstrating MCP (Model Context Protocol) servers with two transport modes:
- **stdio** - Standard input/output transport (auto-started by Claude Code)
- **SSE** - HTTP Server-Sent Events transport (requires manual server start)

## Commands

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest test_server.py -q

# Start SSE server (required before using demo-sse)
uv run python server_sse.py
```

## Architecture

The project contains two MCP server implementations using FastMCP:

- `server_stdio.py` - Provides `add` tool, runs via stdio transport
- `server_sse.py` - Provides `multiply` tool, runs via HTTP/SSE on port 8000
- `test_server.py` - Tests using in-memory and subprocess transports

MCP server configuration is in `.mcp.json`:
- `demo-stdio` - Auto-started by Claude Code
- `demo-sse` - Connects to `http://localhost:8000/sse` (start server first)

## Testing with Claude Code

For stdio: Simply start Claude Code and use `/mcp` to verify, then test with "Use the add tool to calculate 2 + 3"

For SSE: Start server with `uv run python server_sse.py` in a separate terminal first, then test with "Use the multiply tool to calculate 2 * 3"
