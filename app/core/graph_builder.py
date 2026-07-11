from langgraph.graph import StateGraph, START, END

from app.core.state import AgentState

from app.core.supervisor import supervisor
from app.core.edges import route_agent

from app.core.nodes import (
    research_node,
    github_node,
    filesystem_node,
    response_node
)


class GraphBuilder:

    @staticmethod
    def build():

        workflow = StateGraph(AgentState)

        # Nodes

        workflow.add_node("supervisor",supervisor)
        workflow.add_node("research_agent",research_node)
        workflow.add_node("github_agent",github_node)
        workflow.add_node("filesystem_agent",filesystem_node)
        workflow.add_node("response_agent",response_node)

        # Start

        workflow.add_edge(START,"supervisor")

        # Conditional Routing

        workflow.add_conditional_edges(

            "supervisor",

            route_agent,

            {
                "research":"research_agent",
                "github":"github_agent",
                "filesystem":"filesystem_agent",
                "response":"response_agent"

            }

        )


        # Finish

        workflow.add_edge("research_agent",END)
        workflow.add_edge("github_agent",END)
        workflow.add_edge("filesystem_agent",END)
        workflow.add_edge("response_agent",END)

        return workflow.compile()