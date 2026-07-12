import asyncio

from app.core.nodes import response_node


async def main():

    state = {

        "messages": [],

        "user_query": "Explain LangGraph and the project requirements.",

        "system_prompt": "",

        "model_name": "openai/gpt-oss-20b",

        "allow_search": True,

        "next_nodes": [],

        "agent_outputs": {

            "research":
                "LangGraph is a framework for building stateful AI workflows.",

            "filesystem":
                "requirements.txt contains langgraph, fastapi, streamlit, mcp.",

            "github":
                "README.md describes the project as a Multi AI Agent."
        }

    }

    result = await response_node(state)

    print("\n========== FINAL RESPONSE ==========\n")

    print(result["final_response"])


if __name__ == "__main__":
    asyncio.run(main())