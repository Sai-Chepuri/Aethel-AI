from tools.mcp_client import McpClient

# Default stdio runner commands if self-managing the server
# Adjust paths or commands to match local system configuration if needed
GITHUB_MCP_COMMAND = "npx"
GITHUB_MCP_ARGS = ["-y", "@modelcontextprotocol/server-github"]

async def list_github_issues(repository: str, token: str = None) -> dict:
    """
    Call the GitHub MCP tool to list repository issues.
    """
    args = list(GITHUB_MCP_ARGS)
    # We can inject environmental variables or arguments for credentials
    client = McpClient(GITHUB_MCP_COMMAND, args)
    try:
        # Example invocation of search_issues or list_issues
        result = await client.call_tool("list_issues", {"q": f"repo:{repository}"})
        return result
    finally:
        await client.close()

async def create_github_pull_request(repo: str, title: str, head: str, base: str, body: str = "") -> dict:
    """
    Call the GitHub MCP tool to create a pull request.
    """
    client = McpClient(GITHUB_MCP_COMMAND, GITHUB_MCP_ARGS)
    try:
        result = await client.call_tool("create_pull_request", {
            "owner": repo.split("/")[0],
            "repo": repo.split("/")[1],
            "title": title,
            "head": head,
            "base": base,
            "body": body
        })
        return result
    finally:
        await client.close()
