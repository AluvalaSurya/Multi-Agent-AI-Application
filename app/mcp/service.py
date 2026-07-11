from mcp import ClientSession
from mcp import StdioServerParameters

from mcp.client.stdio import stdio_client
from app.mcp.config import SERVERS


class MCPService:

    async def call_tool(
        self,
        server_name: str,
        tool_name: str,
        arguments: dict

    ):

        config = SERVERS[server_name]
        server = StdioServerParameters(
            command=config.command,
            args=config.args,
            env=config.env

        )

        async with stdio_client(server) as (read,write):

            async with ClientSession(read,write) as session:

                await session.initialize()
                result = await session.call_tool(
                    tool_name,
                    arguments=arguments
                )

                return result