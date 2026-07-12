# from app.core.agents.base_agent import BaseAgent


# class FilesystemAgent(BaseAgent):

#     def run(self):

#         prompt = f"""
#         Filesystem Assistant

#         User Request:
#         {self.state["user_query"]}
#         """
        
#         self.state["agent_response"] = self.invoke_llm(prompt)

#         return self.state


# from langchain_core.messages import HumanMessage

# from app.core.llm import LLMFactory
# from app.mcp.tools import MCPTools


# class FilesystemAgent:

#     def __init__(self):

#         self.llm = None

#     async def run(self, state):

#         model_name = state["model_name"]

#         query = state["user_query"]

#         self.llm = LLMFactory.get_llm(model_name)

#         # Example:
#         # Later we'll extract the file path dynamically.
#         path = state.get("file_path", "notes.txt")

#         file_result = await MCPTools.read_file(path)

#         prompt = f"""
# You are a filesystem assistant.

# User Question:
# {query}

# File Content:

# {file_result}

# Answer the user's question using the file content.
# """

#         response = self.llm.invoke(
#             [HumanMessage(content=prompt)]
#         )

#         # state["agent_outputs"]["filesystem"] = response.content

#         # return state

#         return {"agent_outputs": {"filesystem": response.content}}


from app.core.agents.base_agent import BaseAgent
from app.mcp.tools import MCPTools
from app.core.llm import LLMFactory


class FilesystemAgent(BaseAgent):

    async def run(self, state):

        # self.get_llm(state["model_name"])
        self.llm = LLMFactory.get_llm("agent")
        query = state["user_query"]

        path = state.get("file_path", "notes.txt")
        # path = (
        #     state
        #     .get("agent_inputs", {})
        #     .get("filesystem", {})
        #     .get("path")
        # )

        if not path:

            return {
                "agent_outputs": {
                    "filesystem":
                        "No file path provided."
                }
            }
        
        file_result = await MCPTools.read_file(path)

        prompt = f"""
You are a Filesystem Assistant.

User Question:
{query}

File Contents:

{file_result}

Answer the question using ONLY the file contents.
If the answer is not present, say so.
"""

        response = self.invoke_llm(prompt)

        return {
            "agent_outputs": {
                "filesystem": response
            }
        }