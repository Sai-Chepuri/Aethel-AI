from tools.mcp_client import McpClient

FIREBASE_MCP_COMMAND = "npx"
FIREBASE_MCP_ARGS = ["-y", "firebase-mcp-server"]

async def call_firebase_mcp_tool(tool_name: str, arguments: dict = None) -> dict:
    """
    Invoke a Firebase MCP tool.
    """
    client = McpClient(FIREBASE_MCP_COMMAND, FIREBASE_MCP_ARGS)
    try:
        result = await client.call_tool(tool_name, arguments or {})
        return result
    finally:
        await client.close()
