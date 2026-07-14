# """
# Routing logic for LangGraph.
# """

from typing import Literal

def route_supervisor(state) -> list[str]:

    routes = []

    for node in state.get("next_nodes", []):

        if node == "research":
            routes.append("research")

        elif node == "filesystem":
            routes.append("filesystem")

        elif node == "github":
            routes.append("github")

    return routes


def route_response(state) -> Literal["response"]:
    return "response"