from app.core.agents.base_agent import BaseAgent
from app.mcp.tools import MCPTools
from app.core.llm import LLMFactory


class GithubAgent(BaseAgent):

    async def run(self, state):

        self.get_llm("agent")

        query = state["user_query"]
        owner = state.get("owner")
        repo = state.get("repo")
        path = state.get("repo_path")

        github_data = ""

        if owner and repo and path:

            github_data = await MCPTools.get_file_contents(
                owner=owner,
                repo=repo,
                path=path
            )

        prompt = f"""
You are a GitHub Assistant.

User Question:
{query}

GitHub Data:

{github_data}

Answer using ONLY the GitHub data.
"""

        response = self.invoke_llm(prompt)

        return {
            "agent_outputs": {
                "github": response
            }
        }
