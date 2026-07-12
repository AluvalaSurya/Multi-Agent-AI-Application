# # import asyncio

# # from app.mcp.client import MCPClient


# # async def main():

# #     async with MCPClient("github") as client:

# #         tools = await client.list_tools()

# #         for tool in tools.tools:
# #             print(tool.name)


# # asyncio.run(main())

# import asyncio,json


# from app.mcp.tools import MCPTools


# async def main():

#     # result = await MCPTools.search_repositories(
#     #     "Multi-Agent-AI-Application"
#     # )

#     result = await MCPTools.get_file_contents(
#     owner="AluvalaSurya",
#     repo="Multi-Agent-AI-Application",
#     path="requirements.txt"
# )   
    
#     data = json.loads(result.content[0].text)

#     file_content = data["content"]

#     print(file_content)

#     # print(result)


# if __name__ == "__main__":
#     asyncio.run(main())