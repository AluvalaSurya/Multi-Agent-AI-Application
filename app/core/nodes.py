from app.core.agents.research_agent import ResearchAgent
from app.core.agents.github_agent import GithubAgent
from app.core.agents.filesystem_agent import FilesystemAgent
from app.core.agents.response_agent import ResponseAgent

#research using tavily 
def research_node(state):
    return ResearchAgent(state).run()

#for github 
def github_node(state):
    return GithubAgent(state).run()

#for filesystem 
filesystem_agent = FilesystemAgent()
# def filesystem_node(state):
#     return FilesystemAgent(state).run()


async def filesystem_node(state):
    return await filesystem_agent.run(state)


def response_node(state):
    return ResponseAgent(state).run()


