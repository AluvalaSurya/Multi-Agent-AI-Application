import asyncio

from app.core.nodes import supervisor_node


async def main():

    state = {

        "messages": [],

        "user_query":
        "Read requirements.txt and search latest LangGraph release.",

        "system_prompt":"",
        "model_name":"openai/gpt-oss-20b",
        "allow_search":True,
        "next_nodes":[],
        "agent_outputs":{}

    }

    result = await supervisor_node(state)

    print(result)


asyncio.run(main())