# import asyncio

# from app.core.nodes import research_node


# async def main():

#     state = {
#         "messages": [],
#         "user_query": "What is LangGraph?",
#         "system_prompt": "",
#         "model_name": "openai/gpt-oss-20b",
#         "allow_search": True,
#         "next_nodes": [],
#         "agent_outputs": {}
#     }

#     result = await research_node(state)

#     print(result["agent_outputs"]["research"])


# if __name__ == "__main__":
#     asyncio.run(main())


# # import asyncio

# # from app.mcp.client import MCPClient


# # async def main():

# #     async with MCPClient("tavily") as client:

# #         tools = await client.list_tools()

# #         print("\n===== AVAILABLE TOOLS =====\n")

# #         for tool in tools.tools:
# #             print(tool.name)
# #             print(tool.description)
# #             print("-" * 50)


# # if __name__ == "__main__":
# #     asyncio.run(main())