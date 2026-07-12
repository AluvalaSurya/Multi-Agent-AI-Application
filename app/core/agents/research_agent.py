# from langchain_core.messages import HumanMessage

# from app.core.llm import LLMFactory
# from app.mcp.tools import MCPTools


# class ResearchAgent:

#     async def run(self, state):

#         model_name = state["model_name"]
#         query = state["user_query"]

#         llm = LLMFactory.get_llm(model_name)

#         search_results = await MCPTools.search(query)

#         prompt = f"""
# You are a research assistant.

# User Question:
# {query}

# Search Results:
# {search_results}

# Use only the relevant search results to answer clearly and accurately.
# """

#         response = llm.invoke(
#             [HumanMessage(content=prompt)]
#         )

#         # state["agent_outputs"]["research"] = response.content

#         # return state
#         return {"agent_outputs": {"research": response.content}}


from app.core.agents.base_agent import BaseAgent
from app.mcp.tools import MCPTools
from app.core.llm import LLMFactory


class ResearchAgent(BaseAgent):

    async def run(self, state):

        # self.get_llm(state["model_name"])
        self.llm = LLMFactory.get_llm("agent")

        query = state["user_query"]
        # query = (
        #         state
        #         .get("agent_inputs", {})
        #         .get("research", {})
        #         .get("query", state["user_query"])
        #     )

        search_results = await MCPTools.search(query)

        prompt = f"""
You are a Research Assistant.

User Question:
{query}

Search Results:

{search_results}

Use ONLY the search results to answer.

If the search results don't contain enough information,
state that clearly.
"""

        response = self.invoke_llm(prompt)

        return {
            "agent_outputs": {
                "research": response
            }
        }