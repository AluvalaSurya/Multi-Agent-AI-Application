from app.core.state import AgentState


def supervisor(state: AgentState):

    query = state["user_query"].lower()

    #github
    if any(word in query for word in [
        "github",
        "repository",
        "repo",
        "pull request",
        "issue"
    ]):

        state["next_node"] = "github"

    #filesystem
    elif any(word in query for word in [
        "file",
        "folder",
        "directory",
        "read",
        "write",
        "create"
    ]):

        state["next_node"] = "filesystem"

    
    #research
    elif state["allow_search"]:
        state["next_node"] = "research"

    #normal llm
    else:
        state["next_node"] = "response"

    return state