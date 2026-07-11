from langchain_groq import ChatGroq

from app.config.settings import settings


class LLMFactory:

    @staticmethod
    def get_llm(model_name: str):

        return ChatGroq(
            model=model_name,
            api_key=settings.GROQ_API_KEY
        )