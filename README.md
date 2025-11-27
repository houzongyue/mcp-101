# FastMCP Demo

A minimal FastMCP demo with stdio and HTTP transports.

## Install

```bash
uv sync
```

## Files

- `server_stdio.py` - MCP server (stdio transport), provides `add` and `subtract` tools
- `server_http.py` - MCP server (HTTP transport), provides `multiply` tool, supports both SSE (legacy) and Streamable HTTP
- `test_server.py` - Automated tests

## Testing

### Test methods

| Method | Transport | How it works | Scope | Use case |
|--------|-----------|--------------|-------|----------|
| In-memory | Both | Client connects to MCP instance directly in same process | Tool logic | Unit testing, fast CI feedback |
| Subprocess | stdio | Client spawns subprocess, communicates via stdin/stdout | Tool + process + protocol | Integration testing, CI friendly |
| Network | HTTP | Client connects to running server via HTTP | Tool + process + protocol + network | Integration testing, requires running server |
| Claude Code | Both | Real MCP client connects to server | Full integration | End-to-end validation |

### Run tests

```bash
# Without HTTP server (in-memory + subprocess)
uv run pytest test_server.py -q -k "not network"

# With HTTP server (all tests, use SSE for test compatibility)
uv run python server_http.py --transport sse  # in another terminal
uv run pytest test_server.py -q
```

## Test with Claude Code

The project includes `.mcp.json` (project-level config, only works when Claude Code is launched from this directory) with two server configs:

- `demo-stdio` - Auto-started by Claude Code
- `demo-http` - Requires manually starting the server first

### stdio server

```bash
claude
```

Once in the session, type `/mcp` to verify, then test:

```
Use the add tool to calculate 2 + 3
```

### HTTP server

Start the server first:

```bash
# Streamable HTTP (recommended)
uv run python server_http.py

# Or SSE (legacy)
uv run python server_http.py --transport sse
```

Then in Claude Code:

```
Use the multiply tool to calculate 2 * 3
```

## Test with Codex CLI

Codex CLI supports MCP via global config (`~/.codex/config.toml`). Project-level config is not yet supported ([feature request](https://github.com/openai/codex/issues/3120)).

### stdio server

```bash
codex mcp add demo-stdio -- uv run python server_stdio.py
```

### HTTP server

```bash
# Start server first
uv run python server_http.py

# Add HTTP server with url parameter
codex mcp add demo-http --url http://localhost:8000/mcp
```

Note: Use `--url` flag for HTTP servers, not `--` with a command. The `--url` flag tells Codex to connect directly via HTTP.

### Remove servers

```bash
codex mcp remove demo-stdio
codex mcp remove demo-http
```

## HTTP transport comparison

| Transport | Endpoint | Claude Code | Codex CLI |
|-----------|----------|-------------|-----------|
| SSE | `/sse` | ✅ | ❓ |
| Streamable HTTP | `/mcp` | ✅ | ✅ |

## MCP config comparison

| | Claude Code | Codex CLI |
|---|-------------|-----------|
| Global config | `~/.claude/settings.json` | `~/.codex/config.toml` |
| Project config | `.mcp.json` ✅ | ❌ Not supported |
| CLI command | `claude mcp add` | `codex mcp add` |

## Global config (Claude Code)

To make MCP servers available to all projects:

```bash
claude mcp add demo-stdio -- uv run python server_stdio.py
```

To remove:

```bash
claude mcp remove demo-stdio
```
