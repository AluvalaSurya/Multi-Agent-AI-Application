from app.mcp.service import MCPService


class MCPTools:

    def __init__(self):
        self.service = MCPService()

    async def search(self,query: str):

        return await self.service.call_tool("tavily","search",
            {"query": query}
        )

    async def read_file(self,path: str):

        return await self.service.call_tool(
            "filesystem",
            "read_file",
            {"path": path}
        )

    async def write_file(self,path: str,content: str):

        return await self.service.call_tool(
            "filesystem",
            "write_file",
            {"path": path,
             "content": content
}

        )

    async def create_issue(
        self,
        owner: str,
        repo: str,
        title: str,
        body: str

    ):

        return await self.service.call_tool("github","create_issue",
            {
                "owner": owner,
                "repo": repo,
                "title": title,
                "body": body

            }

        )