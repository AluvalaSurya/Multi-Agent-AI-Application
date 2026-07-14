from app.core.agents.base_agent import BaseAgent
from app.mcp.tools import MCPTools
from app.core.llm import LLMFactory


class ResearchAgent(BaseAgent):

    async def run(self, state):

        # self.get_llm(state["model_name"])
        # self.llm = LLMFactory.get_llm("agent")
        self.get_llm("agent")

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