from app.mcp.client import MCPClient


class MCPTools:

    @staticmethod
    async def read_file(path: str):

        async with MCPClient("filesystem") as client:

            return await client.call_tool(

                "read_file",

                {
                    "path": path
                }

            )

    @staticmethod
    async def write_file(

        path: str,

        content: str

    ):

        async with MCPClient("filesystem") as client:

            return await client.call_tool(

                "write_file",

                {
                    "path": path,

                    "content": content

                }

            )

    @staticmethod
    async def list_directory(path: str):

        async with MCPClient("filesystem") as client:

            return await client.call_tool(

                "list_directory",

                {
                    "path": path
                }

            )

    @staticmethod
    async def search(query: str):

        async with MCPClient("tavily") as client:

            return await client.call_tool(

                "tavily_search",

                {
                    "query": query
                }

            )

    @staticmethod
    async def research(query: str):

        async with MCPClient("tavily") as client:

            return await client.call_tool(
                "tavily_research",
                {
                    "query": query
                }
            )

    @staticmethod
    async def extract(url: str):

        async with MCPClient("tavily") as client:

            return await client.call_tool(
                "tavily_extract",
                {
                    "urls": [url]
                }
            )

    @staticmethod
    async def crawl(url: str):

        async with MCPClient("tavily") as client:

            return await client.call_tool(
                "tavily_crawl",
                {
                    "url": url
                }
            )

    @staticmethod
    async def map(url: str):

        async with MCPClient("tavily") as client:

            return await client.call_tool(
                "tavily_map",
                {
                    "url": url
                }
            )

    @staticmethod
    async def create_issue(

        owner: str,

        repo: str,

        title: str,

        body: str

    ):

        async with MCPClient("github") as client:

            return await client.call_tool(

                "create_issue",

                {
                    "owner": owner,

                    "repo": repo,

                    "title": title,

                    "body": body

                }

            )