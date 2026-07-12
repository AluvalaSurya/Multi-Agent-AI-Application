from typing import Annotated, TypedDict, List
from langgraph.graph.message import add_messages

def merge_dict(left: dict, right: dict):
    return {**left, **right}

class AgentState(TypedDict):
    """
    Shared state passed between all LangGraph nodes.
    """

    messages: Annotated[List, add_messages]
    user_query: str
    system_prompt: str
    model_name: str
    allow_search: bool
    next_nodes: list[str]
    routing_reason: str
    routing_confidence: float
    agent_outputs: Annotated[dict[str, str],merge_dict]
    final_response: str