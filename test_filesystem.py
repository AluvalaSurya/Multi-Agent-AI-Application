import asyncio

from app.core.nodes import filesystem_node


async def main():

    state = {
        "messages": [],
        "user_query": "Summarize this file.",
        "system_prompt": "",
        "model_name": "groq/compound",
        "allow_search": False,
        "next_nodes": [],
        "agent_outputs": {}
    }

    result = await filesystem_node(state)

    print("\n====== RESULT ======\n")
    print(result["agent_outputs"]["filesystem"])


if __name__ == "__main__":
    asyncio.run(main())