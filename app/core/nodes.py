from app.core.agents.research_agent import ResearchAgent
from app.core.agents.github_agent import GithubAgent
from app.core.agents.filesystem_agent import FilesystemAgent
from app.core.agents.response_agent import ResponseAgent
from app.core.supervisor import Supervisor
from app.core.aggregator import Aggregator

#research using tavily 
research_agent = ResearchAgent()
# def research_node(state):
#     return ResearchAgent(state).run()

async def research_node(state):
    return await research_agent.run(state)

#for github 
def github_node(state):
    return GithubAgent(state).run()

#for filesystem 
filesystem_agent = FilesystemAgent()
# def filesystem_node(state):
#     return FilesystemAgent(state).run()


async def filesystem_node(state):
    return await filesystem_agent.run(state)


# def response_node(state):
#     return ResponseAgent(state).run()


#supervisor node
supervisor = Supervisor()
async def supervisor_node(state):
    return await supervisor.run(state)

#aggregator node
aggregator = Aggregator()
async def aggregator_node(state):
    return await aggregator.run(state)

#repsonse node
response_agent = ResponseAgent()
async def response_node(state):
    return await response_agent.run(state)

