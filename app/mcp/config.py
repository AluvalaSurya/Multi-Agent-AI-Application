from dataclasses import dataclass
import os


@dataclass(frozen=True)
class MCPServer:
    command: str
    args: list[str]
    env: dict | None = None


SERVERS = {

    "filesystem": MCPServer(
        command="npx",
        args=[
            "-y",
            "@modelcontextprotocol/server-filesystem",
            "./workspace"
        ]

    ),

    "github": MCPServer(
        command="npx",
        args=[
            "-y",
            "@modelcontextprotocol/server-github"
        ],

        env={
            "GITHUB_PERSONAL_ACCESS_TOKEN":
            os.getenv("GITHUB_TOKEN")

        }

    ),

    "tavily": MCPServer(

        command="python",
        args=[
            "-m",
            "tavily_mcp"

        ],

        env={
            "TAVILY_API_KEY":
            os.getenv("TAVILY_API_KEY")

        }

    )

}