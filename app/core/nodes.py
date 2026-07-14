from app.core.agents.research_agent import ResearchAgent
from app.core.agents.github_agent import GithubAgent
from app.core.agents.filesystem_agent import FilesystemAgent
from app.core.agents.response_agent import ResponseAgent
from app.core.supervisor import Supervisor
from app.core.aggregator import Aggregator

#research node
research_agent = ResearchAgent()
async def research_node(state):
    return await research_agent.run(state)

#github node 
github_agent = GithubAgent()
async def github_node(state):
    return await github_agent.run(state)

#filesystem node
filesystem_agent = FilesystemAgent()
async def filesystem_node(state):
    return await filesystem_agent.run(state)

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

