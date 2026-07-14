from app.mcp_registry.client import MCPClient


class MCPTools:

    def __init__(self):
        self.client = MCPClient()

    #web search tool
    def web_search(self, query):

        return self.client.execute(

            server_name="tavily",
            tool_name="search",
            arguments={
                "query": query
            }

        )

    #git hub tool
    def github(self, operation, **kwargs):

        return self.client.execute(
            server_name="github",
            tool_name=operation,
            arguments=kwargs
        )

    #filesystem tool
    def filesystem(self, operation, **kwargs):

        return self.client.execute(
            server_name="filesystem",
            tool_name=operation,
            arguments=kwargs

        )