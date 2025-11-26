# FastMCP Demo

A minimal FastMCP demo with stdio and SSE transports.

## Install

```bash
uv sync
```

## Files

- `server_stdio.py` - MCP server (stdio transport), provides `add` tool
- `server_sse.py` - MCP server (SSE transport), provides `multiply` tool
- `test_server.py` - Automated tests

## Testing

### Test methods

| Method | Transport | How it works | Scope | Use case |
|--------|-----------|--------------|-------|----------|
| In-memory | Both | Client connects to MCP instance directly in same process | Tool logic | Unit testing, fast CI feedback |
| Subprocess | stdio | Client spawns subprocess, communicates via stdin/stdout | Tool + process + protocol | Integration testing, CI friendly |
| Network | SSE | Client connects to running server via HTTP | Tool + process + protocol + network | Integration testing, requires running server |
| Claude Code | Both | Real MCP client connects to server | Full integration | End-to-end validation |

### Run tests

```bash
# Without SSE server (in-memory + subprocess)
uv run pytest test_server.py -q -k "not network"

# With SSE server (all tests)
uv run python server_sse.py  # in another terminal
uv run pytest test_server.py -q
```

## Test with Claude Code

The project includes `.mcp.json` (project-level config, only works when Claude Code is launched from this directory) with two server configs:

- `demo-stdio` - Auto-started by Claude Code
- `demo-sse` - Requires manually starting the server first

### stdio server

```bash
claude
```

Once in the session, type `/mcp` to verify, then test:

```
Use the add tool to calculate 2 + 3
```

### SSE server

Start the server first:

```bash
uv run python server_sse.py
```

Then in Claude Code:

```
Use the multiply tool to calculate 2 * 3
```

## Global config (optional)

To make MCP servers available to all projects:

```bash
claude mcp add demo-stdio -- uv run python server_stdio.py
```

To remove:

```bash
claude mcp remove demo-stdio
```
