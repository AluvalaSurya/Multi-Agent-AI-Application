# from langchain_core.messages import HumanMessage

# from app.core.llm import LLMFactory


# class ResponseAgent:

#     async def run(self, state):

#         llm = LLMFactory.get_llm(
#             state["model_name"]
#         )

#         user_query = state["user_query"]

#         system_prompt = state.get("system_prompt", "")

#         outputs = state.get("agent_outputs", {})

#         context = ""

#         for agent_name, result in outputs.items():

#             context += f"""
# ==============================
# Agent : {agent_name.upper()}
# ==============================

# {result}

# """

#         prompt = f"""
# {system_prompt}

# You are the final response agent.

# The following responses were produced by specialized AI agents.

# {context}

# User Question:
# {user_query}

# Instructions:

# 1. Combine all useful information.
# 2. Remove duplicate information.
# 3. Keep the response concise.
# 4. If agents disagree, mention the conflict.
# 5. Produce one final answer.
# """

#         response = llm.invoke(
#             [
#                 HumanMessage(content=prompt)
#             ]
#         )

#         # state["final_response"] = response.content

#         # return state

#         return {"final_response": response}



from app.core.agents.base_agent import BaseAgent
from app.core.llm import LLMFactory

class ResponseAgent(BaseAgent):

    async def run(self, state):

        # self.get_llm(state["model_name"])
        self.llm = LLMFactory.get_llm("agent")
        
        user_query = state["user_query"]

        system_prompt = state.get("system_prompt", "")

        outputs = state.get("agent_outputs", {})

        context = ""

        for agent_name, result in outputs.items():

            context += f"""

==============================
Agent : {agent_name.upper()}
==============================

{result}

"""

        prompt = f"""
{system_prompt}

You are the Final Response Agent.

The following responses were produced by specialized AI agents.

{context}

User Question:
{user_query}

Instructions:

1. Combine all useful information.
2. Remove duplicate information.
3. Keep the response concise.
4. If agents disagree, mention the conflict.
5. If information is insufficient, clearly state that.
6. Produce one final response.
"""

        response = self.invoke_llm(prompt)

        return {
            "final_response": response
        }