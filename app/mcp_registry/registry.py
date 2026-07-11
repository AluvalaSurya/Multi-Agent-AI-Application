from app.mcp.servers.filesystem_server import FilesystemServer
from app.mcp.servers.github_server import GithubServer
from app.mcp.servers.tavily_server import TavilyServer


class MCPRegistry:

    def __init__(self):

        self._servers = {

            "filesystem": FilesystemServer(),

            "github": GithubServer(),

            "tavily": TavilyServer()

        }

    def get_server(self, name):

        return self._servers.get(name)