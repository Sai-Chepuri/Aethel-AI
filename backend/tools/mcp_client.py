import json
import asyncio

class McpClient:
    """
    A lightweight, zero-dependency client for communicating with Model Context Protocol (MCP) servers
    over Stdio transport (standard input / standard output).
    """
    def __init__(self, command: str, args: list = None):
        self.command = command
        self.args = args or []
        self.process = None
        self.request_id = 1

    async def connect(self):
        """Spawns the MCP server process and binds communication pipes."""
        try:
            self.process = await asyncio.create_subprocess_exec(
                self.command,
                *self.args,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.DEVNULL
            )
        except Exception as e:
            raise RuntimeError(f"Failed to start MCP server process '{self.command}': {e}")

    async def call_tool(self, tool_name: str, arguments: dict = None) -> dict:
        """Invokes a tool on the MCP server via JSON-RPC."""
        if not self.process:
            await self.connect()
        
        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments or {}
            },
            "id": self.request_id
        }
        self.request_id += 1
        
        try:
            request_str = json.dumps(request) + "\n"
            self.process.stdin.write(request_str.encode())
            await self.process.stdin.drain()
            
            response_line = await self.process.stdout.readline()
            if not response_line:
                raise RuntimeError("MCP server disconnected or EOF reached.")
                
            response = json.loads(response_line.decode())
            if "error" in response:
                raise RuntimeError(f"MCP server returned error: {response['error']}")
                
            return response.get("result", {})
        except Exception as e:
            await self.close()
            raise RuntimeError(f"Error calling MCP tool '{tool_name}': {e}")

    async def close(self):
        """Cleans up process resources."""
        if self.process:
            try:
                self.process.terminate()
                await self.process.wait()
            except Exception:
                pass
            self.process = None
