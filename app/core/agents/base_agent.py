from abc import ABC, abstractmethod

from langchain_core.messages import HumanMessage
from app.core.llm import LLMFactory
from app.core.state import AgentState


class BaseAgent(ABC):

    def __init__(self, state: AgentState):

        self.state = state
        self.llm = LLMFactory.get_llm(
            state["model_name"]
        )

    @abstractmethod
    def run(self):
        pass

    def invoke_llm(self, prompt: str):

        response = self.llm.invoke(
            [
                HumanMessage(
                    content=prompt
                )
            ]
        )

        return response.content