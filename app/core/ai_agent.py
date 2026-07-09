# from langchain_groq import ChatGroq
# from langchain_community.tools.tavily_search import TavilySearchResults

# from langgraph.prebuilt import create_react_agent
# from langchain_core.messages.ai import AIMessage

# from app.config.settings import settings

# def get_response_from_ai_agents(llm_id , query , allow_search ,system_prompt):

#     llm = ChatGroq(model=llm_id)

#     tools = [TavilySearchResults(max_results=2)] if allow_search else []

#     agent = create_react_agent(
#         model=llm,
#         tools=tools,
#         state_modifier=system_prompt
#     )

#     state = {"messages" : query}

#     response = agent.invoke(state)

#     messages = response.get("messages")

#     ai_messages = [message.content for message in messages if isinstance(message,AIMessage)]

#     return ai_messages[-1]






from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage

from app.config.settings import settings
from app.common.logger import get_logger

logger = get_logger(__name__)

def get_response_from_ai_agents(llm_id, query, allow_search, system_prompt):
    try:
        logger.info(f"Creating ChatGroq model: {llm_id}")

        llm = ChatGroq(
            model=llm_id,
            api_key=settings.GROQ_API_KEY
        )

        logger.info(f"Search Enabled: {allow_search}")

        tools = [TavilySearchResults(max_results=2)] if allow_search else []

        logger.info("Creating ReAct Agent")

        agent = create_react_agent(
            model=llm,
            tools=tools,
            prompt=system_prompt
        )

        state = {"messages": query}

        logger.info("Invoking agent")

        response = agent.invoke(state)

        logger.info("Agent invocation successful")

        messages = response.get("messages")

        ai_messages = [
            message.content
            for message in messages
            if isinstance(message, AIMessage)
        ]

        return ai_messages[-1]

    except Exception:
        logger.exception("Error inside get_response_from_ai_agents")
        raise