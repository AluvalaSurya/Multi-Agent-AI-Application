# from langchain_groq import ChatGroq

# from app.config.settings import settings


# class LLMFactory:

#     @staticmethod
#     def get_llm(model_name: str):

#         return ChatGroq(
#             model=model_name,
#             api_key=settings.GROQ_API_KEY
#         )


from langchain_groq import ChatGroq

from app.config.settings import settings


class LLMFactory:

    MODELS = {

        "supervisor": "openai/gpt-oss-20b",

        "agent": "llama-3.3-70b-versatile",

        "response": "llama-3.3-70b-versatile"

    }

    @staticmethod
    def get_llm(role: str = "agent"):

        return ChatGroq(
            model=LLMFactory.MODELS[role],
            api_key=settings.GROQ_API_KEY
        )