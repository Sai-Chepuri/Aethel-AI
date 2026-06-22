from tools.mcp_client import McpClient

KNOWLEDGE_MCP_COMMAND = "npx"
KNOWLEDGE_MCP_ARGS = ["-y", "google-developer-knowledge"]

async def search_developer_documents(query: str) -> dict:
    """
    Search developer documents using the google-developer-knowledge MCP server.
    """
    client = McpClient(KNOWLEDGE_MCP_COMMAND, KNOWLEDGE_MCP_ARGS)
    try:
        result = await client.call_tool("search_documents", {"query": query})
        return result
    finally:
        await client.close()
