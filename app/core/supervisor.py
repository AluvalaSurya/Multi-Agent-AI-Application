# from app.core.state import AgentState


# def supervisor(state: AgentState):

#     query = state["user_query"].lower()

#     #github
#     if any(word in query for word in [
#         "github",
#         "repository",
#         "repo",
#         "pull request",
#         "issue"
#     ]):

#         state["next_node"] = "github"

#     #filesystem
#     elif any(word in query for word in [
#         "file",
#         "folder",
#         "directory",
#         "read",
#         "write",
#         "create"
#     ]):

#         state["next_node"] = "filesystem"

    
#     #research
#     elif state["allow_search"]:
#         state["next_node"] = "research"

#     #normal llm
#     else:
#         state["next_node"] = "response"

#     return state

# import json

# from langchain_core.messages import HumanMessage

# from app.core.llm import LLMFactory


# class Supervisor:

#     async def run(self, state):

#         # llm = LLMFactory.get_llm(
#         #     state["model_name"]
#         # )

#         llm = LLMFactory.get_llm("supervisor")

#         user_query = state["user_query"]

#         prompt = f"""
# You are a Supervisor Agent.

# Your job is to decide which specialized AI agents should execute.

# Available Agents:

# 1. research
# - Internet search
# - Current events
# - Technical concepts
# - General knowledge

# 2. filesystem
# - Read local files
# - Write local files
# - List directories

# 3. github
# - Search repositories
# - Read repository files
# - Create GitHub issues

# Return ONLY valid JSON.

# Example:

# {{
#     "next_nodes":[
#         "research"
#     ],
#     "agent_inputs":{

#         "filesystem":{
#             "path":"requirements.txt"
#         },

#         "research":{
#             "query":"latest LangGraph release"
#         },

#         "github":{
#             "owner":"",
#             "repo":"",
#             "path":""
#         }

#     },
#     "reason": "Explain in one sentence why these agents were selected.",
#     "confidence": 0.95
# }}

# User Query:

# {user_query}
# """

#         response = llm.invoke(
#             [
#                 HumanMessage(content=prompt)
#             ]
#         )

#         # print("\n SUPERVISOR RAW OUTPUT")
#         # print(response.content)
        
#         try:

#             routing = json.loads(response.content)

#             # state["next_nodes"] = routing.get("next_nodes",[])
#             # state["routing_reason"] = routing.get("reason", "")
#             # state["routing_confidence"] = routing.get("confidence", 1.0)

#             return {
#                 "next_nodes": routing.get("next_nodes", []),
#                 "agent_inputs":routing.get("agent_inputs", {}),
#                 "routing_reason": routing.get("reason", ""),
#                 "routing_confidence": routing.get("confidence", 1.0)
#             }

#         except Exception:

#         #     state["next_nodes"] = ["research"]
#         #     state["routing_reason"] = "Fallback routing"
#         #     state["routing_confidence"] = 0.0

#         # return state

#             return {
#                 "next_nodes": ["research"],
#                 "agent_inputs":{},
#                 "routing_reason": "Fallback routing",
#                 "routing_confidence": 0.0
#             }
    
import json

from langchain_core.messages import HumanMessage

from app.core.llm import LLMFactory


class Supervisor:   

    async def run(self, state):

        llm = LLMFactory.get_llm("supervisor")

        user_query = state["user_query"]

        example_json = """
{
    "next_nodes": [
        "filesystem",
        "research"
    ],
    "agent_inputs": {
        "filesystem": {
            "path": "requirements.txt"
        },
        "research": {
            "query": "latest LangGraph release"
        },
        "github": {
            "owner": "AluvalaSurya",
            "repo": "Multi-Agent-AI-Application",
            "path": "README.md"
        }
    },
    "reason": "The user wants to read a local file and search the web.",
    "confidence": 0.98
}
"""

        prompt = f"""
You are a Supervisor Agent.

Your responsibility is to decide:

1. Which AI agents should execute.
2. What input each selected agent should receive.

Available Agents

1. research
- Internet search
- Current events
- Technical concepts
- General knowledge

2. filesystem
- Read local files
- Write local files
- List directories

3. github
- Search repositories
- Read repository files
- Create GitHub issues

Rules:

- Return ONLY valid JSON.
- Do NOT return markdown.
- Do NOT explain anything.
- Include ONLY the agents that are required.
- If an agent is not used, omit it from agent_inputs.
- Confidence must be between 0 and 1.

Example:

{example_json}

User Query:

{user_query}
"""

        response = llm.invoke(
            [
                HumanMessage(content=prompt)
            ]
        )

        # Uncomment for debugging
        # print(response.content)

        try:

            routing = json.loads(response.content)

            return {

                "next_nodes":
                    routing.get("next_nodes", []),

                "agent_inputs":
                    routing.get("agent_inputs", {}),

                "routing_reason":
                    routing.get("reason", ""),

                "routing_confidence":
                    routing.get("confidence", 1.0)
            }

        except Exception:

            return {

                "next_nodes": ["research"],

                "agent_inputs": {
                    "research": {
                        "query": user_query
                    }
                },

                "routing_reason":
                    "Fallback routing",

                "routing_confidence":
                    0.0
            }