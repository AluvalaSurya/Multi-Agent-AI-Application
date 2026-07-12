from langchain_core.messages import HumanMessage

from app.core.llm import LLMFactory
from app.mcp.tools import MCPTools


class ResearchAgent:

    async def run(self, state):

        model_name = state["model_name"]
        query = state["user_query"]

        llm = LLMFactory.get_llm(model_name)

        search_results = await MCPTools.search(query)

        prompt = f"""
You are a research assistant.

User Question:
{query}

Search Results:
{search_results}

Use only the relevant search results to answer clearly and accurately.
"""

        response = llm.invoke(
            [HumanMessage(content=prompt)]
        )

        state["agent_outputs"]["research"] = response.content

        return state