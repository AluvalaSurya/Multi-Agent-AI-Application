# import asyncio

# from app.core.graph_builder import build_graph


# async def main():

#     graph = build_graph()

#     state = {

#         "messages": [],

#         "user_query":
#         "Read notes.txt and search latest LangGraph release.",

#         "system_prompt":"",

#         "model_name":"openai/gpt-oss-20b",

#         "allow_search":True,

#         "next_nodes":[],

#         "agent_outputs":{}

#     }

#     result = await graph.ainvoke(state)

#     print("\n========== FINAL ==========\n")

#     print(result["final_response"])


# asyncio.run(main())