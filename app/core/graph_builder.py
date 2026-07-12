from langgraph.graph import StateGraph, START, END

from app.core.state import AgentState

from app.core.nodes import (
    supervisor_node,
    research_node,
    filesystem_node,
    github_node,
    aggregator_node,
    response_node
)

from app.core.edges import route_supervisor


def build_graph():

    graph = StateGraph(AgentState)

    #nodes
    graph.add_node("supervisor", supervisor_node)
    graph.add_node("research", research_node)
    graph.add_node("filesystem", filesystem_node)
    graph.add_node("github", github_node)
    graph.add_node("aggregator", aggregator_node)
    graph.add_node("response", response_node)

    #edges
    graph.add_edge(START, "supervisor")

    graph.add_conditional_edges(
        "supervisor",
        route_supervisor,
        {
            "research": "research",
            "filesystem": "filesystem",
            "github": "github"
        }
    )

    graph.add_edge("research", "aggregator")
    graph.add_edge("filesystem", "aggregator")
    graph.add_edge("github", "aggregator")
    graph.add_edge("aggregator", "response")
    graph.add_edge("response", END)

    return graph.compile()