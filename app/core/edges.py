"""
Routing logic for LangGraph.

This module contains only edge/router functions.
It does not create the graph.
"""


from app.core.state import AgentState


def route_agent(state: AgentState) -> str:
    """
    Determines the next node to execute.

    Returns:
        str: Name of the next node.
    """
    return state["next_node"]