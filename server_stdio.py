"""FastMCP server with stdio transport"""

from fastmcp import FastMCP

mcp_stdio = FastMCP("Demo Server")


@mcp_stdio.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


if __name__ == "__main__":
    mcp_stdio.run()
