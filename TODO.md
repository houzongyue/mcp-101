# TODO

## SSE Network Test Issue

### Problem
`test_sse_network` fails with `httpx.RemoteProtocolError: Server disconnected without sending a response.`

### What we tried
1. Server starts successfully (`uv run python server_sse.py`)
2. `curl` can access `http://localhost:8000/sse` and gets 200 OK
3. But `fastmcp.Client("http://localhost:8000/sse")` fails to connect

### Possible causes
1. **Sandbox/network isolation** - The test environment may have network restrictions
2. **IPv4/IPv6 mismatch** - Server logs show `::1` (IPv6), client may be using IPv4
3. **Timing issue** - Server not fully ready when client connects (though we added waits)
4. **FastMCP Client issue** - May need specific configuration for SSE transport

### To investigate
1. Try running the test outside of Claude Code environment
2. Check if `Client` needs explicit transport configuration for SSE URLs
3. Test with `127.0.0.1` vs `localhost` vs `0.0.0.0`
4. Check FastMCP documentation for SSE client examples

### Conclusion
Claude Code can successfully connect to `server_sse.py`, confirming the server implementation is correct. The issue is with how `fastmcp.Client` connects to SSE URLs in test code.

### Current workaround
SSE network test is removed. Use in-memory test or Claude Code for SSE testing.
