from fastmcp import FastMCP
from tools import register_tools
from prompts import register_prompts

mcp = FastMCP(name="Demo MCP Server")

register_tools(mcp)
register_prompts(mcp)

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=9001)
