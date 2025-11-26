# FastMCP Demo

A minimal FastMCP local MCP server demo.

## Install

```bash
uv sync
```

## Files

- `server_stdio.py` - MCP server (stdio transport), provides `add` tool
- `server_sse.py` - MCP server (HTTP/SSE transport), provides `multiply` tool
- `test_server.py` - Unit tests (in-memory + subprocess)

## Run tests

```bash
uv run pytest test_server.py -q
```

### Test methods

| Method | Transport | How it works | Speed | Scope |
|--------|-----------|--------------|-------|-------|
| In-memory | stdio/SSE | Client connects to MCP instance directly in same process | Fast | Tool logic |
| Subprocess | stdio | Client spawns subprocess, communicates via stdin/stdout | Medium | Tool + process + protocol |
| Network | SSE | Client connects to running server via HTTP | Slow | Tool + process + protocol + network |
| Claude Code | stdio | CC spawns subprocess, communicates via stdin/stdout | Medium | Full integration |
| Claude Code | SSE | CC connects to running server via HTTP | Slow | Full integration |

This project implements: in-memory (both), subprocess (stdio), Claude Code (both).

Network test for SSE is not implemented due to environment limitations.

## Run SSE server

```bash
uv run python server_sse.py
```

Server runs at `http://localhost:8000/sse`.

## Test with Claude Code

Claude Code can act as an MCP client to connect to your server directly.

The project includes `.mcp.json` with two server configs:

- `demo-stdio` - Auto-started by Claude Code (no manual setup)
- `demo-sse` - Requires manually starting the server first

### Test stdio server

```bash
claude
```

Once in the session, type `/mcp` to verify the MCP server is loaded, then test:

```
Use the add tool to calculate 2 + 3
```

### Test SSE server

First start the server in a separate terminal:

```bash
uv run python server_sse.py
```

Then start Claude Code and test:

```
Use the multiply tool to calculate 2 * 3
```

### Global config (optional)

To make MCP servers available to all projects:

```bash
claude mcp add demo-stdio -- uv run python server_stdio.py
```

**Note**: This writes to `~/.claude/settings.json`. To remove:

```bash
claude mcp remove demo-stdio
```
