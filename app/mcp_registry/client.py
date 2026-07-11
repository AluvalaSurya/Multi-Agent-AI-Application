from typing import Dict, Any

from app.mcp.registry import MCPRegistry


class MCPClient:

    def __init__(self):

        self.registry = MCPRegistry()

    def execute(
        self,
        server_name: str,
        tool_name: str,
        arguments: Dict[str, Any]
    ):

        server = self.registry.get_server(server_name)

        if server is None:

            raise ValueError(
                f"MCP Server '{server_name}' not registered."
            )

        return server.execute_tool(
            tool_name,
            arguments
        )