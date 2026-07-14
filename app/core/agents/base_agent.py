from abc import ABC, abstractmethod
from langchain_core.messages import HumanMessage
from app.core.llm import LLMFactory


class BaseAgent(ABC):

    def __init__(self):
        self.llm = None

    def get_llm(self, model_name: str):
        self.llm = LLMFactory.get_llm(model_name)

    def invoke_llm(self, prompt: str):

        response = self.llm.invoke(
            [
                HumanMessage(content=prompt)
            ]
        )

        return response.content

    @abstractmethod
    async def run(self, state):
        pass