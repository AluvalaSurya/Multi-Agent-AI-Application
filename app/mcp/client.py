from __future__ import annotations

from contextlib import AsyncExitStack

from mcp import ClientSession
from mcp.client.stdio import (
    stdio_client,
    StdioServerParameters,
)

from app.mcp.config import MCP_SERVERS


class MCPClient:

    def __init__(self, server_name: str):

        if server_name not in MCP_SERVERS:
            raise ValueError(
                f"Unknown MCP server: {server_name}"
            )

        self.config = MCP_SERVERS[server_name]

        self.exit_stack = AsyncExitStack()

        self.session = None

    async def connect(self):

        server = StdioServerParameters(
            command=self.config.command,
            args=self.config.args,
            env=self.config.env
        )

        read_stream, write_stream = (
            await self.exit_stack.enter_async_context(
                stdio_client(server)
            )
        )

        self.session = (
            await self.exit_stack.enter_async_context(
                ClientSession(
                    read_stream,
                    write_stream
                )
            )
        )

        await self.session.initialize()

    async def close(self):

        await self.exit_stack.aclose()

    async def list_tools(self):

        if self.session is None:
            raise RuntimeError(
                "MCP Client not connected."
            )

        return await self.session.list_tools()

    async def call_tool(

        self,

        tool_name: str,

        arguments: dict

    ):

        if self.session is None:
            raise RuntimeError(
                "MCP Client not connected."
            )

        return await self.session.call_tool(

            name=tool_name,

            arguments=arguments

        )

    async def __aenter__(self):

        await self.connect()

        return self

    async def __aexit__(

        self,

        exc_type,

        exc,

        tb

    ):

        await self.close()