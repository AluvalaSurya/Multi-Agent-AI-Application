from dataclasses import dataclass
import os


@dataclass(frozen=True)
class MCPServerConfig:
    name: str
    command: str
    args: list[str]
    env: dict[str, str] | None = None


MCP_SERVERS = {

    "filesystem": MCPServerConfig(
        name="filesystem",
        command="npx",
        args=[
            "-y",
            "@modelcontextprotocol/server-filesystem",
            "./workspace"
        ]
    ),

    "github": MCPServerConfig(
        name="github",
        command="npx",
        args=[
            "-y",
            "@modelcontextprotocol/server-github"
        ],
        env={
            "GITHUB_PERSONAL_ACCESS_TOKEN":
                os.getenv("GITHUB_TOKEN", "")
        }
    ),

    
    "tavily": MCPServerConfig(
        name="tavily",
        command="npx",
        args=[
            "-y",
            "tavily-mcp@latest"
        ],
        env={
            "TAVILY_API_KEY":
                os.getenv("TAVILY_API_KEY", "")
        }
    )

}