"""FastMCP server with HTTP transport (supports SSE and Streamable HTTP)"""

import argparse
from fastmcp import FastMCP

mcp_http = FastMCP("Demo Server")


@mcp_http.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--transport", choices=["sse", "http"], default="http",
                        help="Transport type: sse (legacy) or http (streamable, default)")
    args = parser.parse_args()

    mcp_http.run(transport=args.transport, host="0.0.0.0", port=8000)
