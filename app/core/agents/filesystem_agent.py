from app.core.agents.base_agent import BaseAgent
from app.mcp.tools import MCPTools


class FilesystemAgent(BaseAgent):

    async def run(self, state):

        self.get_llm("agent")

        query = state["user_query"]

        path = state.get("file_path", "notes.txt")
        # Future implementation:
        # path = (
        #     state
        #     .get("agent_inputs", {})
        #     .get("filesystem", {})
        #     .get("path", "notes.txt")
        # )

        if not path:
            return {
                "agent_outputs": {
                    "filesystem": "No file path provided."
                }
            }

        file_result = await MCPTools.read_file(path)

        prompt = f"""
You are a Filesystem Assistant.

User Question:
{query}

File Contents:
{file_result}

Answer the user's question using ONLY the provided file contents.
If the answer is not present in the file, clearly state that.
"""

        response = self.invoke_llm(prompt)

        return {
            "agent_outputs": {
                "filesystem": response
            }
        }