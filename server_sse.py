"""FastMCP server with HTTP/SSE transport"""

from fastmcp import FastMCP

mcp_sse = FastMCP("Demo Server")


@mcp_sse.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b


if __name__ == "__main__":
    mcp_sse.run(transport="sse", host="0.0.0.0", port=8000)
