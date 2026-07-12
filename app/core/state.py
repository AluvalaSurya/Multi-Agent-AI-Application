from typing import Annotated, TypedDict, List
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """
    Shared state passed between all LangGraph nodes.
    """

    messages: Annotated[List, add_messages]
    user_query: str
    system_prompt: str
    model_name: str
    allow_search: bool
    next_node: str
    agent_outputs: dict[str, str]