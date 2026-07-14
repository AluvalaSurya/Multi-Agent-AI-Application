from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.core import state
from app.core.graph_builder import build_graph
from app.config.settings import settings
from app.common.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(title="Multi AI Agent")


class ChatRequest(BaseModel):
    model_name: str
    user_query: str


@app.post("/chat")
async def chat(request: ChatRequest):

    logger.info(f"Received request for model: {request.model_name}")

    if request.model_name not in settings.ALLOWED_MODEL_NAMES:
        raise HTTPException(
            status_code=400,
            detail="Invalid model name"
        )

    state = {

        "model_name": request.model_name,
        "user_query": request.user_query,
        "next_nodes": [],
        "agent_inputs": {},
        "agent_outputs": {},
        "routing_reason": "",
        "routing_confidence": 0.0,
        "final_response": ""

    }

    try:

        compiled_graph = build_graph()
        result = await compiled_graph.ainvoke(state)

        logger.info("Successfully completed graph execution.")

        return {

            "answer": result.get("final_response"),

            "routing": {

                "agents": result.get("next_nodes"),
                "reason": result.get("routing_reason"),
                "confidence": result.get("routing_confidence")

            },

            "agent_outputs": result.get("agent_outputs", {})

        }

    except Exception:

        logger.exception("Graph execution failed.")

        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )


